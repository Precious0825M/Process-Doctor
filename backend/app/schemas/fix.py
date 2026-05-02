"""Fix/optimization schemas"""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class WorkflowChange(BaseModel):
    """Schema for a workflow change"""
    type: str = Field(..., description="Change type")
    description: str = Field(..., description="Change description")
    before: str = Field(..., description="Before state")
    after: str = Field(..., description="After state")
    impact: str = Field(..., description="Expected impact")


class OptimizationImprovements(BaseModel):
    """Schema for optimization improvements"""
    time_saved: str = Field(..., description="Time saved")
    efficiency_gain: str = Field(..., description="Efficiency gain percentage")
    optimizations_applied: int = Field(..., description="Number of optimizations applied")
    cost_reduction: str = Field(default="N/A", description="Estimated cost reduction")

# Made with Bob
