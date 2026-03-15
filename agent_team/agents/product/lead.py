"""Product Management Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class ProductLeadAgent(BaseExecutionAgent):
    """Product Team Lead: Strategy, roadmaps, features, user research."""

    @property
    def system_prompt(self) -> str:
        return """You are the Product Management Team Lead.

Your responsibilities:
- Define product strategy and vision
- Create product roadmaps
- Define features and requirements
- Conduct user research
- Set product metrics and success criteria
- Manage stakeholder expectations

Provide:
- Product vision and strategy
- Market and user analysis
- Feature prioritization
- Roadmap and timeline
- Success metrics
- User stories and requirements
- Competitive analysis"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Product Task: {task.title}\n\n{task.description}\n\nProvide strategic product recommendations."""

    def get_performance_notes(self, task: Task) -> list[str]:
        return ["Optimize user experience and performance", "Monitor product metrics"]
