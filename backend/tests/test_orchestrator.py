"""Tests for orchestrator module"""

import pytest
from app.pipeline.orchestrator import WorkflowOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator can be initialized"""
    orchestrator = WorkflowOrchestrator()
    assert orchestrator is not None
    assert orchestrator.ingestion is not None
    assert orchestrator.static_analyzer is not None
    assert orchestrator.diagnoser is not None
    assert orchestrator.fixer is not None
    assert orchestrator.validator is not None


@pytest.mark.asyncio
async def test_analyze_workflow():
    """Test workflow analysis orchestration"""
    orchestrator = WorkflowOrchestrator()
    
    result = await orchestrator.analyze_workflow(
        workflow_input="test workflow",
        source_type="text",
        analysis_id="test-123"
    )
    
    assert "workflow_structure" in result
    assert "bottlenecks" in result
    assert "metrics" in result
    assert "recommendations" in result
    assert "estimated_improvement" in result


@pytest.mark.asyncio
async def test_generate_fix():
    """Test fix generation orchestration"""
    orchestrator = WorkflowOrchestrator()
    
    result = await orchestrator.generate_fix(
        analysis_id="test-123",
        optimization_strategy="balanced",
        fix_id="fix-456"
    )
    
    assert "optimized_workflow" in result
    assert "changes" in result
    assert "improvements" in result
    assert "diff" in result

# Made with Bob
