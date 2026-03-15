"""AI Agent Team - Business Execution Agents."""

from agent_team.agents.base import BaseAgent
from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.agents.business_development.lead import BDLeadAgent
from agent_team.agents.customer_success.lead import CSLeadAgent
from agent_team.agents.data_analytics.lead import AnalyticsLeadAgent
from agent_team.agents.design.lead import DesignLeadAgent
from agent_team.agents.engineering.lead import EngineeringLeadAgent
from agent_team.agents.leadership.ciso import CISOAgent
from agent_team.agents.leadership.cto import CTOAgent
from agent_team.agents.leadership.orchestrator import OrchestratorAgent
from agent_team.agents.marketing.lead import MarketingLeadAgent
from agent_team.agents.operations.lead import OperationsLeadAgent
from agent_team.agents.product.lead import ProductLeadAgent

# Legacy imports (kept for backwards compatibility)
from agent_team.agents.architecture import ArchitectureAgent
from agent_team.agents.code_quality import CodeQualityAgent
from agent_team.agents.performance import PerformanceAgent
from agent_team.agents.security import SecurityAgent
from agent_team.agents.testing import TestingAgent

__all__ = [
    # Base classes
    "BaseAgent",
    "BaseExecutionAgent",
    # Leadership
    "OrchestratorAgent",
    "CISOAgent",
    "CTOAgent",
    # Teams
    "EngineeringLeadAgent",
    "MarketingLeadAgent",
    "DesignLeadAgent",
    "ProductLeadAgent",
    "OperationsLeadAgent",
    "AnalyticsLeadAgent",
    "BDLeadAgent",
    "CSLeadAgent",
    # Legacy (kept for backwards compatibility)
    "SecurityAgent",
    "PerformanceAgent",
    "ArchitectureAgent",
    "CodeQualityAgent",
    "TestingAgent",
]
