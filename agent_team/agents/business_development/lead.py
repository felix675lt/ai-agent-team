"""Business Development Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class BDLeadAgent(BaseExecutionAgent):
    """Business Development Team Lead: Partnerships, sales, growth."""

    @property
    def system_prompt(self) -> str:
        return """You are the Business Development Team Lead.

Your responsibilities:
- Develop partnership strategies
- Plan sales initiatives
- Identify business opportunities
- Create business plans
- Analyze markets and competitors
- Drive business growth"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""BD Task: {task.title}\n\n{task.description}\n\nProvide business development strategies."""
