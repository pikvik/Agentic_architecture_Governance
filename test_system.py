#!/usr/bin/env python3
"""
Test script for the Agentic AI Swarm system
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data for testing
MOCK_GOVERNANCE_REQUEST = {
    "request_id": "test-gov-001",
    "scope": "comprehensive",
    "target_components": ["web-service", "database", "api-gateway"],
    "business_context": {
        "business_value": "E-commerce platform for retail customers",
        "stakeholders": ["customers", "business_owners", "developers"],
        "required_capabilities": ["customer_management", "order_processing", "payment_processing"]
    },
    "technical_context": {
        "solution_pattern": "microservices",
        "technology_stack": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "deployment_model": "cloud-native",
        "scalability_requirements": "high",
        "load_balancing": True,
        "auto_scaling": True
    },
    "compliance_requirements": ["GDPR", "PCI-DSS", "ISO_27001"],
    "priority": "high",
    "timeout_seconds": 300,
    "user_id": "test-user",
    "organization_id": "test-org"
}

async def test_agent_initialization():
    """Test agent initialization"""
    logger.info("🧪 Testing Agent Initialization...")
    
    try:
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
        
        # Create agents
        agents = {
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
        
        # Initialize agents
        for name, agent in agents.items():
            success = await agent.initialize()
            logger.info(f"✅ {name}: {'Initialized' if success else 'Failed'}")
        
        # Create and initialize core brain
        core_brain = CoreBrainAgent()
        for name, agent in agents.items():
            core_brain.register_specialized_agent(name, agent)
        
        success = await core_brain.initialize()
        logger.info(f"✅ Core Brain: {'Initialized' if success else 'Failed'}")
        
        return core_brain, agents
        
    except Exception as e:
        logger.error(f"❌ Agent initialization failed: {e}")
        return None, None

async def test_governance_validation(core_brain):
    """Test governance validation"""
    logger.info("🧪 Testing Governance Validation...")
    
    try:
        from app.models.governance import GovernanceRequest
        from app.models.agents import AgentTask
        
        # Create governance request
        governance_request = GovernanceRequest(**MOCK_GOVERNANCE_REQUEST)
        
        # Create task
        task = AgentTask(
            task_id=governance_request.request_id,
            agent_id=core_brain.agent_id,
            task_type="governance_validation",
            priority=governance_request.priority,
            input_data={"governance_request": governance_request.dict()},
            timeout_seconds=governance_request.timeout_seconds
        )
        
        # Process task
        logger.info("🔄 Processing governance validation...")
        result = await core_brain.process_task(task)
        
        logger.info("✅ Governance validation completed!")
        logger.info(f"📊 Results: {json.dumps(result, indent=2, default=str)}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Governance validation failed: {e}")
        return None

async def test_individual_agents(agents):
    """Test individual agent functionality"""
    logger.info("🧪 Testing Individual Agents...")
    
    try:
        from app.models.agents import AgentTask
        
        for name, agent in agents.items():
            logger.info(f"🔄 Testing {name} agent...")
            
            # Create a simple task for each agent
            task = AgentTask(
                task_id=f"test-{name}-001",
                agent_id=agent.agent_id,
                task_type="validation",
                priority="medium",
                input_data={"test": True, "agent": name},
                timeout_seconds=60
            )
            
            # Process task
            result = await agent.process_task(task)
            logger.info(f"✅ {name}: Task completed successfully")
            logger.info(f"   Risk Score: {result.get('risk_score', 'N/A')}")
            logger.info(f"   Compliance Score: {result.get('compliance_score', 'N/A')}")
            
    except Exception as e:
        logger.error(f"❌ Individual agent testing failed: {e}")

async def test_swarm_status(core_brain):
    """Test swarm status monitoring"""
    logger.info("🧪 Testing Swarm Status...")
    
    try:
        status = await core_brain.get_swarm_status()
        logger.info("✅ Swarm status retrieved successfully")
        logger.info(f"📊 Overall Health: {status.get('overall_health', 'N/A')}%")
        logger.info(f"👥 Total Agents: {status.get('total_agents', 'N/A')}")
        logger.info(f"🔄 Active Tasks: {status.get('active_tasks', 'N/A')}")
        
        return status
        
    except Exception as e:
        logger.error(f"❌ Swarm status test failed: {e}")
        return None

async def main():
    """Main test function"""
    logger.info("🚀 Starting Agentic AI Swarm System Test")
    logger.info("=" * 50)
    
    # Test 1: Agent Initialization
    core_brain, agents = await test_agent_initialization()
    if not core_brain:
        logger.error("❌ Cannot proceed without core brain agent")
        return
    
    logger.info("=" * 50)
    
    # Test 2: Individual Agent Testing
    await test_individual_agents(agents)
    
    logger.info("=" * 50)
    
    # Test 3: Swarm Status
    await test_swarm_status(core_brain)
    
    logger.info("=" * 50)
    
    # Test 4: Governance Validation
    await test_governance_validation(core_brain)
    
    logger.info("=" * 50)
    
    # Test 5: Shutdown
    logger.info("🧪 Testing Shutdown...")
    try:
        await core_brain.shutdown()
        for name, agent in agents.items():
            await agent.shutdown()
        logger.info("✅ All agents shutdown successfully")
    except Exception as e:
        logger.error(f"❌ Shutdown failed: {e}")
    
    logger.info("🎉 All tests completed!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(main())
