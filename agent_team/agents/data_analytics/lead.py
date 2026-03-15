"""Data & Analytics Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class AnalyticsLeadAgent(BaseExecutionAgent):
    """Data & Analytics Team Lead: Data strategy, analytics, BI, ML."""

    @property
    def system_prompt(self) -> str:
        return """You are the Data & Analytics Team Lead.

Your responsibilities:
- Define data strategy
- Design analytics solutions
- Build BI dashboards
- Develop ML models
- Analyze business metrics
- Provide data-driven insights"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Analytics Task: {task.title}\n\n{task.description}\n\nProvide data and analytics solutions."""
