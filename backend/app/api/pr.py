"""Pull request creation endpoint"""

from typing import Any, Dict

from app.schemas.api import PRRequest, PRResponse
from app.shared import orchestrator, pr_creator
from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["github"])


@router.post(
    "/pr",
    status_code=status.HTTP_201_CREATED,
    response_model=PRResponse,
    summary="Create pull request with optimized workflow"
)
async def create_pull_request(request: PRRequest) -> PRResponse:
    """
    Create a GitHub pull request with the optimized workflow.
    
    Args:
        request: PR request containing fix ID, repository, and branch info
    
    Returns:
        Created pull request information
    
    Raises:
        HTTPException: If PR creation fails
    """
    try:
        # Get fix data from orchestrator cache
        fix_data = orchestrator._fix_cache.get(request.fix_id)
        if not fix_data:
            raise ValueError(f"Fix data not found for fix_id: {request.fix_id}")
        
        # Store fix data in PR creator cache
        pr_creator.store_fix_data(request.fix_id, fix_data)
        
        # Create pull request
        result = await pr_creator.create_pr(
            fix_id=request.fix_id,
            repository=request.repository,
            branch=request.branch,
            title=request.title,
            description=request.description
        )
        
        return PRResponse(
            pr_number=result.get("pr_number", 0),
            pr_url=result.get("pr_url", ""),
            branch=result.get("branch", ""),
            status="created",
            message="Pull request created successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PR creation failed: {str(e)}"
        )


@router.get(
    "/pr/{repository}/{pr_number}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Get pull request status"
)
async def get_pr_status(repository: str, pr_number: int) -> Dict[str, Any]:
    """
    Get the status of a pull request.
    
    Args:
        repository: Repository in format "owner/repo"
        pr_number: Pull request number
    
    Returns:
        Pull request status information
    
    Raises:
        HTTPException: If PR not found
    """
    try:
        status_info = await pr_creator.get_pr_status(repository, pr_number)
        return status_info
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PR not found: {str(e)}"
        )

# Made with Bob
