"""
Base Agent class for the Agentic AI Swarm system
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from uuid import uuid4

from app.config import settings
from app.models.agents import Agent, AgentStatus, AgentType, AgentTask
from app.models.governance import ValidationResult, ValidationStatus, ValidationSeverity


class BaseAgent(ABC):
    """Base class for all AI agents in the swarm"""
    
    def __init__(self, agent_type: AgentType, name: str, description: str):
        self.agent_id = str(uuid4())
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.status = AgentStatus.INITIALIZING
        self.logger = logging.getLogger(f"agent.{self.name}")
        
        # Performance tracking
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.average_response_time = 0.0
        self.last_activity = None
        
        # Configuration
        self.config = {}
        self.llm_provider = settings.openai_api_key and "openai" or "anthropic"
        self.model_name = "gpt-4" if self.llm_provider == "openai" else "claude-3-sonnet"
        
        # Health monitoring
        self.health_score = 100.0
        self.error_count = 0
        self.last_error = None
        
        # Task management
        self.current_task: Optional[AgentTask] = None
        self.task_queue: List[AgentTask] = []
        
        self.logger.info(f"Initializing {self.name} agent ({self.agent_type})")
    
    async def initialize(self) -> bool:
        """Initialize the agent"""
        try:
            self.status = AgentStatus.INITIALIZING
            self.logger.info(f"Initializing {self.name} agent")
            
            # Initialize agent-specific components
            await self._initialize_agent()
            
            # Load configuration
            await self._load_configuration()
            
            # Perform health check
            health_check = await self._perform_health_check()
            if not health_check:
                raise Exception("Health check failed")
            
            self.status = AgentStatus.IDLE
            self.logger.info(f"{self.name} agent initialized successfully")
            return True
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.last_error = str(e)
            self.error_count += 1
            self.logger.error(f"Failed to initialize {self.name} agent: {e}")
            return False
    
    @abstractmethod
    async def _initialize_agent(self) -> None:
        """Agent-specific initialization"""
        pass
    
    @abstractmethod
    async def _load_configuration(self) -> None:
        """Load agent-specific configuration"""
        pass
    
    @abstractmethod
    async def _perform_health_check(self) -> bool:
        """Perform agent-specific health check"""
        pass
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process a task assigned to this agent"""
        start_time = datetime.utcnow()
        
        try:
            self.status = AgentStatus.BUSY
            self.current_task = task
            self.total_requests += 1
            self.last_activity = datetime.utcnow()
            
            self.logger.info(f"Processing task {task.task_id} for {self.name}")
            
            # Update task status
            task.status = "in_progress"
            task.started_at = datetime.utcnow()
            
            # Process the task
            result = await self._process_task(task)
            
            # Update task completion
            task.status = "completed"
            task.completed_at = datetime.utcnow()
            task.result = result
            
            # Update performance metrics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_performance_metrics(processing_time, True)
            
            self.status = AgentStatus.IDLE
            self.current_task = None
            
            self.logger.info(f"Task {task.task_id} completed successfully in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            # Update error metrics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_performance_metrics(processing_time, False)
            self.error_count += 1
            self.last_error = str(e)
            
            # Update task status
            if self.current_task:
                self.current_task.status = "failed"
                self.current_task.error_message = str(e)
                self.current_task.completed_at = datetime.utcnow()
            
            self.status = AgentStatus.ERROR
            self.logger.error(f"Task {task.task_id} failed: {e}")
            
            # Attempt recovery
            await self._attempt_recovery()
            
            raise
    
    @abstractmethod
    async def _process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process a specific task - to be implemented by subclasses"""
        pass
    
    async def _attempt_recovery(self) -> bool:
        """Attempt to recover from errors"""
        try:
            self.logger.info(f"Attempting recovery for {self.name}")
            
            # Perform health check
            if await self._perform_health_check():
                self.status = AgentStatus.IDLE
                self.logger.info(f"Recovery successful for {self.name}")
                return True
            else:
                self.logger.warning(f"Recovery failed for {self.name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Recovery attempt failed for {self.name}: {e}")
            return False
    
    def _update_performance_metrics(self, response_time: float, success: bool) -> None:
        """Update agent performance metrics"""
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        # Update average response time
        if self.total_requests > 0:
            self.average_response_time = (
                (self.average_response_time * (self.total_requests - 1) + response_time) 
                / self.total_requests
            )
        
        # Update health score
        success_rate = (self.successful_requests / self.total_requests) * 100
        self.health_score = min(100.0, success_rate - (self.error_count * 5))
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_type": self.agent_type,
            "status": self.status,
            "health_score": self.health_score,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "average_response_time": self.average_response_time,
            "error_count": self.error_count,
            "last_error": self.last_error,
            "last_activity": self.last_activity,
            "current_task": self.current_task.task_id if self.current_task else None,
            "queue_length": len(self.task_queue)
        }
    
    async def shutdown(self) -> None:
        """Shutdown the agent gracefully"""
        try:
            self.logger.info(f"Shutting down {self.name} agent")
            self.status = AgentStatus.OFFLINE
            
            # Complete current task if any
            if self.current_task:
                self.logger.warning(f"Completing current task {self.current_task.task_id}")
                # Handle task completion based on agent type
            
            # Cleanup agent-specific resources
            await self._cleanup()
            
            self.logger.info(f"{self.name} agent shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown of {self.name}: {e}")
    
    @abstractmethod
    async def _cleanup(self) -> None:
        """Agent-specific cleanup"""
        pass
    
    def create_validation_result(
        self,
        rule_id: str,
        rule_name: str,
        rule_description: str,
        severity: ValidationSeverity,
        status: ValidationStatus,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        recommendations: Optional[List[str]] = None,
        compliance_frameworks: Optional[List[str]] = None
    ) -> ValidationResult:
        """Create a validation result"""
        return ValidationResult(
            rule_id=rule_id,
            rule_name=rule_name,
            rule_description=rule_description,
            severity=severity,
            status=status,
            message=message,
            details=details or {},
            recommendations=recommendations or [],
            compliance_frameworks=compliance_frameworks or [],
            domain=self.agent_type
        )
    
    async def communicate_with_agent(self, target_agent_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Communicate with another agent in the swarm"""
        # This would be implemented through the agent manager
        # For now, return a placeholder response
        return {
            "status": "message_sent",
            "target_agent": target_agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
