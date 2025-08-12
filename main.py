"""
Main application entry point for the Agentic AI Swarm
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
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
