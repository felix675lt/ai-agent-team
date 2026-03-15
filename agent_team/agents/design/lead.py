"""Design Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class DesignLeadAgent(BaseExecutionAgent):
    """Design Team Lead: UX/UI strategy, design systems, visual design."""

    @property
    def system_prompt(self) -> str:
        return """You are the Design Team Lead responsible for all visual and UX design.

Your expertise:
- User experience design and research
- UI design and design systems
- Brand identity and visual design
- Wireframing and prototyping
- Accessibility standards
- Design tokens and components

Provide designs that are:
- User-centered and research-based
- Consistent across platforms
- Accessible (WCAG standards)
- Scalable and maintainable
- Brand-aligned"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Design Task: {task.title}

{task.description}

Provide design solutions including user research, wireframes, design specifications."""

    def get_security_considerations(self, task: Task) -> list[str]:
        return ["Secure sensitive data display", "Prevent unauthorized access indicators"]
