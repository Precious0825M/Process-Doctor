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
            logger.error(f"Failed to get repository {repo_name}: {e}")
            raise
    
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
