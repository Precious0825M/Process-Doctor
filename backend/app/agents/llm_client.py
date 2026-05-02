"""LLM client wrapper for IBM Granite and Bob"""

import logging
from typing import Any, Dict, Optional

import httpx
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Base LLM client for API interactions"""
    
    def __init__(self, api_key: str, api_url: str, timeout: int = 120):
        self.api_key = api_key
        self.api_url = api_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated text
        """
        # TODO: Implement actual API call
        logger.info("Generating LLM response")
        return "Generated response"
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class GraniteClient(LLMClient):
    """IBM Granite API client"""
    
    def __init__(self):
        super().__init__(
            api_key=settings.granite_api_key,
            api_url=settings.granite_api_url,
            timeout=settings.llm_timeout
        )


class BobClient(LLMClient):
    """IBM Bob API client"""
    
    def __init__(self):
        super().__init__(
            api_key=settings.bob_api_key,
            api_url=settings.bob_api_url,
            timeout=settings.llm_timeout
        )

# Made with Bob
