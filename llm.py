import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class LLMProvider:
    """Abstract base class for LLM providers"""
    def __init__(self):
        self.model = self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the LLM model/client - to be implemented by specific providers"""
        raise NotImplementedError
        
    def get_response(self, message: str, context: Optional[list] = None) -> str:
        """Get response from LLM - to be implemented by specific providers"""
        raise NotImplementedError

class ClaudeLLM(LLMProvider):
    """Claude-specific implementation"""
    def _initialize_model(self):
        try:
            from anthropic import Anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
            return Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Please install anthropic package: pip install anthropic")
    
    def get_response(self, message: str, context: Optional[list] = None) -> str:
        try:
            messages = []
            if context:
                for msg in context:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": message})
            
            response = self.model.messages.create(
                model="claude-3-opus-20240229",
                messages=messages,
                max_tokens=1024
            )
            return response.content[0].text
        except Exception as e:
            return f"Error getting response from Claude: {str(e)}"

def get_llm_provider() -> LLMProvider:
    """Factory function to get the configured LLM provider"""
    return ClaudeLLM()
