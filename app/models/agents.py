"""
Agent models for the Agentic AI Swarm system
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field

from .base import BaseModel


class AgentType(str, Enum):
    """Types of agents in the swarm"""
    CORE_BRAIN = "core_brain"
    SOLUTION_ARCHITECTURE = "solution_architecture"
    TECHNICAL_ARCHITECTURE = "technical_architecture"
    SECURITY_ARCHITECTURE = "security_architecture"
    DATA_ARCHITECTURE = "data_architecture"
    INTEGRATION_ARCHITECTURE = "integration_architecture"
    INFRASTRUCTURE_ARCHITECTURE = "infrastructure_architecture"
    COSTING = "costing"
    APPLICATION_PORTFOLIO = "application_portfolio"
    GENERIC = "generic"


class AgentStatus(str, Enum):
    """Agent status states"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    UPDATING = "updating"


class AgentCapability(str, Enum):
    """Agent capabilities"""
    CODE_ANALYSIS = "code_analysis"
    SECURITY_SCANNING = "security_scanning"
    COST_OPTIMIZATION = "cost_optimization"
    COMPLIANCE_CHECKING = "compliance_checking"
    ARCHITECTURE_VALIDATION = "architecture_validation"
    DOCUMENTATION_GENERATION = "documentation_generation"
    API_TESTING = "api_testing"
    INFRASTRUCTURE_SCANNING = "infrastructure_scanning"
    DATA_QUALITY_ASSESSMENT = "data_quality_assessment"
    INTEGRATION_VALIDATION = "integration_validation"


class Agent(BaseModel):
    """AI Agent model"""
    
    name: str = Field(..., description="Agent name")
    agent_type: AgentType = Field(..., description="Type of agent")
    status: AgentStatus = Field(AgentStatus.IDLE, description="Current agent status")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    description: str = Field(..., description="Agent description")
    version: str = Field("1.0.0", description="Agent version")
    
    # Performance metrics
    total_requests_processed: int = Field(0, description="Total requests processed")
    average_response_time: float = Field(0.0, description="Average response time in seconds")
    success_rate: float = Field(100.0, description="Success rate percentage")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    
    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict, description="Agent configuration")
    llm_provider: str = Field("openai", description="LLM provider used by agent")
    model_name: str = Field("gpt-4", description="LLM model name")
    
    # Health and monitoring
    health_score: float = Field(100.0, description="Agent health score (0-100)")
    error_count: int = Field(0, description="Number of errors encountered")
    last_error: Optional[str] = Field(None, description="Last error message")
    
    # Dependencies
    dependencies: List[str] = Field(default_factory=list, description="Other agents this agent depends on")
    required_apis: List[str] = Field(default_factory=list, description="Required external APIs")
    
    # Resource usage
    memory_usage_mb: float = Field(0.0, description="Memory usage in MB")
    cpu_usage_percent: float = Field(0.0, description="CPU usage percentage")
    
    class Config:
        use_enum_values = True


class AgentTask(BaseModel):
    """Task assigned to an agent"""
    
    task_id: str = Field(..., description="Unique task identifier")
    agent_id: str = Field(..., description="Agent assigned to this task")
    task_type: str = Field(..., description="Type of task")
    priority: str = Field("medium", description="Task priority")
    status: str = Field("pending", description="Task status")
    
    # Task details
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data for the task")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    timeout_seconds: int = Field(300, description="Task timeout")
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Task creation time")
    started_at: Optional[datetime] = Field(None, description="Task start time")
    completed_at: Optional[datetime] = Field(None, description="Task completion time")
    
    # Results
    result: Optional[Dict[str, Any]] = Field(None, description="Task result")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Progress tracking
    progress_percentage: float = Field(0.0, description="Task progress percentage")
    current_step: str = Field("", description="Current step description")


class AgentCommunication(BaseModel):
    """Inter-agent communication message"""
    
    message_id: str = Field(..., description="Unique message identifier")
    sender_agent_id: str = Field(..., description="Sending agent ID")
    receiver_agent_id: str = Field(..., description="Receiving agent ID")
    message_type: str = Field(..., description="Type of message")
    
    # Message content
    content: Dict[str, Any] = Field(..., description="Message content")
    priority: str = Field("normal", description="Message priority")
    
    # Timing
    sent_at: datetime = Field(default_factory=datetime.utcnow, description="Message sent time")
    received_at: Optional[datetime] = Field(None, description="Message received time")
    
    # Status
    status: str = Field("sent", description="Message status")
    requires_response: bool = Field(False, description="Whether response is required")
    response_message_id: Optional[str] = Field(None, description="Response message ID")
