"""watsonx Orchestrate client for workflow deployment"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from app.config import settings

logger = logging.getLogger(__name__)


class DeploymentStatus(str, Enum):
    """Deployment status enum"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class WorkflowStep:
    """Represents a single workflow deployment step"""
    
    def __init__(self, name: str, action: str, params: Dict[str, Any]):
        self.name = name
        self.action = action
        self.params = params
        self.status = DeploymentStatus.PENDING
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None


class OrchestrateClient:
    """Client for IBM watsonx Orchestrate API"""
    
    def __init__(self):
        self.api_key = settings.watsonx_orchestrate_api_key
        self.api_url = settings.watsonx_orchestrate_url
        self.timeout = settings.llm_timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def execute_workflow(
        self,
        workflow_id: str,
        steps: List[WorkflowStep],
        rollback_on_failure: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a multi-step workflow deployment.
        
        Args:
            workflow_id: Unique workflow identifier
            steps: List of workflow steps to execute
            rollback_on_failure: Whether to rollback on failure
        
        Returns:
            Execution results
        """
        logger.info(f"Executing workflow {workflow_id} with {len(steps)} steps")
        
        execution_id = f"exec-{workflow_id}"
        completed_steps = []
        
        try:
            for i, step in enumerate(steps):
                logger.info(f"Executing step {i+1}/{len(steps)}: {step.name}")
                
                step.status = DeploymentStatus.IN_PROGRESS
                
                try:
                    # Execute step
                    result = await self._execute_step(step)
                    step.result = result
                    step.status = DeploymentStatus.COMPLETED
                    completed_steps.append(step)
                    
                    logger.info(f"Step {step.name} completed successfully")
                    
                except Exception as e:
                    step.error = str(e)
                    step.status = DeploymentStatus.FAILED
                    logger.error(f"Step {step.name} failed: {e}")
                    
                    if rollback_on_failure:
                        logger.warning("Rolling back completed steps...")
                        await self._rollback_steps(completed_steps)
                    
                    raise
            
            return {
                "execution_id": execution_id,
                "status": DeploymentStatus.COMPLETED,
                "steps_completed": len(completed_steps),
                "total_steps": len(steps),
                "results": [step.result for step in steps]
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "execution_id": execution_id,
                "status": DeploymentStatus.FAILED,
                "steps_completed": len(completed_steps),
                "total_steps": len(steps),
                "error": str(e)
            }
    
    async def _execute_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """
        Execute a single workflow step.
        
        Args:
            step: Workflow step to execute
        
        Returns:
            Step execution result
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "action": step.action,
            "parameters": step.params
        }
        
        try:
            response = await self.client.post(
                f"{self.api_url}/execute",
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "step_name": step.name,
                "action": step.action,
                "status": "success",
                "data": result
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error executing step: {e.response.status_code}")
            raise ValueError(f"Step execution failed: {e.response.text}")
        except Exception as e:
            logger.error(f"Error executing step: {e}")
            raise
    
    async def _rollback_steps(self, steps: List[WorkflowStep]) -> None:
        """
        Rollback completed steps in reverse order.
        
        Args:
            steps: List of completed steps to rollback
        """
        logger.info(f"Rolling back {len(steps)} steps")
        
        for step in reversed(steps):
            try:
                logger.info(f"Rolling back step: {step.name}")
                
                # Execute rollback action
                rollback_params = step.params.copy()
                rollback_params["rollback"] = True
                
                rollback_step = WorkflowStep(
                    name=f"rollback-{step.name}",
                    action=f"rollback-{step.action}",
                    params=rollback_params
                )
                
                await self._execute_step(rollback_step)
                step.status = DeploymentStatus.ROLLED_BACK
                
                logger.info(f"Successfully rolled back: {step.name}")
                
            except Exception as e:
                logger.error(f"Failed to rollback step {step.name}: {e}")
                # Continue with other rollbacks even if one fails
    
    async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution.
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Execution status information
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = await self.client.get(
                f"{self.api_url}/executions/{execution_id}",
                headers=headers
            )
            
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to get execution status: {e}")
            raise
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Helper function to create deployment steps
def create_deployment_steps(
    optimized_workflow: Dict[str, Any],
    repository: str,
    branch: str
) -> List[WorkflowStep]:
    """
    Create deployment steps for workflow optimization.
    
    Args:
        optimized_workflow: Optimized workflow configuration
        repository: Target repository
        branch: Target branch
    
    Returns:
        List of workflow steps
    """
    steps = [
        WorkflowStep(
            name="validate-workflow",
            action="validate",
            params={
                "workflow": optimized_workflow,
                "strict": True
            }
        ),
        WorkflowStep(
            name="backup-current-workflow",
            action="backup",
            params={
                "repository": repository,
                "branch": branch,
                "path": ".github/workflows"
            }
        ),
        WorkflowStep(
            name="deploy-optimized-workflow",
            action="deploy",
            params={
                "workflow": optimized_workflow,
                "repository": repository,
                "branch": branch
            }
        ),
        WorkflowStep(
            name="verify-deployment",
            action="verify",
            params={
                "repository": repository,
                "branch": branch,
                "run_tests": True
            }
        )
    ]
    
    return steps


# Made with Bob