"""
Governance models for the Agentic AI Swarm system
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field

from .base import BaseModel


class ValidationSeverity(str, Enum):
    """Validation severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ValidationStatus(str, Enum):
    """Validation status"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"
    ERROR = "error"


class GovernanceScope(str, Enum):
    """Governance scope types"""
    SOLUTION = "solution"
    TECHNICAL = "technical"
    SECURITY = "security"
    DATA = "data"
    INTEGRATION = "integration"
    INFRASTRUCTURE = "infrastructure"
    COSTING = "costing"
    APPLICATION_PORTFOLIO = "application_portfolio"
    COMPREHENSIVE = "comprehensive"


class ValidationResult(BaseModel):
    """Individual validation result"""
    
    rule_id: str = Field(..., description="Unique identifier for the validation rule")
    rule_name: str = Field(..., description="Human-readable name of the validation rule")
    rule_description: str = Field(..., description="Description of what the rule validates")
    severity: ValidationSeverity = Field(..., description="Severity level of the validation")
    status: ValidationStatus = Field(..., description="Validation status")
    message: str = Field(..., description="Validation message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional validation details")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for improvement")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Relevant compliance frameworks")
    domain: GovernanceScope = Field(..., description="Architecture domain this validation belongs to")


class GovernanceRequest(BaseModel):
    """Governance validation request"""
    
    request_id: str = Field(..., description="Unique request identifier")
    scope: GovernanceScope = Field(..., description="Scope of governance validation")
    target_components: List[str] = Field(default_factory=list, description="Specific components to validate")
    business_context: Dict[str, Any] = Field(default_factory=dict, description="Business context and requirements")
    technical_context: Dict[str, Any] = Field(default_factory=dict, description="Technical context and constraints")
    compliance_requirements: List[str] = Field(default_factory=list, description="Required compliance frameworks")
    priority: str = Field("medium", description="Request priority")
    timeout_seconds: int = Field(300, description="Request timeout in seconds")
    user_id: Optional[str] = Field(None, description="User making the request")
    organization_id: Optional[str] = Field(None, description="Organization context")


class GovernanceResponse(BaseModel):
    """Governance validation response"""
    
    request_id: str = Field(..., description="Original request identifier")
    status: str = Field(..., description="Overall governance status")
    summary: str = Field(..., description="Executive summary of findings")
    validation_results: List[ValidationResult] = Field(default_factory=list, description="All validation results")
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    compliance_score: float = Field(..., description="Overall compliance score (0-100)")
    recommendations: List[str] = Field(default_factory=list, description="High-level recommendations")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When the response was generated")
    processing_time_seconds: float = Field(..., description="Total processing time")
    agents_used: List[str] = Field(default_factory=list, description="Agents that participated in validation")
