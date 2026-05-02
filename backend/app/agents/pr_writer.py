"""PR description writer agent"""

import logging
from typing import Any, Dict

from app.agents.llm_client import GraniteClient

logger = logging.getLogger(__name__)


class PRWriterAgent:
    """AI agent for generating PR descriptions"""
    
    def __init__(self):
        self.client = GraniteClient()
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load PR writer system prompt"""
        try:
            with open("app/prompts/pr_writer_system.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("PR writer system prompt not found, using default")
            return "You are a technical writer for pull requests."
    
    async def generate_pr_description(
        self,
        fix_data: Dict[str, Any]
    ) -> str:
        """
        Generate PR description.
        
        Args:
            fix_data: Fix data with changes and improvements
        
        Returns:
            PR description markdown
        """
        logger.info("Generating PR description")
        
        # Build prompt
        prompt = self._build_prompt(fix_data)
        
        # Get AI response
        description = await self.client.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=0.3
        )
        
        return description
    
    def _build_prompt(self, fix_data: Dict[str, Any]) -> str:
        """Build PR description prompt"""
        return f"""
Generate a comprehensive pull request description for workflow optimizations.

Changes:
{fix_data.get('changes', [])}

Improvements:
{fix_data.get('improvements', {})}

Include:
- Summary
- Detailed changes
- Performance improvements
- Testing recommendations
"""

# Made with Bob
