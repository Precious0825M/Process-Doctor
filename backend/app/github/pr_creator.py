"""GitHub pull request creator"""

import base64
import logging
from typing import Any, Dict, Optional

import yaml
from app.agents.pr_writer import PRWriterAgent
from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


class PRCreator:
    """Create pull requests with workflow improvements"""
    
    def __init__(self):
        self.client = GitHubClient()
        self.pr_writer = PRWriterAgent()
        # In-memory storage for fix data (TODO: replace with Redis/DB)
        self._fix_cache: Dict[str, Any] = {}
    
    def store_fix_data(self, fix_id: str, fix_data: Dict[str, Any]):
        """Store fix data for later retrieval"""
        self._fix_cache[fix_id] = fix_data
        logger.info(f"Stored fix data for fix {fix_id}")
    
    async def create_pr(
        self,
        fix_id: str,
        repository: str,
        branch: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create pull request with optimized workflow.
        
        Args:
            fix_id: Fix identifier
            repository: Repository name
            branch: Branch name for PR
            title: PR title (optional)
            description: PR description (optional)
        
        Returns:
            Created PR information
        """
        logger.info(f"Creating PR for fix {fix_id} in {repository}")
        
        try:
            # Retrieve fix data from storage
            fix_data = self._fix_cache.get(fix_id)
            if not fix_data:
                raise ValueError(f"Fix data not found for fix_id: {fix_id}")
            
            # Extract workflow YAML
            workflow_yaml = fix_data.get("workflow_yaml")
            if not workflow_yaml:
                # Try to convert workflow dict to YAML
                workflow_dict = fix_data.get("workflow", {})
                if workflow_dict:
                    workflow_yaml = yaml.dump(workflow_dict, default_flow_style=False)
                else:
                    raise ValueError("No workflow data found in fix")
            
            # Generate PR description if not provided
            if not description:
                description = await self.pr_writer.generate_pr_description(fix_data)
            
            # Set default title if not provided
            if not title:
                title = "🚀 Optimize CI/CD workflow for improved performance"
            
            # Get repository object
            repo = self.client.get_repository(repository)
            
            # Get default branch
            default_branch = repo.default_branch
            base_ref = repo.get_git_ref(f"heads/{default_branch}")
            
            # Create new branch
            try:
                new_ref = repo.create_git_ref(
                    ref=f"refs/heads/{branch}",
                    sha=base_ref.object.sha
                )
                logger.info(f"Created branch: {branch}")
            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg or "Resource not accessible" in error_msg:
                    raise ValueError(
                        f"GitHub token does not have permission to create branches in {repository}. "
                        "Please ensure your token has 'repo' scope and write access to this repository."
                    )
                logger.warning(f"Branch creation failed, attempting to use existing branch: {e}")
                try:
                    new_ref = repo.get_git_ref(f"heads/{branch}")
                    logger.info(f"Using existing branch: {branch}")
                except Exception as get_error:
                    raise ValueError(
                        f"Failed to create or access branch '{branch}': {error_msg}. "
                        "The branch may not exist and you don't have permission to create it."
                    )
            
            # Commit optimized workflow file to the branch
            workflow_path = ".github/workflows/ci.yml"  # Default path, could be configurable
            
            try:
                # Try to get existing file to update it
                existing_file = repo.get_contents(workflow_path, ref=default_branch)
                
                # Handle case where get_contents returns a list
                if isinstance(existing_file, list):
                    existing_file = existing_file[0]
                
                commit_message = f"Optimize CI/CD workflow\n\nChanges:\n"
                for change in fix_data.get("changes", []):
                    commit_message += f"- {change.get('description', 'Optimization')}\n"
                
                # Update the file
                repo.update_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_yaml,
                    sha=existing_file.sha,
                    branch=branch
                )
                logger.info(f"Updated workflow file: {workflow_path}")
                
            except Exception as e:
                # File doesn't exist, create it
                logger.info(f"Creating new workflow file: {workflow_path}")
                commit_message = f"Add optimized CI/CD workflow\n\nChanges:\n"
                for change in fix_data.get("changes", []):
                    commit_message += f"- {change.get('description', 'Optimization')}\n"
                
                repo.create_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_yaml,
                    branch=branch
                )
            
            # Create pull request
            pr = repo.create_pull(
                title=title,
                body=description,
                head=branch,
                base=default_branch
            )
            
            logger.info(f"Created PR #{pr.number}: {pr.html_url}")
            
            return {
                "pr_number": pr.number,
                "pr_url": pr.html_url,
                "branch": branch,
                "title": title
            }
            
        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            raise
    
    async def get_pr_status(self, repository: str, pr_number: int) -> Dict[str, Any]:
        """
        Get pull request status.
        
        Args:
            repository: Repository name
            pr_number: PR number
        
        Returns:
            PR status information
        """
        logger.info(f"Getting PR status for {repository}#{pr_number}")
        
        try:
            repo = self.client.get_repository(repository)
            pr = repo.get_pull(pr_number)
            
            # Get check runs status
            commits = pr.get_commits()
            latest_commit = list(commits)[-1] if commits.totalCount > 0 else None
            
            checks_status = "unknown"
            if latest_commit:
                check_runs = latest_commit.get_check_runs()
                if check_runs.totalCount > 0:
                    statuses = [run.status for run in check_runs]
                    if all(s == "completed" for s in statuses):
                        conclusions = [run.conclusion for run in check_runs]
                        checks_status = "success" if all(c == "success" for c in conclusions) else "failure"
                    else:
                        checks_status = "pending"
            
            return {
                "number": pr.number,
                "state": pr.state,
                "mergeable": pr.mergeable,
                "merged": pr.merged,
                "checks_status": checks_status,
                "url": pr.html_url,
                "title": pr.title,
                "created_at": pr.created_at.isoformat() if pr.created_at else None,
                "updated_at": pr.updated_at.isoformat() if pr.updated_at else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get PR status: {e}")
            raise

# Made with Bob
