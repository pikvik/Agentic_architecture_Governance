"""
Architecture models for the Agentic AI Swarm system
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field

from .base import BaseModel


class ArchitectureDomain(str, Enum):
    """Architecture domains"""
    SOLUTION = "solution"
    TECHNICAL = "technical"
    SECURITY = "security"
    DATA = "data"
    INTEGRATION = "integration"
    INFRASTRUCTURE = "infrastructure"
    COSTING = "costing"
    APPLICATION_PORTFOLIO = "application_portfolio"


class ComponentType(str, Enum):
    """Types of architecture components"""
    SERVICE = "service"
    DATABASE = "database"
    API = "api"
    FRONTEND = "frontend"
    BACKEND = "backend"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    INTEGRATION = "integration"
    DATA_STORE = "data_store"
    EXTERNAL_SERVICE = "external_service"


class ComponentStatus(str, Enum):
    """Component status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"
    IN_DEVELOPMENT = "in_development"
    MAINTENANCE = "maintenance"


class ArchitectureComponent(BaseModel):
    """Architecture component model"""
    
    name: str = Field(..., description="Component name")
    component_type: ComponentType = Field(..., description="Type of component")
    domain: ArchitectureDomain = Field(..., description="Architecture domain")
    status: ComponentStatus = Field(ComponentStatus.ACTIVE, description="Component status")
    
    # Technical details
    technology_stack: List[str] = Field(default_factory=list, description="Technologies used")
    version: str = Field("1.0.0", description="Component version")
    description: str = Field(..., description="Component description")
    
    # Dependencies and relationships
    dependencies: List[str] = Field(default_factory=list, description="Component dependencies")
    dependents: List[str] = Field(default_factory=list, description="Components that depend on this")
    interfaces: List[str] = Field(default_factory=list, description="Component interfaces")
    
    # Configuration and settings
    config: Dict[str, Any] = Field(default_factory=dict, description="Component configuration")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    
    # Performance and monitoring
    performance_metrics: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    health_status: str = Field("healthy", description="Component health status")
    last_monitored: Optional[datetime] = Field(None, description="Last monitoring timestamp")
    
    # Security and compliance
    security_score: float = Field(100.0, description="Security score (0-100)")
    compliance_status: Dict[str, str] = Field(default_factory=dict, description="Compliance status by framework")
    vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list, description="Security vulnerabilities")
    
    # Cost and resource usage
    cost_per_month: float = Field(0.0, description="Monthly cost estimate")
    resource_usage: Dict[str, float] = Field(default_factory=dict, description="Resource usage metrics")
    
    # Documentation and metadata
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    repository_url: Optional[str] = Field(None, description="Source code repository URL")
    owner: Optional[str] = Field(None, description="Component owner")
    team: Optional[str] = Field(None, description="Responsible team")
    
    # Tags and categorization
    tags: List[str] = Field(default_factory=list, description="Component tags")
    business_capability: Optional[str] = Field(None, description="Associated business capability")
    criticality: str = Field("medium", description="Business criticality level")
    
    class Config:
        use_enum_values = True


class ArchitecturePattern(BaseModel):
    """Architecture pattern model"""
    
    name: str = Field(..., description="Pattern name")
    pattern_type: str = Field(..., description="Type of pattern")
    description: str = Field(..., description="Pattern description")
    
    # Pattern details
    components: List[str] = Field(default_factory=list, description="Components in this pattern")
    relationships: List[Dict[str, Any]] = Field(default_factory=list, description="Component relationships")
    constraints: List[str] = Field(default_factory=list, description="Pattern constraints")
    
    # Benefits and trade-offs
    benefits: List[str] = Field(default_factory=list, description="Pattern benefits")
    trade_offs: List[str] = Field(default_factory=list, description="Pattern trade-offs")
    
    # Usage context
    applicable_domains: List[ArchitectureDomain] = Field(default_factory=list, description="Applicable domains")
    use_cases: List[str] = Field(default_factory=list, description="Use cases")
    
    # Implementation guidance
    implementation_steps: List[str] = Field(default_factory=list, description="Implementation steps")
    best_practices: List[str] = Field(default_factory=list, description="Best practices")
    
    # References
    reference_urls: List[str] = Field(default_factory=list, description="Reference URLs")
    examples: List[str] = Field(default_factory=list, description="Example implementations")
    
    class Config:
        use_enum_values = True


class ArchitectureDecision(BaseModel):
    """Architecture decision record (ADR)"""
    
    title: str = Field(..., description="Decision title")
    status: str = Field("proposed", description="Decision status")
    context: str = Field(..., description="Decision context")
    
    # Decision details
    decision: str = Field(..., description="The decision made")
    consequences: List[str] = Field(default_factory=list, description="Consequences of the decision")
    alternatives: List[str] = Field(default_factory=list, description="Alternatives considered")
    
    # Impact and scope
    impacted_components: List[str] = Field(default_factory=list, description="Impacted components")
    impacted_domains: List[ArchitectureDomain] = Field(default_factory=list, description="Impacted domains")
    
    # Decision makers and timeline
    decision_makers: List[str] = Field(default_factory=list, description="Decision makers")
    decision_date: Optional[datetime] = Field(None, description="Decision date")
    review_date: Optional[datetime] = Field(None, description="Review date")
    
    # Rationale and evidence
    rationale: str = Field(..., description="Decision rationale")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    
    # Compliance and governance
    compliance_impact: Dict[str, str] = Field(default_factory=dict, description="Compliance impact")
    risk_assessment: str = Field("", description="Risk assessment")
    
    class Config:
        use_enum_values = True
