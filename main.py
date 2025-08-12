"""
Main application entry point for the Agentic AI Swarm
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from uuid import uuid4
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.agents import (
    CoreBrainAgent,
    SolutionArchitectureAgent,
    TechnicalArchitectureAgent,
    SecurityArchitectureAgent,
    DataArchitectureAgent,
    IntegrationArchitectureAgent,
    InfrastructureArchitectureAgent,
    CostingAgent,
    ApplicationPortfolioAgent,
    GenericAgent
)
from app.models.governance import GovernanceRequest, GovernanceResponse
from app.models.agents import AgentTask
from app.models.architecture import (
    ArchitectureFile, FileType, FileUploadStatus, FileUploadRequest, 
    FileValidationRequest, FileProcessingResult
)
from app.services.file_processor import file_processor
from app.services.dify_service import dify_service
from app.services.ollama_service import ollama_service


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instances
agents: Dict[str, Any] = {}
core_brain_agent: CoreBrainAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Agentic AI Swarm...")
    
    try:
        # Initialize all agents
        await initialize_agents()
        logger.info("All agents initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize agents: {e}")
        sys.exit(1)
    
    finally:
        # Shutdown
        logger.info("Shutting down Agentic AI Swarm...")
        await shutdown_agents()
        logger.info("Shutdown complete")


async def initialize_agents():
    """Initialize all agents in the swarm"""
    global agents, core_brain_agent
    
    # Create specialized agents
    specialized_agents = {
        "solution_architecture": SolutionArchitectureAgent(),
        "technical_architecture": TechnicalArchitectureAgent(),
        "security_architecture": SecurityArchitectureAgent(),
        "data_architecture": DataArchitectureAgent(),
        "integration_architecture": IntegrationArchitectureAgent(),
        "infrastructure_architecture": InfrastructureArchitectureAgent(),
        "costing": CostingAgent(),
        "application_portfolio": ApplicationPortfolioAgent(),
        "generic": GenericAgent()
    }
    
    # Initialize specialized agents
    for name, agent in specialized_agents.items():
        try:
            success = await agent.initialize()
            if success:
                agents[name] = agent
                logger.info(f"Agent {name} initialized successfully")
            else:
                logger.error(f"Failed to initialize agent {name}")
        except Exception as e:
            logger.error(f"Error initializing agent {name}: {e}")
    
    # Create and initialize core brain agent
    core_brain_agent = CoreBrainAgent()
    
    # Register specialized agents with core brain
    for name, agent in agents.items():
        core_brain_agent.register_specialized_agent(name, agent)
    
    # Initialize core brain agent
    success = await core_brain_agent.initialize()
    if not success:
        raise Exception("Failed to initialize core brain agent")
    
    agents["core_brain"] = core_brain_agent
    logger.info("Core brain agent initialized successfully")


async def shutdown_agents():
    """Shutdown all agents gracefully"""
    global agents
    
    for name, agent in agents.items():
        try:
            await agent.shutdown()
            logger.info(f"Agent {name} shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down agent {name}: {e}")


# Create FastAPI application
app = FastAPI(
    title="Agentic AI Swarm - Architecture Governance",
    description="Autonomous AI swarm for software architecture governance and validation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic AI Swarm - Architecture Governance & Validation",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if core brain agent is healthy
        if core_brain_agent:
            swarm_status = await core_brain_agent.get_swarm_status()
            return {
                "status": "healthy",
                "swarm_health": swarm_status["overall_health"],
                "active_agents": len(agents),
                "active_tasks": swarm_status["active_tasks"]
            }
        else:
            return {"status": "unhealthy", "error": "Core brain agent not initialized"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/agents")
async def list_agents():
    """List all agents and their status"""
    try:
        agent_statuses = {}
        for name, agent in agents.items():
            try:
                status = await agent.get_status()
                agent_statuses[name] = status
            except Exception as e:
                agent_statuses[name] = {"status": "error", "error": str(e)}
        
        return {
            "agents": agent_statuses,
            "total_agents": len(agents)
        }
    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/governance/validate")
async def validate_governance(
    request: GovernanceRequest,
    background_tasks: BackgroundTasks
):
    """Validate architecture governance"""
    try:
        if not core_brain_agent:
            raise HTTPException(status_code=503, detail="Core brain agent not available")
        
        # Create task for core brain agent
        task = AgentTask(
            task_id=request.request_id,
            agent_id=core_brain_agent.agent_id,
            task_type="governance_validation",
            priority=request.priority,
            input_data={"governance_request": request.dict()},
            timeout_seconds=request.timeout_seconds
        )
        
        # Process task
        result = await core_brain_agent.process_task(task)
        
        # Convert result to GovernanceResponse
        governance_response = GovernanceResponse(
            request_id=request.request_id,
            status=result.get("status", "completed"),
            summary=result.get("summary", "Governance validation completed"),
            validation_results=result.get("validation_results", []),
            risk_score=result.get("risk_score", 0.0),
            compliance_score=result.get("compliance_score", 0.0),
            recommendations=result.get("recommendations", []),
            next_steps=result.get("next_steps", []),
            processing_time_seconds=0.0,
            agents_used=result.get("agents_used", [])
        )
        
        return governance_response
        
    except Exception as e:
        logger.error(f"Governance validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/governance/status/{request_id}")
async def get_governance_status(request_id: str):
    """Get status of a governance validation request"""
    try:
        # This would typically query a database for request status
        # For now, return a placeholder response
        return {
            "request_id": request_id,
            "status": "completed",
            "message": "Request status retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Failed to get governance status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/swarm/status")
async def get_swarm_status():
    """Get overall swarm status"""
    try:
        if not core_brain_agent:
            raise HTTPException(status_code=503, detail="Core brain agent not available")
        
        swarm_status = await core_brain_agent.get_swarm_status()
        return swarm_status
        
    except Exception as e:
        logger.error(f"Failed to get swarm status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_name}/task")
async def assign_task_to_agent(agent_name: str, task_data: Dict[str, Any]):
    """Assign a task to a specific agent"""
    try:
        if agent_name not in agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        agent = agents[agent_name]
        
        # Create task
        task = AgentTask(
            task_id=task_data.get("task_id", f"task_{agent_name}_{len(agent.task_queue)}"),
            agent_id=agent.agent_id,
            task_type=task_data.get("task_type", "general"),
            priority=task_data.get("priority", "medium"),
            input_data=task_data.get("input_data", {}),
            timeout_seconds=task_data.get("timeout_seconds", 300)
        )
        
        # Process task
        result = await agent.process_task(task)
        
        return {
            "task_id": task.task_id,
            "agent": agent_name,
            "status": "completed",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Failed to assign task to agent {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_id}/start")
async def start_agent(agent_id: str):
    """Start a specific agent"""
    try:
        # Find agent by ID
        agent = None
        for name, a in agents.items():
            if a.agent_id == agent_id:
                agent = a
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
        
        # Start the agent
        success = await agent.start()
        if success:
            return {"message": f"Agent {agent_id} started successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to start agent {agent_id}")
            
    except Exception as e:
        logger.error(f"Failed to start agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """Stop a specific agent"""
    try:
        # Find agent by ID
        agent = None
        for name, a in agents.items():
            if a.agent_id == agent_id:
                agent = a
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
        
        # Stop the agent
        success = await agent.stop()
        if success:
            return {"message": f"Agent {agent_id} stopped successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to stop agent {agent_id}")
            
    except Exception as e:
        logger.error(f"Failed to stop agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{agent_id}/restart")
async def restart_agent(agent_id: str):
    """Restart a specific agent"""
    try:
        # Find agent by ID
        agent = None
        for name, a in agents.items():
            if a.agent_id == agent_id:
                agent = a
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent with ID {agent_id} not found")
        
        # Restart the agent
        success = await agent.restart()
        if success:
            return {"message": f"Agent {agent_id} restarted successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to restart agent {agent_id}")
            
    except Exception as e:
        logger.error(f"Failed to restart agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# File Upload and Processing Endpoints
@app.post("/files/upload")
async def upload_architecture_file(
    file: UploadFile,
    architecture_domain: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    project_id: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None)
):
    """Upload an architecture file for processing"""
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        file_type_map = {
            'pdf': FileType.PDF,
            'docx': FileType.DOCX,
            'ppt': FileType.PPT,
            'pptx': FileType.PPTX,
            'doc': FileType.DOC,
            'png': FileType.PNG,
            'jpg': FileType.JPG,
            'jpeg': FileType.JPEG,
            'svg': FileType.SVG,
            'dia': FileType.DIA,
            'drawio': FileType.DRAW_IO,
            'vsdx': FileType.VISIO
        }
        
        if file_extension not in file_type_map:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Supported types: {list(file_type_map.keys())}"
            )
        
        file_type = file_type_map[file_extension]
        
        # Generate file ID
        file_id = str(uuid4())
        
        # Create upload directory
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = upload_dir / f"{file_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create architecture file record
        architecture_file = ArchitectureFile(
            file_id=file_id,
            filename=file.filename,
            file_type=file_type,
            file_size=len(content),
            upload_path=str(file_path),
            upload_status=FileUploadStatus.UPLOADING,
            architecture_domain=architecture_domain,
            description=description,
            project_id=project_id,
            uploaded_by=user_id
        )
        
        # Process file asynchronously
        asyncio.create_task(process_uploaded_file(architecture_file))
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_type": file_type,
            "file_size": len(content),
            "status": "uploading",
            "message": "File uploaded successfully. Processing started."
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_uploaded_file(architecture_file: ArchitectureFile):
    """Process an uploaded file asynchronously"""
    try:
        # Update status to processing
        architecture_file.upload_status = FileUploadStatus.PROCESSING
        
        # Process the file
        processing_result = await file_processor.process_file(
            architecture_file.upload_path,
            architecture_file.file_type,
            architecture_file.file_id
        )
        
        if processing_result.processing_success:
            # Update file with processing results
            architecture_file.upload_status = FileUploadStatus.COMPLETED
            architecture_file.processing_status = "completed"
            architecture_file.extracted_text = processing_result.text_content
            architecture_file.extracted_images = processing_result.image_paths
            architecture_file.diagrams_detected = processing_result.diagram_paths
            architecture_file.processed_at = processing_result.processed_at
            
            # Extract architecture elements from text
            if processing_result.text_content:
                elements = await file_processor.extract_architecture_elements(processing_result.text_content)
                architecture_file.components_extracted = [str(comp) for comp in elements.get("components_found", [])]
                architecture_file.patterns_identified = [str(pattern) for pattern in elements.get("patterns_found", [])]
                architecture_file.decisions_extracted = [str(decision) for decision in elements.get("decisions_found", [])]
            
            logger.info(f"File {architecture_file.file_id} processed successfully")
        else:
            architecture_file.upload_status = FileUploadStatus.FAILED
            architecture_file.processing_status = "failed"
            logger.error(f"File {architecture_file.file_id} processing failed: {processing_result.processing_errors}")
            
    except Exception as e:
        architecture_file.upload_status = FileUploadStatus.FAILED
        architecture_file.processing_status = "failed"
        logger.error(f"Error processing file {architecture_file.file_id}: {e}")


@app.get("/files")
async def list_architecture_files():
    """List all uploaded architecture files"""
    try:
        # In a real implementation, this would query a database
        # For now, return a placeholder response
        return {
            "files": [],
            "total": 0,
            "message": "No files uploaded yet"
        }
    except Exception as e:
        logger.error(f"Failed to list files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{file_id}")
async def get_architecture_file(file_id: str):
    """Get details of a specific architecture file"""
    try:
        # In a real implementation, this would query a database
        # For now, return a placeholder response
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")
    except Exception as e:
        logger.error(f"Failed to get file {file_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/files/{file_id}/validate")
async def validate_architecture_file(file_id: str, request: FileValidationRequest):
    """Validate an architecture file"""
    try:
        # In a real implementation, this would validate the file using the governance system
        # For now, return a placeholder response
        return {
            "file_id": file_id,
            "validation_status": "completed",
            "compliance_score": 85.0,
            "quality_score": 90.0,
            "validation_results": [
                {
                    "rule": "architecture_consistency",
                    "status": "passed",
                    "score": 90.0,
                    "message": "Architecture is consistent with best practices"
                }
            ],
            "message": "File validation completed successfully"
        }
    except Exception as e:
        logger.error(f"Failed to validate file {file_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/files/{file_id}")
async def delete_architecture_file(file_id: str):
    """Delete an architecture file"""
    try:
        # In a real implementation, this would delete the file and database record
        # For now, return a placeholder response
        return {
            "file_id": file_id,
            "message": "File deleted successfully"
        }
    except Exception as e:
        logger.error(f"Failed to delete file {file_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# LLM Integration Endpoints
@app.get("/llm/health")
async def llm_health_check():
    """Check health of LLM services"""
    try:
        # Check Dify health
        dify_healthy = await dify_service.health_check()
        
        # Check Ollama health
        ollama_healthy = await ollama_service.health_check()
        
        return {
            "dify": {
                "status": "healthy" if dify_healthy else "unhealthy",
                "base_url": dify_service.base_url
            },
            "ollama": {
                "status": "healthy" if ollama_healthy else "unhealthy",
                "base_url": ollama_service.base_url,
                "default_model": ollama_service.default_model
            },
            "overall_status": "healthy" if (dify_healthy or ollama_healthy) else "unhealthy"
        }
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/ollama/models")
async def list_ollama_models():
    """List available Ollama models"""
    try:
        models = await ollama_service.list_models()
        return {
            "models": models,
            "default_model": ollama_service.default_model
        }
    except Exception as e:
        logger.error(f"Failed to list Ollama models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/ollama/generate")
async def ollama_generate(request: Dict[str, Any]):
    """Generate text using Ollama"""
    try:
        prompt = request.get("prompt")
        model = request.get("model")
        temperature = request.get("temperature")
        max_tokens = request.get("max_tokens")
        system_prompt = request.get("system_prompt")
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        result = await ollama_service.generate_text(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Ollama generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/ollama/chat")
async def ollama_chat(request: Dict[str, Any]):
    """Chat completion using Ollama"""
    try:
        messages = request.get("messages", [])
        model = request.get("model")
        temperature = request.get("temperature")
        max_tokens = request.get("max_tokens")
        
        if not messages:
            raise HTTPException(status_code=400, detail="Messages are required")
        
        result = await ollama_service.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Ollama chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/ollama/embed")
async def ollama_embed(request: Dict[str, Any]):
    """Generate embeddings using Ollama"""
    try:
        text = request.get("text")
        model = request.get("model")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        result = await ollama_service.embed_text(text=text, model=model)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Ollama embedding failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/ollama/pull")
async def ollama_pull_model(request: Dict[str, Any]):
    """Pull a model to Ollama"""
    try:
        model = request.get("model")
        
        if not model:
            raise HTTPException(status_code=400, detail="Model name is required")
        
        result = await ollama_service.pull_model(model=model)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Ollama model pull failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/dify/workspaces")
async def list_dify_workspaces():
    """List Dify workspaces"""
    try:
        workspaces = await dify_service.list_workspaces()
        return {
            "workspaces": workspaces,
            "current_workspace_id": dify_service.workspace_id
        }
    except Exception as e:
        logger.error(f"Failed to list Dify workspaces: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/dify/applications")
async def list_dify_applications(workspace_id: Optional[str] = None):
    """List Dify applications"""
    try:
        applications = await dify_service.list_applications(workspace_id=workspace_id)
        return {
            "applications": applications,
            "current_app_id": dify_service.app_id
        }
    except Exception as e:
        logger.error(f"Failed to list Dify applications: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/dify/chat")
async def dify_chat(request: Dict[str, Any]):
    """Chat completion using Dify"""
    try:
        messages = request.get("messages", [])
        app_id = request.get("app_id")
        user_id = request.get("user_id")
        conversation_id = request.get("conversation_id")
        inputs = request.get("inputs", {})
        
        if not messages:
            raise HTTPException(status_code=400, detail="Messages are required")
        
        result = await dify_service.chat_completion(
            messages=messages,
            app_id=app_id,
            user_id=user_id,
            conversation_id=conversation_id,
            inputs=inputs
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Dify chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm/dify/completion")
async def dify_completion(request: Dict[str, Any]):
    """Text completion using Dify"""
    try:
        prompt = request.get("prompt")
        app_id = request.get("app_id")
        user_id = request.get("user_id")
        inputs = request.get("inputs", {})
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        result = await dify_service.completion(
            prompt=prompt,
            app_id=app_id,
            user_id=user_id,
            inputs=inputs
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Dify completion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/llm/dify/conversations/{conversation_id}")
async def get_dify_conversation(conversation_id: str, app_id: Optional[str] = None):
    """Get Dify conversation history"""
    try:
        result = await dify_service.get_conversation_history(
            conversation_id=conversation_id,
            app_id=app_id
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Failed to get Dify conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
