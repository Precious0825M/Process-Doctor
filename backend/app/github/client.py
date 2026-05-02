"""GitHub API client"""

import logging
from typing import Any, Dict, Optional

from app.config import settings
from github import Github, GithubException

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API client wrapper"""
    
    def __init__(self):
        self.client = Github(settings.github_token)
        self.timeout = settings.github_timeout
    
    def get_repository(self, repo_name: str):
        """
        Get repository object.
        
        Args:
            repo_name: Repository name in format "owner/repo"
        
        Returns:
            Repository object
        """
        try:
            return self.client.get_repo(repo_name)
        except GithubException as e:
            if e.status == 404:
                logger.error(f"Repository not found: {repo_name}")
                raise ValueError(
                    f"Repository '{repo_name}' not found. Please verify:\n"
                    f"1. The repository exists\n"
                    f"2. The repository name is correct (format: owner/repo)\n"
                    f"3. Your GitHub token has access to this repository"
                )
            elif e.status == 401:
                logger.error(f"Authentication failed for repository {repo_name}")
                raise ValueError(
                    f"GitHub authentication failed. Please verify:\n"
                    f"1. Your GITHUB_TOKEN is valid\n"
                    f"2. The token has not expired\n"
                    f"3. The token has 'repo' scope"
                )
            elif e.status == 403:
                logger.error(f"Access forbidden to repository {repo_name}")
                raise ValueError(
                    f"Access denied to repository '{repo_name}'. Please verify:\n"
                    f"1. Your GitHub token has access to this repository\n"
                    f"2. The repository is not private (or token has private repo access)\n"
                    f"3. The token has 'repo' scope"
                )
            else:
                logger.error(f"Failed to get repository {repo_name}: {e}")
                raise ValueError(f"GitHub API error: {e.data.get('message', str(e))}")
    
    def get_workflow_file(self, repo_name: str, workflow_path: str) -> str:
        """
        Get workflow file content.
        
        Args:
            repo_name: Repository name
            workflow_path: Path to workflow file
        
        Returns:
            Workflow file content
        """
        try:
            repo = self.get_repository(repo_name)
            content = repo.get_contents(workflow_path)
            return content.decoded_content.decode('utf-8')
        except GithubException as e:
            logger.error(f"Failed to get workflow file: {e}")
            raise
    
    def list_workflows(self, repo_name: str) -> list:
        """
        List all workflows in repository.
        
        Args:
            repo_name: Repository name
        
        Returns:
            List of workflow files
        """
        try:
            repo = self.get_repository(repo_name)
            workflows_path = ".github/workflows"
            contents = repo.get_contents(workflows_path)
            return [item.path for item in contents if item.path.endswith(('.yml', '.yaml'))]
        except GithubException as e:
            logger.error(f"Failed to list workflows: {e}")
            return []

# Made with Bob
