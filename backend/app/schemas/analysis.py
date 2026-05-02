"""Analysis result schemas"""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Bottleneck(BaseModel):
    """Schema for identified bottleneck"""
    type: str = Field(..., description="Bottleneck type")
    severity: str = Field(..., description="Severity level: critical, high, medium, low")
    description: str = Field(..., description="Bottleneck description")
    location: str = Field(..., description="Location in workflow")
    impact: str = Field(..., description="Performance impact")


class AnalysisMetrics(BaseModel):
    """Schema for analysis metrics"""
    current_duration: str = Field(..., description="Current workflow duration")
    estimated_optimal: str = Field(..., description="Estimated optimal duration")
    efficiency_score: float = Field(..., description="Efficiency score (0-100)")
    total_jobs: int = Field(default=0, description="Total number of jobs")
    total_steps: int = Field(default=0, description="Total number of steps")

# Made with Bob
