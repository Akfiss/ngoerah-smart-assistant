"""
LLM Service - Wrapper for Ollama LLM
Handles text generation using Llama 3 model
"""

import logging
from typing import Optional
import ollama

from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Ollama LLM"""
    
    def __init__(self, model: Optional[str] = None, host: Optional[str] = None):
        self.model = model or settings.LLM_MODEL
        self.host = host or settings.OLLAMA_URL
        self.client = ollama.Client(host=self.host)
        logger.info(f"LLM Service initialized with model: {self.model}")
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 512,
        temperature: float = 0.3,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text response from the LLM.
        
        Args:
            prompt: The input prompt for the LLM
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            system_prompt: Optional system prompt to set context
            
        Returns:
            Generated text response
        """
        try:
            options = {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
            
            if system_prompt:
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    system=system_prompt,
                    options=options
                )
            else:
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    options=options
                )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise
    
    def chat(
        self, 
        messages: list[dict],
        max_tokens: int = 512,
        temperature: float = 0.3
    ) -> str:
        """
        Chat-style interaction with the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness
            
        Returns:
            Generated response text
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            )
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"LLM chat error: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test if the LLM connection is working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = self.generate("Say 'OK' if you are working.", max_tokens=10)
            return len(response) > 0
        except Exception as e:
            logger.error(f"LLM connection test failed: {str(e)}")
            return False
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        try:
            return self.client.show(self.model)
        except Exception as e:
            logger.error(f"Failed to get model info: {str(e)}")
            return {"error": str(e)}


# Singleton instance for convenience
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
