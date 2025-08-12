"""
Report models for the Agentic AI Swarm system
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field

from .base import BaseModel


class ReportType(str, Enum):
    """Types of reports"""
    GOVERNANCE_VALIDATION = "governance_validation"
    COMPLIANCE_AUDIT = "compliance_audit"
    SECURITY_ASSESSMENT = "security_assessment"
    COST_ANALYSIS = "cost_analysis"
    ARCHITECTURE_REVIEW = "architecture_review"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    INTEGRATION_VALIDATION = "integration_validation"
    DATA_QUALITY_ASSESSMENT = "data_quality_assessment"
    INFRASTRUCTURE_OPTIMIZATION = "infrastructure_optimization"
    APPLICATION_PORTFOLIO_REVIEW = "application_portfolio_review"


class ReportStatus(str, Enum):
    """Report status"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class ReportFormat(str, Enum):
    """Report output formats"""
    PDF = "pdf"
    JSON = "json"
    HTML = "html"
    CSV = "csv"
    EXCEL = "excel"


class Report(BaseModel):
    """Report model"""
    
    title: str = Field(..., description="Report title")
    report_type: ReportType = Field(..., description="Type of report")
    status: ReportStatus = Field(ReportStatus.DRAFT, description="Report status")
    
    # Content and data
    summary: str = Field(..., description="Executive summary")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="Key findings")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    conclusions: str = Field(..., description="Report conclusions")
    
    # Scope and context
    scope: str = Field(..., description="Report scope")
    target_audience: List[str] = Field(default_factory=list, description="Target audience")
    business_context: Dict[str, Any] = Field(default_factory=dict, description="Business context")
    
    # Data sources and methodology
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    methodology: str = Field(..., description="Methodology used")
    tools_used: List[str] = Field(default_factory=list, description="Tools and agents used")
    
    # Metrics and scores
    risk_score: float = Field(0.0, description="Overall risk score (0-100)")
    compliance_score: float = Field(0.0, description="Overall compliance score (0-100)")
    performance_score: float = Field(0.0, description="Overall performance score (0-100)")
    cost_score: float = Field(0.0, description="Overall cost efficiency score (0-100)")
    
    # Timing and lifecycle
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    valid_until: Optional[datetime] = Field(None, description="Report validity period")
    next_review_date: Optional[datetime] = Field(None, description="Next review date")
    
    # Authorship and approval
    author: str = Field(..., description="Report author")
    reviewers: List[str] = Field(default_factory=list, description="Report reviewers")
    approver: Optional[str] = Field(None, description="Report approver")
    approval_date: Optional[datetime] = Field(None, description="Approval date")
    
    # Attachments and references
    attachments: List[str] = Field(default_factory=list, description="Report attachments")
    references: List[str] = Field(default_factory=list, description="References and sources")
    
    # Version control
    version: str = Field("1.0", description="Report version")
    previous_version: Optional[str] = Field(None, description="Previous version ID")
    change_log: List[str] = Field(default_factory=list, description="Change log")
    
    # Distribution and access
    distribution_list: List[str] = Field(default_factory=list, description="Distribution list")
    access_level: str = Field("internal", description="Access level")
    tags: List[str] = Field(default_factory=list, description="Report tags")
    
    class Config:
        use_enum_values = True


class ReportTemplate(BaseModel):
    """Report template model"""
    
    name: str = Field(..., description="Template name")
    report_type: ReportType = Field(..., description="Template type")
    description: str = Field(..., description="Template description")
    
    # Template structure
    sections: List[Dict[str, Any]] = Field(default_factory=list, description="Template sections")
    required_fields: List[str] = Field(default_factory=list, description="Required fields")
    optional_fields: List[str] = Field(default_factory=list, description="Optional fields")
    
    # Formatting and styling
    format_config: Dict[str, Any] = Field(default_factory=dict, description="Format configuration")
    styling: Dict[str, Any] = Field(default_factory=dict, description="Styling configuration")
    
    # Default values
    default_values: Dict[str, Any] = Field(default_factory=dict, description="Default values")
    placeholders: Dict[str, str] = Field(default_factory=dict, description="Placeholder mappings")
    
    # Usage context
    applicable_domains: List[str] = Field(default_factory=list, description="Applicable domains")
    use_cases: List[str] = Field(default_factory=list, description="Use cases")
    
    # Version and maintenance
    version: str = Field("1.0", description="Template version")
    is_active: bool = Field(True, description="Whether template is active")
    created_by: str = Field(..., description="Template creator")
    
    class Config:
        use_enum_values = True


class ReportSchedule(BaseModel):
    """Report scheduling model"""
    
    name: str = Field(..., description="Schedule name")
    report_type: ReportType = Field(..., description="Report type to generate")
    template_id: str = Field(..., description="Template to use")
    
    # Schedule configuration
    frequency: str = Field(..., description="Schedule frequency (daily, weekly, monthly)")
    cron_expression: Optional[str] = Field(None, description="Cron expression for custom schedules")
    timezone: str = Field("UTC", description="Timezone for scheduling")
    
    # Scope and parameters
    scope: Dict[str, Any] = Field(default_factory=dict, description="Report scope")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Report parameters")
    
    # Recipients and distribution
    recipients: List[str] = Field(default_factory=list, description="Report recipients")
    distribution_method: str = Field("email", description="Distribution method")
    
    # Status and control
    is_active: bool = Field(True, description="Whether schedule is active")
    last_run: Optional[datetime] = Field(None, description="Last run timestamp")
    next_run: Optional[datetime] = Field(None, description="Next run timestamp")
    
    # Error handling
    retry_count: int = Field(0, description="Number of retries on failure")
    max_retries: int = Field(3, description="Maximum retry attempts")
    error_notification: List[str] = Field(default_factory=list, description="Error notification recipients")
    
    class Config:
        use_enum_values = True
