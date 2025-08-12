"""
Core Brain Agent - Orchestrates all specialized agents in the swarm
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from app.agents.base_agent import BaseAgent
from app.models.agents import AgentType, AgentStatus, AgentTask
from app.models.governance import (
    GovernanceRequest, 
    GovernanceResponse, 
    ValidationResult,
    ValidationStatus,
    ValidationSeverity,
    GovernanceScope
)
from app.config import settings


class CoreBrainAgent(BaseAgent):
    """Core Brain Agent that orchestrates all specialized agents"""
    
    def __init__(self):
        super().__init__(
            agent_type=AgentType.CORE_BRAIN,
            name="Core Brain Agent",
            description="Orchestrates all specialized agents for comprehensive architecture governance"
        )
        
        # Agent registry - will be populated by agent manager
        self.specialized_agents: Dict[str, Any] = {}
        
        # Task routing rules
        self.routing_rules = {
            GovernanceScope.SOLUTION: ["solution_architecture"],
            GovernanceScope.TECHNICAL: ["technical_architecture"],
            GovernanceScope.SECURITY: ["security_architecture"],
            GovernanceScope.DATA: ["data_architecture"],
            GovernanceScope.INTEGRATION: ["integration_architecture"],
            GovernanceScope.INFRASTRUCTURE: ["infrastructure_architecture"],
            GovernanceScope.COSTING: ["costing"],
            GovernanceScope.APPLICATION_PORTFOLIO: ["application_portfolio"],
            GovernanceScope.COMPREHENSIVE: [
                "solution_architecture",
                "technical_architecture", 
                "security_architecture",
                "data_architecture",
                "integration_architecture",
                "infrastructure_architecture",
                "costing",
                "application_portfolio"
            ]
        }
        
        # Governance frameworks and standards
        self.governance_frameworks = {
            "TOGAF": "The Open Group Architecture Framework",
            "ISO_42010": "ISO/IEC/IEEE 42010 Systems and software engineering",
            "AWS_WELL_ARCHITECTED": "AWS Well-Architected Framework",
            "AZURE_ARCHITECTURE": "Microsoft Azure Architecture Framework",
            "GCP_ARCHITECTURE": "Google Cloud Architecture Framework",
            "NIST_CYBERSECURITY": "NIST Cybersecurity Framework",
            "GDPR": "General Data Protection Regulation",
            "SOX": "Sarbanes-Oxley Act",
            "HIPAA": "Health Insurance Portability and Accountability Act"
        }
    
    async def _initialize_agent(self) -> None:
        """Initialize the core brain agent"""
        self.logger.info("Initializing Core Brain Agent")
        
        # Initialize governance knowledge base
        await self._initialize_knowledge_base()
        
        # Initialize task routing system
        await self._initialize_routing_system()
        
        # Initialize monitoring and metrics
        await self._initialize_monitoring()
    
    async def _load_configuration(self) -> None:
        """Load core brain configuration"""
        self.config = {
            "max_concurrent_tasks": settings.max_concurrent_agents,
            "task_timeout": settings.agent_timeout,
            "batch_size": settings.batch_size,
            "enable_parallel_processing": True,
            "enable_agent_communication": True,
            "enable_automatic_recovery": True
        }
    
    async def _perform_health_check(self) -> bool:
        """Perform health check for core brain agent"""
        try:
            # Check if all required specialized agents are available
            required_agents = [
                "solution_architecture",
                "technical_architecture",
                "security_architecture",
                "data_architecture",
                "integration_architecture",
                "infrastructure_architecture",
                "costing",
                "application_portfolio"
            ]
            
            available_agents = list(self.specialized_agents.keys())
            missing_agents = [agent for agent in required_agents if agent not in available_agents]
            
            if missing_agents:
                self.logger.warning(f"Missing specialized agents: {missing_agents}")
                return False
            
            # Check agent health scores
            unhealthy_agents = []
            for agent_name, agent in self.specialized_agents.items():
                if hasattr(agent, 'health_score') and agent.health_score < 50:
                    unhealthy_agents.append(agent_name)
            
            if unhealthy_agents:
                self.logger.warning(f"Unhealthy agents detected: {unhealthy_agents}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    async def _process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process governance validation task"""
        try:
            # Parse governance request
            governance_request = GovernanceRequest(**task.input_data)
            
            self.logger.info(f"Processing governance request: {governance_request.request_id}")
            
            # Determine which agents to involve
            target_agents = self._determine_target_agents(governance_request.scope)
            
            # Create subtasks for specialized agents
            subtasks = await self._create_subtasks(governance_request, target_agents)
            
            # Execute tasks in parallel
            results = await self._execute_parallel_tasks(subtasks)
            
            # Aggregate and synthesize results
            governance_response = await self._synthesize_results(
                governance_request, results
            )
            
            return governance_response.dict()
            
        except Exception as e:
            self.logger.error(f"Failed to process governance task: {e}")
            raise
    
    async def _initialize_knowledge_base(self) -> None:
        """Initialize governance knowledge base"""
        self.logger.info("Initializing governance knowledge base")
        
        # Load governance frameworks
        # Load best practices
        # Load compliance requirements
        # Load industry standards
        
        self.logger.info("Governance knowledge base initialized")
    
    async def _initialize_routing_system(self) -> None:
        """Initialize task routing system"""
        self.logger.info("Initializing task routing system")
        
        # Set up routing rules
        # Configure load balancing
        # Set up failover mechanisms
        
        self.logger.info("Task routing system initialized")
    
    async def _initialize_monitoring(self) -> None:
        """Initialize monitoring and metrics"""
        self.logger.info("Initializing monitoring system")
        
        # Set up performance monitoring
        # Configure alerting
        # Initialize metrics collection
        
        self.logger.info("Monitoring system initialized")
    
    def _determine_target_agents(self, scope: GovernanceScope) -> List[str]:
        """Determine which specialized agents to involve based on scope"""
        return self.routing_rules.get(scope, [])
    
    async def _create_subtasks(
        self, 
        governance_request: GovernanceRequest, 
        target_agents: List[str]
    ) -> List[AgentTask]:
        """Create subtasks for specialized agents"""
        subtasks = []
        
        for agent_name in target_agents:
            if agent_name in self.specialized_agents:
                subtask = AgentTask(
                    task_id=f"{governance_request.request_id}_{agent_name}",
                    agent_id=self.specialized_agents[agent_name].agent_id,
                    task_type="governance_validation",
                    priority=governance_request.priority,
                    input_data={
                        "governance_request": governance_request.dict(),
                        "agent_specific_context": self._get_agent_context(agent_name, governance_request)
                    },
                    timeout_seconds=governance_request.timeout_seconds
                )
                subtasks.append(subtask)
        
        return subtasks
    
    def _get_agent_context(self, agent_name: str, governance_request: GovernanceRequest) -> Dict[str, Any]:
        """Get agent-specific context for the governance request"""
        context = {
            "business_context": governance_request.business_context,
            "technical_context": governance_request.technical_context,
            "compliance_requirements": governance_request.compliance_requirements,
            "target_components": governance_request.target_components
        }
        
        # Add agent-specific context based on agent type
        if agent_name == "security_architecture":
            context.update({
                "security_frameworks": ["NIST", "ISO_27001", "OWASP"],
                "threat_modeling_required": True
            })
        elif agent_name == "costing":
            context.update({
                "cost_analysis_period": "monthly",
                "include_operational_costs": True
            })
        
        return context
    
    async def _execute_parallel_tasks(self, subtasks: List[AgentTask]) -> List[Dict[str, Any]]:
        """Execute tasks in parallel across specialized agents"""
        try:
            # Create tasks for each agent
            tasks = []
            for subtask in subtasks:
                agent = self.specialized_agents.get(subtask.agent_id)
                if agent and agent.status == AgentStatus.IDLE:
                    task = asyncio.create_task(agent.process_task(subtask))
                    tasks.append(task)
            
            # Execute all tasks in parallel
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                processed_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        self.logger.error(f"Task {subtasks[i].task_id} failed: {result}")
                        processed_results.append({
                            "status": "failed",
                            "error": str(result),
                            "agent": subtasks[i].agent_id
                        })
                    else:
                        processed_results.append(result)
                
                return processed_results
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Failed to execute parallel tasks: {e}")
            raise
    
    async def _synthesize_results(
        self, 
        governance_request: GovernanceRequest, 
        agent_results: List[Dict[str, Any]]
    ) -> GovernanceResponse:
        """Synthesize results from all agents into a comprehensive response"""
        try:
            # Collect all validation results
            all_validation_results = []
            risk_scores = []
            compliance_scores = []
            recommendations = []
            agents_used = []
            
            for result in agent_results:
                if result.get("status") == "completed":
                    # Extract validation results
                    if "validation_results" in result:
                        all_validation_results.extend(result["validation_results"])
                    
                    # Extract scores
                    if "risk_score" in result:
                        risk_scores.append(result["risk_score"])
                    if "compliance_score" in result:
                        compliance_scores.append(result["compliance_score"])
                    
                    # Extract recommendations
                    if "recommendations" in result:
                        recommendations.extend(result["recommendations"])
                    
                    # Track agents used
                    if "agent_id" in result:
                        agents_used.append(result["agent_id"])
            
            # Calculate overall scores
            overall_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0
            overall_compliance_score = sum(compliance_scores) / len(compliance_scores) if compliance_scores else 0.0
            
            # Determine overall status
            overall_status = self._determine_overall_status(all_validation_results)
            
            # Generate executive summary
            summary = self._generate_executive_summary(
                governance_request, all_validation_results, overall_risk_score, overall_compliance_score
            )
            
            # Generate next steps
            next_steps = self._generate_next_steps(all_validation_results, recommendations)
            
            return GovernanceResponse(
                request_id=governance_request.request_id,
                status=overall_status,
                summary=summary,
                validation_results=all_validation_results,
                risk_score=overall_risk_score,
                compliance_score=overall_compliance_score,
                recommendations=recommendations,
                next_steps=next_steps,
                processing_time_seconds=0.0,  # Will be calculated by caller
                agents_used=agents_used
            )
            
        except Exception as e:
            self.logger.error(f"Failed to synthesize results: {e}")
            raise
    
    def _determine_overall_status(self, validation_results: List[ValidationResult]) -> str:
        """Determine overall governance status based on validation results"""
        if not validation_results:
            return "unknown"
        
        # Count by status
        status_counts = {}
        for result in validation_results:
            status = result.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Determine overall status
        if status_counts.get(ValidationStatus.FAILED, 0) > 0:
            return "failed"
        elif status_counts.get(ValidationStatus.WARNING, 0) > 0:
            return "warning"
        elif status_counts.get(ValidationStatus.PASSED, 0) > 0:
            return "passed"
        else:
            return "unknown"
    
    def _generate_executive_summary(
        self,
        governance_request: GovernanceRequest,
        validation_results: List[ValidationResult],
        risk_score: float,
        compliance_score: float
    ) -> str:
        """Generate executive summary of governance validation"""
        total_validations = len(validation_results)
        passed_validations = len([r for r in validation_results if r.status == ValidationStatus.PASSED])
        failed_validations = len([r for r in validation_results if r.status == ValidationStatus.FAILED])
        warning_validations = len([r for r in validation_results if r.status == ValidationStatus.WARNING])
        
        summary = f"""
        Governance validation completed for scope: {governance_request.scope.value}
        
        Overall Results:
        - Total validations: {total_validations}
        - Passed: {passed_validations}
        - Failed: {failed_validations}
        - Warnings: {warning_validations}
        
        Scores:
        - Risk Score: {risk_score:.1f}/100
        - Compliance Score: {compliance_score:.1f}/100
        
        Status: {self._determine_overall_status(validation_results).upper()}
        """
        
        return summary.strip()
    
    def _generate_next_steps(
        self, 
        validation_results: List[ValidationResult], 
        recommendations: List[str]
    ) -> List[str]:
        """Generate next steps based on validation results and recommendations"""
        next_steps = []
        
        # Prioritize failed validations
        failed_results = [r for r in validation_results if r.status == ValidationStatus.FAILED]
        for result in failed_results:
            next_steps.append(f"Address {result.rule_name}: {result.message}")
        
        # Add high-priority recommendations
        high_priority_recs = [rec for rec in recommendations if any(
            keyword in rec.lower() for keyword in ["critical", "urgent", "immediate", "security"]
        )]
        next_steps.extend(high_priority_recs[:3])  # Limit to top 3
        
        # Add general next steps
        if not next_steps:
            next_steps.append("Review all validation results and recommendations")
            next_steps.append("Implement recommended improvements")
            next_steps.append("Schedule follow-up validation")
        
        return next_steps[:5]  # Limit to 5 next steps
    
    async def _cleanup(self) -> None:
        """Cleanup core brain agent resources"""
        self.logger.info("Cleaning up Core Brain Agent resources")
        
        # Cleanup knowledge base
        # Cleanup routing system
        # Cleanup monitoring
        
        self.logger.info("Core Brain Agent cleanup complete")
    
    def register_specialized_agent(self, agent_name: str, agent_instance: Any) -> None:
        """Register a specialized agent with the core brain"""
        self.specialized_agents[agent_name] = agent_instance
        self.logger.info(f"Registered specialized agent: {agent_name}")
    
    async def get_swarm_status(self) -> Dict[str, Any]:
        """Get status of the entire agent swarm"""
        swarm_status = {
            "core_brain": await self.get_status(),
            "specialized_agents": {},
            "overall_health": 100.0,
            "active_tasks": 0,
            "total_agents": len(self.specialized_agents) + 1
        }
        
        # Collect status from all specialized agents
        total_health = 100.0
        active_tasks = 0
        
        for agent_name, agent in self.specialized_agents.items():
            try:
                agent_status = await agent.get_status()
                swarm_status["specialized_agents"][agent_name] = agent_status
                
                total_health += agent_status.get("health_score", 100.0)
                if agent_status.get("current_task"):
                    active_tasks += 1
                    
            except Exception as e:
                self.logger.error(f"Failed to get status for {agent_name}: {e}")
                swarm_status["specialized_agents"][agent_name] = {"status": "error", "error": str(e)}
        
        # Calculate overall health
        swarm_status["overall_health"] = total_health / (len(self.specialized_agents) + 1)
        swarm_status["active_tasks"] = active_tasks
        
        return swarm_status
