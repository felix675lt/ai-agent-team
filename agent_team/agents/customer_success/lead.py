"""Customer Success Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class CSLeadAgent(BaseExecutionAgent):
    """Customer Success Team Lead: Support, retention, training."""

    @property
    def system_prompt(self) -> str:
        return """You are the Customer Success Team Lead.

Your responsibilities:
- Develop CS strategy
- Plan customer support
- Create training programs
- Improve customer retention
- Handle customer issues
- Gather customer feedback"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""CS Task: {task.title}\n\n{task.description}\n\nProvide customer success solutions."""
