"""Workflow data schemas"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowJob(BaseModel):
    """Schema for a workflow job"""
    name: str = Field(..., description="Job name")
    steps: List[str] = Field(default_factory=list, description="Job steps")
    dependencies: List[str] = Field(default_factory=list, description="Job dependencies")
    estimated_duration: Optional[str] = Field(None, description="Estimated duration")
    parallelizable: bool = Field(default=False, description="Can run in parallel")


class WorkflowStructure(BaseModel):
    """Schema for workflow structure"""
    name: str = Field(..., description="Workflow name")
    triggers: List[str] = Field(default_factory=list, description="Workflow triggers")
    jobs: List[WorkflowJob] = Field(default_factory=list, description="Workflow jobs")
    overall_structure: str = Field(..., description="Overall structure type")
    critical_path: List[str] = Field(default_factory=list, description="Critical path jobs")

# Made with Bob
