"""Tests for static analysis module"""

import pytest
from app.pipeline.static_analysis import StaticAnalyzer


@pytest.mark.asyncio
async def test_static_analyzer_initialization():
    """Test static analyzer can be initialized"""
    analyzer = StaticAnalyzer()
    assert analyzer is not None


@pytest.mark.asyncio
async def test_analyze_workflow():
    """Test workflow analysis"""
    analyzer = StaticAnalyzer()
    
    workflow_data = {
        "source": "test",
        "content": "test workflow",
        "structure": {}
    }
    
    result = await analyzer.analyze(workflow_data)
    
    assert "syntax_valid" in result
    assert "issues" in result
    assert "warnings" in result
    assert "metrics" in result


@pytest.mark.asyncio
async def test_analyze_returns_valid_structure():
    """Test that analysis returns expected structure"""
    analyzer = StaticAnalyzer()
    
    workflow_data = {
        "source": "test",
        "structure": {
            "jobs": []
        }
    }
    
    result = await analyzer.analyze(workflow_data)
    
    assert isinstance(result["syntax_valid"], bool)
    assert isinstance(result["issues"], list)
    assert isinstance(result["warnings"], list)
    assert isinstance(result["metrics"], dict)

# Made with Bob
