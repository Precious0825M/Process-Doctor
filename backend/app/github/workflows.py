"""GitHub workflows operations"""

import logging
from typing import Any, Dict, List

from app.github.client import GitHubClient

logger = logging.getLogger(__name__)


class WorkflowOperations:
    """Operations for GitHub workflows"""
    
    def __init__(self):
        self.client = GitHubClient()
    
    async def fetch_workflows(self, repo_name: str) -> List[Dict[str, Any]]:
        """
        Fetch all workflows from repository.
        
        Args:
            repo_name: Repository name
        
        Returns:
            List of workflows with content
        """
        logger.info(f"Fetching workflows from {repo_name}")
        
        workflow_paths = self.client.list_workflows(repo_name)
        workflows = []
        
        for path in workflow_paths:
            try:
                content = self.client.get_workflow_file(repo_name, path)
                workflows.append({
                    "path": path,
                    "content": content
                })
            except Exception as e:
                logger.error(f"Failed to fetch workflow {path}: {e}")
        
        return workflows

# Made with Bob
