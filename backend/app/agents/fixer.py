"""Workflow fixer agent"""

import json
import logging
import re
import yaml
from typing import Any, Dict, Optional

from app.agents.llm_client import GraniteClient
from app.config import settings

logger = logging.getLogger(__name__)


class FixerAgent:
    """AI agent for generating optimized workflows"""
    
    def __init__(self):
        self.client: Optional[GraniteClient] = GraniteClient() if not settings.use_mock_mode else None
        self.system_prompt = self._load_system_prompt()
        # In-memory storage for workflow data (TODO: replace with Redis/DB)
        self._workflow_cache: Dict[str, Any] = {}
    
    def _load_system_prompt(self) -> str:
        """Load fixer system prompt"""
        try:
            with open("app/prompts/fixer_system.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Fixer system prompt not found, using default")
            return "You are a DevOps optimization expert."
    
    def store_workflow_data(self, analysis_id: str, workflow_data: Dict[str, Any]):
        """Store workflow data for later retrieval"""
        self._workflow_cache[analysis_id] = workflow_data
        logger.info(f"Stored workflow data for analysis {analysis_id}")
    
    async def generate_fix(
        self,
        analysis_id: str,
        strategy: str = "balanced",
        workflow_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate optimized workflow.
        
        Args:
            analysis_id: Analysis identifier
            strategy: Optimization strategy (aggressive, balanced, conservative)
            workflow_data: Original workflow data (optional, will retrieve from cache if not provided)
        
        Returns:
            Optimized workflow and changes
        """
        logger.info(f"Generating fix with {strategy} strategy for analysis {analysis_id}")
        
        # Use mock mode for development
        if settings.use_mock_mode:
            logger.info("Using mock fix generation (USE_MOCK_MODE=true)")
            return self._get_mock_fix(analysis_id, strategy)
        
        # Retrieve workflow data from cache if not provided
        workflow_data_resolved: Dict[str, Any] = workflow_data if workflow_data is not None else self._workflow_cache.get(analysis_id, {})
        
        # Ensure client is available
        if self.client is None:
            raise ValueError("LLM client not initialized. Set USE_MOCK_MODE=false and provide API credentials.")
        
        # Build prompt with actual workflow data
        prompt = self._build_prompt(analysis_id, strategy, workflow_data_resolved)
        
        # Get AI response
        logger.info("Calling LLM to generate optimized workflow...")
        response = await self.client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=0.2,
            max_tokens=3000
        )
        
        # Parse response
        fix = self._parse_response(response, workflow_data_resolved)
        
        return fix
    
    def _build_prompt(self, analysis_id: str, strategy: str, workflow_data: Dict[str, Any]) -> str:
        """Build optimization prompt with actual workflow data"""
        original_workflow = workflow_data.get("workflow", {})
        workflow_yaml = yaml.dump(original_workflow, default_flow_style=False)
        
        return f"""
Optimize the following GitHub Actions workflow using a {strategy} strategy.

ORIGINAL WORKFLOW:
```yaml
{workflow_yaml}
```

OPTIMIZATION STRATEGY: {strategy}
- aggressive: Maximum performance, may require more resources
- balanced: Good performance with reasonable resource usage
- conservative: Minimal changes, focus on safe optimizations

Please provide:
1. The complete optimized workflow in YAML format
2. A list of specific changes made
3. Expected performance improvements

Format your response as JSON:
{{
  "workflow_yaml": "complete optimized workflow as YAML string",
  "changes": [
    {{"type": "optimization_type", "description": "what was changed"}},
    ...
  ],
  "time_saved": "estimated time saved (e.g., '15 minutes')",
  "efficiency_gain": "percentage improvement (e.g., '45%')"
}}
"""
    
    def _get_mock_fix(self, analysis_id: str, strategy: str) -> Dict[str, Any]:
        """Return mock fix for development with proper YAML format"""
        mock_workflow_yaml = """name: Optimized CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version:
          - "18.x"
          - "20.x"
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "${{ matrix.node-version }}"
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: node_modules
          key: "${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}"
          restore-keys: |
            ${{ runner.os }}-node-
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: "matrix.node-version == '20.x'"

  build:
    needs: test
    runs-on: ubuntu-latest
    if: "github.event_name == 'push'"
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: node_modules
          key: "${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}"
      
      - run: npm ci
      - run: npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-output
          path: dist/
"""
        
        # Parse YAML to ensure it's valid
        try:
            workflow_dict = yaml.safe_load(mock_workflow_yaml)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse mock YAML: {e}")
            workflow_dict = {}
        
        return {
            "workflow_yaml": mock_workflow_yaml,
            "workflow": workflow_dict,
            "changes": [
                {
                    "type": "caching",
                    "description": "Added dependency caching to reduce build time by ~3 minutes"
                },
                {
                    "type": "parallelization",
                    "description": "Parallelized tests across Node.js versions 18.x and 20.x"
                },
                {
                    "type": "conditional_execution",
                    "description": "Build job only runs on push events, not pull requests"
                },
                {
                    "type": "version_updates",
                    "description": "Updated actions to latest versions (v4) for better performance"
                }
            ],
            "time_saved": "8 minutes",
            "efficiency_gain": "45%",
            "diff": "--- original.yml\n+++ optimized.yml\n@@ -10,6 +10,12 @@\n+      - name: Cache dependencies\n+        uses: actions/cache@v3\n+        with:\n+          path: node_modules\n+          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}"
        }
    
    def _parse_response(self, response: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                parsed = json.loads(json_match.group())
                
                # Ensure we have workflow_yaml
                workflow_yaml = parsed.get("workflow_yaml", "")
                
                # Parse YAML to dict
                try:
                    workflow_dict = yaml.safe_load(workflow_yaml)
                except yaml.YAMLError as e:
                    logger.error(f"Failed to parse generated YAML: {e}")
                    workflow_dict = {}
                
                return {
                    "workflow_yaml": workflow_yaml,
                    "workflow": workflow_dict,
                    "changes": parsed.get("changes", []),
                    "time_saved": parsed.get("time_saved", "Unknown"),
                    "efficiency_gain": parsed.get("efficiency_gain", "0%"),
                    "diff": self._generate_diff(workflow_data.get("workflow", {}), workflow_dict)
                }
            else:
                logger.warning("Could not extract JSON from LLM response, using fallback")
                return self._get_mock_fix("", "balanced")
                
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            return self._get_mock_fix("", "balanced")
    
    def _generate_diff(self, original: Dict[str, Any], optimized: Dict[str, Any]) -> str:
        """Generate a simple diff between original and optimized workflows"""
        try:
            original_yaml = yaml.dump(original, default_flow_style=False)
            optimized_yaml = yaml.dump(optimized, default_flow_style=False)
            
            # Simple diff representation
            return f"--- original.yml\n+++ optimized.yml\n\nOriginal: {len(original_yaml)} bytes\nOptimized: {len(optimized_yaml)} bytes"
        except Exception as e:
            logger.error(f"Error generating diff: {e}")
            return "Diff generation failed"

# Made with Bob
