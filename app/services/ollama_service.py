"""
Ollama service for local LLM integration
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama local LLM"""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.default_model = settings.ollama_model
        self.timeout = settings.ollama_timeout
        self.temperature = settings.ollama_temperature
        self.max_tokens = settings.ollama_max_tokens
        
    async def health_check(self) -> bool:
        """Check if Ollama is running and healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=5) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("models", [])
                    else:
                        logger.error(f"Failed to list models: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    async def generate_text(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate text using Ollama"""
        try:
            model = model or self.default_model
            temperature = temperature or self.temperature
            max_tokens = max_tokens or self.max_tokens
            
            payload = {
                "model": model,
                "prompt": prompt,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
                "stream": False
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "text": data.get("response", ""),
                            "model": model,
                            "usage": {
                                "prompt_tokens": data.get("prompt_eval_count", 0),
                                "completion_tokens": data.get("eval_count", 0),
                                "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                            },
                            "finish_reason": data.get("done", True),
                            "created_at": datetime.utcnow().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama generation failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Generation failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Chat completion using Ollama"""
        try:
            model = model or self.default_model
            temperature = temperature or self.temperature
            max_tokens = max_tokens or self.max_tokens
            
            # Convert messages to Ollama format
            ollama_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    # System messages are handled separately in Ollama
                    continue
                elif role == "assistant":
                    ollama_messages.append({"role": "assistant", "content": content})
                else:
                    ollama_messages.append({"role": "user", "content": content})
            
            # Extract system message if present
            system_message = None
            for msg in messages:
                if msg.get("role") == "system":
                    system_message = msg.get("content")
                    break
            
            payload = {
                "model": model,
                "messages": ollama_messages,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
                "stream": False
            }
            
            if system_message:
                payload["system"] = system_message
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "message": {
                                "role": "assistant",
                                "content": data.get("message", {}).get("content", "")
                            },
                            "model": model,
                            "usage": {
                                "prompt_tokens": data.get("prompt_eval_count", 0),
                                "completion_tokens": data.get("eval_count", 0),
                                "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                            },
                            "finish_reason": data.get("done", True),
                            "created_at": datetime.utcnow().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama chat failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Chat failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error with Ollama chat: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def embed_text(self, text: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Generate embeddings using Ollama"""
        try:
            model = model or self.default_model
            
            payload = {
                "model": model,
                "prompt": text
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                    timeout=self.timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "embeddings": data.get("embedding", []),
                            "model": model
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama embedding failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Embedding failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error generating embeddings with Ollama: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def pull_model(self, model: str) -> Dict[str, Any]:
        """Pull a model from Ollama"""
        try:
            payload = {
                "name": model
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/pull",
                    json=payload,
                    timeout=300  # Longer timeout for model pulling
                ) as response:
                    if response.status == 200:
                        return {
                            "success": True,
                            "model": model,
                            "message": "Model pulled successfully"
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Model pull failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Model pull failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error pulling model: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global Ollama service instance
ollama_service = OllamaService()
