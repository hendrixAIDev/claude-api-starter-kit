"""
Claude API Client Wrapper
Provides a simple interface to the Anthropic API with built-in error handling.
"""

import os
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from .error_handler import handle_api_errors


class ClaudeClient:
    """Wrapper around the Anthropic API client with convenience methods."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Claude client.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use (default: claude-sonnet-4-20250514)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
    
    @handle_api_errors
    def chat(
        self,
        message: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> str:
        """
        Send a single chat message and get a response.
        
        Args:
            message: User message to send
            system: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            str: Claude's response text
        """
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": message}]
        }
        
        if system:
            params["system"] = system
            
        params.update(kwargs)
        
        response = self.client.messages.create(**params)
        return response.content[0].text
    
    @handle_api_errors
    def chat_stream(
        self,
        message: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ):
        """
        Send a chat message and stream the response.
        
        Args:
            message: User message to send
            system: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            **kwargs: Additional arguments to pass to the API
            
        Yields:
            str: Chunks of Claude's response
        """
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": message}]
        }
        
        if system:
            params["system"] = system
            
        params.update(kwargs)
        
        with self.client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                yield text
    
    @handle_api_errors
    def multi_turn_chat(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        **kwargs
    ) -> str:
        """
        Send a multi-turn conversation and get a response.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            system: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            **kwargs: Additional arguments to pass to the API
            
        Returns:
            str: Claude's response text
        """
        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }
        
        if system:
            params["system"] = system
            
        params.update(kwargs)
        
        response = self.client.messages.create(**params)
        return response.content[0].text
