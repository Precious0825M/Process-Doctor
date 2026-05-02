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
        # ValueError is raised for user-facing errors (repo not found, auth issues, etc.)
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_trace = traceback.format_exc()
        print(f"PR creation error:\n{error_trace}")
        
        # Return user-friendly error
        error_message = str(e)
        if "404" in error_message or "Not Found" in error_message:
            error_message = (
                "Repository not found or inaccessible. Please verify:\n"
                "1. The repository exists and the name is correct (format: owner/repo)\n"
                "2. Your GitHub token has access to this repository\n"
                "3. The repository is not private (or your token has private repo access)"
            )
        elif "401" in error_message or "Unauthorized" in error_message:
            error_message = (
                "GitHub authentication failed. Please verify:\n"
                "1. Your GITHUB_TOKEN environment variable is set correctly\n"
                "2. The token has not expired\n"
                "3. The token has 'repo' scope permissions"
            )
        elif "403" in error_message or "Forbidden" in error_message:
            error_message = (
                "Access denied. Please verify:\n"
                "1. Your GitHub token has write access to this repository\n"
                "2. The token has 'repo' scope permissions\n"
                "3. You are not rate limited by GitHub API"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PR creation failed: {error_message}"
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
