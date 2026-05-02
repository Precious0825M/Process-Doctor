"""API request and response schemas"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request schema for workflow analysis"""
    workflow_input: str = Field(..., description="Workflow content or repository URL")
    source_type: str = Field(..., description="Input source type: text, github, or file")


class AnalyzeResponse(BaseModel):
    """Response schema for workflow analysis"""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    status: str = Field(..., description="Analysis status")
    workflow_structure: Optional[Dict[str, Any]] = Field(None, description="Workflow structure")
    bottlenecks: List[Dict[str, Any]] = Field(default_factory=list, description="Identified bottlenecks")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    recommendations: List[str] = Field(default_factory=list, description="Optimization recommendations")
    estimated_improvement: str = Field(..., description="Estimated improvement percentage")


class FixRequest(BaseModel):
    """Request schema for workflow optimization"""
    analysis_id: str = Field(..., description="Analysis identifier")
    optimization_strategy: str = Field(
        default="balanced",
        description="Optimization strategy: aggressive, balanced, or conservative"
    )


class FixResponse(BaseModel):
    """Response schema for workflow optimization"""
    fix_id: str = Field(..., description="Unique fix identifier")
    analysis_id: str = Field(..., description="Related analysis identifier")
    status: str = Field(..., description="Fix generation status")
    optimized_workflow: Optional[Dict[str, Any]] = Field(None, description="Optimized workflow configuration")
    changes: List[Dict[str, Any]] = Field(default_factory=list, description="List of changes made")
    improvements: Dict[str, Any] = Field(default_factory=dict, description="Performance improvements")
    diff: str = Field(default="", description="Diff of changes")


class PRRequest(BaseModel):
    """Request schema for PR creation"""
    fix_id: str = Field(..., description="Fix identifier")
    repository: str = Field(..., description="Repository name in format 'owner/repo'")
    branch: str = Field(default="optimization/workflow-improvements", description="Branch name for PR")
    title: Optional[str] = Field(None, description="PR title")
    description: Optional[str] = Field(None, description="PR description")


class PRResponse(BaseModel):
    """Response schema for PR creation"""
    pr_number: int = Field(..., description="Pull request number")
    pr_url: str = Field(..., description="Pull request URL")
    branch: str = Field(..., description="Branch name")
    status: str = Field(..., description="PR creation status")
    message: str = Field(..., description="Status message")

# Made with Bob
