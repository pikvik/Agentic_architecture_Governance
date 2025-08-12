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
    APPLICATION = "application"
    BUSINESS = "business"


class ComponentType(str, Enum):
    """Component types"""
    SERVICE = "service"
    DATABASE = "database"
    API = "api"
    UI = "ui"
    QUEUE = "queue"
    CACHE = "cache"
    STORAGE = "storage"
    NETWORK = "network"
    SECURITY = "security"
    MONITORING = "monitoring"


class ComponentStatus(str, Enum):
    """Component status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    PLANNED = "planned"
    IN_DEVELOPMENT = "in_development"


class ArchitectureComponent(BaseModel):
    """Architecture component"""
    
    component_id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    component_type: ComponentType = Field(..., description="Type of component")
    domain: ArchitectureDomain = Field(..., description="Architecture domain")
    status: ComponentStatus = Field(..., description="Component status")
    description: str = Field(..., description="Component description")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    dependencies: List[str] = Field(default_factory=list, description="Component dependencies")
    interfaces: List[str] = Field(default_factory=list, description="Component interfaces")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Component configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ArchitecturePattern(BaseModel):
    """Architecture pattern"""
    
    pattern_id: str = Field(..., description="Unique pattern identifier")
    name: str = Field(..., description="Pattern name")
    category: str = Field(..., description="Pattern category")
    description: str = Field(..., description="Pattern description")
    benefits: List[str] = Field(default_factory=list, description="Pattern benefits")
    drawbacks: List[str] = Field(default_factory=list, description="Pattern drawbacks")
    use_cases: List[str] = Field(default_factory=list, description="Use cases")
    implementation_guidance: str = Field(..., description="Implementation guidance")
    examples: List[str] = Field(default_factory=list, description="Example implementations")


class ArchitectureDecision(BaseModel):
    """Architecture Decision Record (ADR)"""
    
    adr_id: str = Field(..., description="Unique ADR identifier")
    title: str = Field(..., description="Decision title")
    status: str = Field(..., description="Decision status")
    context: str = Field(..., description="Decision context")
    decision: str = Field(..., description="Decision made")
    consequences: List[str] = Field(default_factory=list, description="Decision consequences")
    alternatives_considered: List[str] = Field(default_factory=list, description="Alternatives considered")
    decision_drivers: List[str] = Field(default_factory=list, description="Decision drivers")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class FileType(str, Enum):
    """Supported file types for architecture documents"""
    PDF = "pdf"
    PPT = "ppt"
    PPTX = "pptx"
    DOC = "doc"
    DOCX = "docx"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    SVG = "svg"
    DIA = "dia"
    DRAW_IO = "drawio"
    LUCIDCHART = "lucidchart"
    VISIO = "vsdx"


class FileUploadStatus(str, Enum):
    """File upload status"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATED = "validated"


class ArchitectureFile(BaseModel):
    """Architecture file model"""
    
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    file_type: FileType = Field(..., description="File type")
    file_size: int = Field(..., description="File size in bytes")
    upload_path: str = Field(..., description="File storage path")
    upload_status: FileUploadStatus = Field(..., description="Upload status")
    processing_status: str = Field(default="pending", description="Processing status")
    
    # Metadata
    title: Optional[str] = Field(None, description="Document title")
    description: Optional[str] = Field(None, description="Document description")
    author: Optional[str] = Field(None, description="Document author")
    version: Optional[str] = Field(None, description="Document version")
    created_date: Optional[datetime] = Field(None, description="Document creation date")
    
    # Architecture context
    architecture_domain: Optional[ArchitectureDomain] = Field(None, description="Architecture domain")
    components_extracted: List[str] = Field(default_factory=list, description="Extracted component IDs")
    patterns_identified: List[str] = Field(default_factory=list, description="Identified pattern IDs")
    decisions_extracted: List[str] = Field(default_factory=list, description="Extracted decision IDs")
    
    # Processing results
    extracted_text: Optional[str] = Field(None, description="Extracted text content")
    extracted_images: List[str] = Field(default_factory=list, description="Extracted image paths")
    diagrams_detected: List[str] = Field(default_factory=list, description="Detected diagram paths")
    
    # Validation results
    validation_results: List[Dict[str, Any]] = Field(default_factory=list, description="Validation results")
    compliance_score: Optional[float] = Field(None, description="Compliance score")
    quality_score: Optional[float] = Field(None, description="Quality score")
    
    # Timestamps
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, description="Upload timestamp")
    processed_at: Optional[datetime] = Field(None, description="Processing completion timestamp")
    validated_at: Optional[datetime] = Field(None, description="Validation completion timestamp")
    
    # User context
    uploaded_by: Optional[str] = Field(None, description="User who uploaded the file")
    organization_id: Optional[str] = Field(None, description="Organization context")
    project_id: Optional[str] = Field(None, description="Project context")


class FileProcessingResult(BaseModel):
    """File processing result"""
    
    file_id: str = Field(..., description="File identifier")
    processing_success: bool = Field(..., description="Processing success status")
    processing_errors: List[str] = Field(default_factory=list, description="Processing errors")
    
    # Extracted content
    text_content: Optional[str] = Field(None, description="Extracted text content")
    image_paths: List[str] = Field(default_factory=list, description="Extracted image paths")
    diagram_paths: List[str] = Field(default_factory=list, description="Extracted diagram paths")
    
    # Architecture elements
    components_found: List[Dict[str, Any]] = Field(default_factory=list, description="Found components")
    patterns_found: List[Dict[str, Any]] = Field(default_factory=list, description="Found patterns")
    decisions_found: List[Dict[str, Any]] = Field(default_factory=list, description="Found decisions")
    
    # Metadata
    document_metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    processing_time: float = Field(..., description="Processing time in seconds")
    processed_at: datetime = Field(default_factory=datetime.utcnow, description="Processing timestamp")


class FileUploadRequest(BaseModel):
    """File upload request"""
    
    filename: str = Field(..., description="Original filename")
    file_type: FileType = Field(..., description="File type")
    file_size: int = Field(..., description="File size in bytes")
    architecture_domain: Optional[ArchitectureDomain] = Field(None, description="Architecture domain")
    description: Optional[str] = Field(None, description="File description")
    project_id: Optional[str] = Field(None, description="Project context")
    user_id: Optional[str] = Field(None, description="User uploading the file")


class FileValidationRequest(BaseModel):
    """File validation request"""
    
    file_id: str = Field(..., description="File to validate")
    validation_rules: List[str] = Field(default_factory=list, description="Validation rules to apply")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks")
    quality_standards: List[str] = Field(default_factory=list, description="Quality standards")
    priority: str = Field("medium", description="Validation priority")
