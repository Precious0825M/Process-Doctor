"""GitHub pull request creator"""

import logging
from typing import Any, Dict, Optional

from app.agents.pr_writer import PRWriterAgent
from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


class PRCreator:
    """Create pull requests with workflow improvements"""
    
    def __init__(self):
        self.client = GitHubClient()
        self.pr_writer = PRWriterAgent()
    
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
            # TODO: Retrieve fix data from storage
            fix_data = {
                "changes": ["Optimized caching strategy", "Parallelized test jobs"],
                "improvements": {"time_saved": "25m", "efficiency_gain": "62%"}
            }
            
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
                logger.warning(f"Branch may already exist: {e}")
                new_ref = repo.get_git_ref(f"heads/{branch}")
            
            # TODO: Commit optimized workflow files to the branch
            # This would involve:
            # 1. Get current workflow file content
            # 2. Update with optimized version
            # 3. Commit changes
            
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
