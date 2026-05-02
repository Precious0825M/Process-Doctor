"""Workflow diagnoser agent"""

import logging
from typing import Any, Dict

from app.agents.llm_client import BobClient
from app.config import settings

logger = logging.getLogger(__name__)


class DiagnoserAgent:
    """AI agent for diagnosing workflow issues"""
    
    def __init__(self):
        self.client = BobClient() if not settings.use_mock_mode else None
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
        logger.info(f"Workflow data keys: {list(workflow_data.keys())}")
        logger.info(f"Workflow source: {workflow_data.get('source')}")
        
        # Use mock mode for development
        if settings.use_mock_mode:
            logger.info("Using mock diagnosis (USE_MOCK_MODE=true)")
            return self._get_mock_diagnosis(workflow_data)
        
        # Build prompt
        prompt = self._build_prompt(workflow_data, static_results)
        logger.info(f"=== PROMPT TO AI MODEL ===")
        logger.info(f"Prompt length: {len(prompt)} characters")
        logger.info(f"Prompt preview: {prompt[:500]}...")
        logger.info(f"=========================")
        
        # Get AI response
        logger.info("Calling AI model...")
        response = await self.client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=0.3
        )
        
        logger.info(f"=== AI MODEL RESPONSE ===")
        logger.info(f"Response length: {len(response)} characters")
        logger.info(f"Response: {response}")
        logger.info(f"========================")
        
        # Parse response
        diagnosis = self._parse_response(response)
        logger.info(f"Parsed diagnosis with {len(diagnosis.get('bottlenecks', []))} bottlenecks")
        
        return diagnosis
    
    def _build_prompt(
        self,
        workflow_data: Dict[str, Any],
        static_results: Dict[str, Any]
    ) -> str:
        """Build diagnosis prompt"""
        workflow_desc = workflow_data.get('description') or workflow_data.get('content') or str(workflow_data)
        
        prompt = f"""
Analyze the following CI/CD workflow and identify bottlenecks and optimization opportunities.

Workflow Information:
{workflow_desc}

Static Analysis:
{static_results}

Please provide a comprehensive analysis including:
1. Current workflow duration estimate (e.g., "45 minutes", "1.5 hours")
2. Optimal workflow duration after fixes (e.g., "18 minutes", "30 minutes")
3. Efficiency score (0-100, where 100 is optimal)
4. List of bottlenecks with severity (critical/medium/low)
5. Impact of each bottleneck
6. Specific recommendations to fix each issue
7. Workflow structure showing jobs and their dependencies

Format your response as JSON with this EXACT structure:
{{
  "current_duration": "45 minutes",
  "estimated_optimal": "18 minutes",
  "efficiency_score": 40,
  "bottlenecks": [
    {{
      "id": "unique-id",
      "label": "Short description",
      "severity": "critical|medium|low",
      "impact": "Description of impact",
      "fix": "How to fix it"
    }}
  ],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "estimated_improvement": "60%",
  "workflow_structure": {{
    "jobs": [
      {{
        "name": "job-name",
        "duration": "5 minutes",
        "dependencies": ["job1", "job2"],
        "parallel": true
      }}
    ]
  }}
}}

IMPORTANT:
- Provide realistic time estimates based on the workflow complexity
- current_duration should reflect the actual workflow execution time
- estimated_optimal should be achievable after applying your recommendations
- Include all fields in your response
"""
        logger.debug(f"Built prompt with {len(prompt)} characters")
        return prompt
    
    def _get_mock_diagnosis(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return mock diagnosis for development"""
        return {
            "bottlenecks": [
                {
                    "id": "sequential-tests",
                    "label": "Sequential test execution",
                    "severity": "critical",
                    "impact": "Tests run one after another, adding 15+ minutes to each build",
                    "fix": "Parallelize test suites across multiple runners"
                },
                {
                    "id": "no-caching",
                    "label": "Missing dependency caching",
                    "severity": "medium",
                    "impact": "Dependencies downloaded on every run, wasting 5-8 minutes",
                    "fix": "Implement GitHub Actions cache for node_modules and pip packages"
                },
                {
                    "id": "manual-approval",
                    "label": "Manual deployment approval",
                    "severity": "medium",
                    "impact": "Deployments blocked waiting for human approval, average 2-hour delay",
                    "fix": "Automate deployment to staging, require approval only for production"
                }
            ],
            "current_duration": "40 minutes",
            "estimated_optimal": "15 minutes",
            "efficiency_score": 45,
            "recommendations": [
                "Parallelize test execution across 4 runners",
                "Add dependency caching for faster builds",
                "Automate staging deployments",
                "Use matrix strategy for multi-platform testing"
            ],
            "estimated_improvement": "62%"
        }
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        import json
        import re
        
        try:
            # Try to extract JSON from response
            # Look for JSON object in the response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                parsed = json.loads(json_match.group())
                
                # Ensure bottlenecks have required fields
                bottlenecks = parsed.get("bottlenecks", [])
                for i, bottleneck in enumerate(bottlenecks):
                    # Add id if missing
                    if "id" not in bottleneck:
                        bottleneck["id"] = f"bottleneck-{i+1}"
                    # Ensure all required fields exist
                    bottleneck.setdefault("label", "Unnamed bottleneck")
                    bottleneck.setdefault("severity", "medium")
                    bottleneck.setdefault("impact", "No impact description provided")
                    bottleneck.setdefault("fix", "No fix recommendation provided")
                
                logger.info(f"Successfully parsed {len(bottlenecks)} bottlenecks from AI response")
                
                # Extract workflow structure if provided
                workflow_structure = parsed.get("workflow_structure", {})
                
                result = {
                    "bottlenecks": bottlenecks,
                    "current_duration": parsed.get("current_duration", "Unknown"),
                    "estimated_optimal": parsed.get("estimated_optimal", "Unknown"),
                    "efficiency_score": parsed.get("efficiency_score", 0),
                    "recommendations": parsed.get("recommendations", []),
                    "estimated_improvement": parsed.get("estimated_improvement", "0%"),
                    "workflow_structure": workflow_structure
                }
                
                logger.info(f"Parsed metrics - Duration: {result['current_duration']} -> {result['estimated_optimal']}, Score: {result['efficiency_score']}%")
                
                return result
            else:
                logger.warning("No JSON found in AI response, returning empty diagnosis")
                return {
                    "bottlenecks": [],
                    "current_duration": "Unknown",
                    "estimated_optimal": "Unknown",
                    "efficiency_score": 0,
                    "recommendations": [],
                    "estimated_improvement": "0%"
                }
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response was: {response[:500]}...")
            # Return empty diagnosis on parse error
            return {
                "bottlenecks": [],
                "current_duration": "Unknown",
                "estimated_optimal": "Unknown",
                "efficiency_score": 0,
                "recommendations": [],
                "estimated_improvement": "0%"
            }
        except Exception as e:
            logger.error(f"Unexpected error parsing AI response: {e}")
            return {
                "bottlenecks": [],
                "current_duration": "Unknown",
                "estimated_optimal": "Unknown",
                "efficiency_score": 0,
                "recommendations": [],
                "estimated_improvement": "0%"
            }

# Made with Bob
