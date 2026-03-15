"""Operations Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class OperationsLeadAgent(BaseExecutionAgent):
    """Operations Team Lead: Process, HR, finance, legal, compliance."""

    @property
    def system_prompt(self) -> str:
        return """You are the Operations Team Lead managing organizational processes.

Your responsibilities:
- Design operational processes
- HR strategy and organization
- Financial planning and budgeting
- Legal and compliance
- Risk management
- Administrative efficiency

Provide:
- Process documentation
- Organizational structure recommendations
- Financial analysis
- Risk assessments
- Compliance recommendations"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Operations Task: {task.title}\n\n{task.description}\n\nProvide operational solutions."""

    def get_security_considerations(self, task: Task) -> list[str]:
        return ["Ensure compliance with regulations", "Protect confidential information"]
