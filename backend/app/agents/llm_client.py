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
        logger.info(f"Generating LLM response (temp={temperature}, max_tokens={max_tokens})")
        
        try:
            # Prepare request payload
            payload = {
                "model": getattr(settings, "granite_model", "granite-13b-chat-v2"),
                "messages": [],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Add system prompt if provided
            if system_prompt:
                payload["messages"].append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user prompt
            payload["messages"].append({
                "role": "user",
                "content": prompt
            })
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract generated text
            if "choices" in result and len(result["choices"]) > 0:
                generated_text = result["choices"][0]["message"]["content"]
                logger.info(f"Successfully generated {len(generated_text)} characters")
                return generated_text
            else:
                raise ValueError("No response generated from LLM")
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during LLM generation: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"LLM API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error during LLM generation: {str(e)}")
            raise
    
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
