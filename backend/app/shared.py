"""Shared singleton instances for the application"""

from app.github.pr_creator import PRCreator
from app.pipeline.orchestrator import WorkflowOrchestrator

# Singleton instances shared across all API endpoints
# This ensures data persists across API calls within the same application instance
orchestrator = WorkflowOrchestrator()
pr_creator = PRCreator()

# Made with Bob
