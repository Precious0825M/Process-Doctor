"""Workflow diagnoser agent"""

import logging
from typing import Any, Dict

from app.agents.llm_client import BobClient

logger = logging.getLogger(__name__)


class DiagnoserAgent:
    """AI agent for diagnosing workflow issues"""
    
    def __init__(self):
        self.client = BobClient()
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load diagnoser system prompt"""
        try:
            with open("app/prompts/diagnoser_system.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Diagnoser system prompt not found, using default")
            return "You are a workflow analysis expert."
    
    async def diagnose(
        self,
        workflow_data: Dict[str, Any],
        static_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Diagnose workflow issues using AI.
        
        Args:
            workflow_data: Normalized workflow data
            static_results: Static analysis results
        
        Returns:
            Diagnosis with bottlenecks and recommendations
        """
        logger.info("Running AI diagnosis")
        
        # Build prompt
        prompt = self._build_prompt(workflow_data, static_results)
        
        # Get AI response
        response = await self.client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=0.3
        )
        
        # Parse response
        diagnosis = self._parse_response(response)
        
        return diagnosis
    
    def _build_prompt(
        self,
        workflow_data: Dict[str, Any],
        static_results: Dict[str, Any]
    ) -> str:
        """Build diagnosis prompt"""
        return f"""
Analyze the following workflow:

Workflow Data:
{workflow_data}

Static Analysis Results:
{static_results}

Identify bottlenecks, inefficiencies, and provide recommendations.
"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        # TODO: Implement proper response parsing
        return {
            "bottlenecks": [],
            "current_duration": "40m",
            "estimated_optimal": "15m",
            "efficiency_score": 45,
            "recommendations": [],
            "estimated_improvement": "62%"
        }

# Made with Bob
