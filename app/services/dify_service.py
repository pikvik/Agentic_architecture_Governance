"""
Enhanced Dify service for integration with hosted Dify platform
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


class DifyService:
    """Service for interacting with hosted Dify platform"""
    
    def __init__(self):
        self.api_key = settings.dify_api_key
        self.base_url = settings.dify_base_url
        self.workspace_id = settings.dify_workspace_id
        self.app_id = settings.dify_app_id
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def health_check(self) -> bool:
        """Check if Dify service is accessible"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/workspaces",
                    headers=self.headers,
                    timeout=10
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Dify health check failed: {e}")
            return False
    
    async def list_workspaces(self) -> List[Dict[str, Any]]:
        """List available workspaces"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/workspaces",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        logger.error(f"Failed to list workspaces: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error listing workspaces: {e}")
            return []
    
    async def list_applications(self, workspace_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List applications in a workspace"""
        try:
            workspace_id = workspace_id or self.workspace_id
            if not workspace_id:
                logger.error("No workspace ID provided")
                return []
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/workspaces/{workspace_id}/applications",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        logger.error(f"Failed to list applications: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Error listing applications: {e}")
            return []
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Chat completion using Dify"""
        try:
            app_id = app_id or self.app_id
            if not app_id:
                return {
                    "success": False,
                    "error": "No app ID provided"
                }
            
            payload = {
                "inputs": inputs or {},
                "query": messages[-1].get("content", "") if messages else "",
                "response_mode": "blocking",
                "user": user_id or "default_user"
            }
            
            if conversation_id:
                payload["conversation_id"] = conversation_id
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat-messages",
                    headers=self.headers,
                    json=payload,
                    params={"app_id": app_id}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "message": {
                                "role": "assistant",
                                "content": data.get("answer", "")
                            },
                            "conversation_id": data.get("conversation_id"),
                            "message_id": data.get("id"),
                            "usage": data.get("usage", {}),
                            "created_at": datetime.utcnow().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Dify chat failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Chat failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error with Dify chat: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def completion(
        self,
        prompt: str,
        app_id: Optional[str] = None,
        user_id: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Text completion using Dify"""
        try:
            app_id = app_id or self.app_id
            if not app_id:
                return {
                    "success": False,
                    "error": "No app ID provided"
                }
            
            payload = {
                "inputs": inputs or {},
                "query": prompt,
                "response_mode": "blocking",
                "user": user_id or "default_user"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/completion-messages",
                    headers=self.headers,
                    json=payload,
                    params={"app_id": app_id}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "text": data.get("answer", ""),
                            "message_id": data.get("id"),
                            "usage": data.get("usage", {}),
                            "created_at": datetime.utcnow().isoformat()
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Dify completion failed: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Completion failed: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error with Dify completion: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_conversation_history(
        self,
        conversation_id: str,
        app_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get conversation history"""
        try:
            app_id = app_id or self.app_id
            if not app_id:
                return {
                    "success": False,
                    "error": "No app ID provided"
                }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/conversations/{conversation_id}/messages",
                    headers=self.headers,
                    params={"app_id": app_id}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "messages": data.get("data", []),
                            "conversation_id": conversation_id
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to get conversation history: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Failed to get history: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_workflow(
        self,
        name: str,
        description: str,
        workflow_data: Dict[str, Any],
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new workflow in Dify"""
        try:
            workspace_id = workspace_id or self.workspace_id
            if not workspace_id:
                return {
                    "success": False,
                    "error": "No workspace ID provided"
                }
            
            payload = {
                "name": name,
                "description": description,
                "workflow_data": workflow_data
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/workspaces/{workspace_id}/workflows",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "workflow_id": data.get("id"),
                            "workflow": data
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create workflow: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Failed to create workflow: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_workflow(
        self,
        workflow_id: str,
        inputs: Dict[str, Any],
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a workflow"""
        try:
            workspace_id = workspace_id or self.workspace_id
            if not workspace_id:
                return {
                    "success": False,
                    "error": "No workspace ID provided"
                }
            
            payload = {
                "inputs": inputs
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/workspaces/{workspace_id}/workflows/{workflow_id}/execute",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "outputs": data.get("outputs", {}),
                            "execution_id": data.get("execution_id")
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to execute workflow: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Failed to execute workflow: {response.status}",
                            "details": error_text
                        }
                        
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global Dify service instance
dify_service = DifyService()
