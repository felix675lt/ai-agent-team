"""Task dispatcher - routes tasks to appropriate teams and agents."""

import uuid
from datetime import datetime

from agent_team.agents import (
    AnalyticsLeadAgent,
    BDLeadAgent,
    CSLeadAgent,
    DesignLeadAgent,
    EngineeringLeadAgent,
    MarketingLeadAgent,
    OperationsLeadAgent,
    OrchestratorAgent,
    ProductLeadAgent,
)
from agent_team.core.config import AgentConfig, ModelTier
from agent_team.core.models import Task, TaskResult, TaskStatus, TaskType


class TaskDispatcher:
    """Dispatcher that routes tasks to appropriate teams and agents."""

    def __init__(self):
        """Initialize the dispatcher with all teams."""
        self.teams = {
            TaskType.ENGINEERING: ("Engineering Team", EngineeringLeadAgent),
            TaskType.MARKETING: ("Marketing Team", MarketingLeadAgent),
            TaskType.DESIGN: ("Design Team", DesignLeadAgent),
            TaskType.PRODUCT: ("Product Management", ProductLeadAgent),
            TaskType.OPERATIONS: ("Operations Team", OperationsLeadAgent),
            TaskType.DATA_ANALYTICS: ("Data & Analytics", AnalyticsLeadAgent),
            TaskType.BUSINESS_DEVELOPMENT: ("Business Development", BDLeadAgent),
            TaskType.CUSTOMER_SUCCESS: ("Customer Success", CSLeadAgent),
        }

        # Initialize all team agents
        self.agents = {}
        for task_type, (team_name, agent_class) in self.teams.items():
            config = AgentConfig(
                name=f"{team_name} Lead",
                team_name=team_name,
                role=task_type.value,
                model=ModelTier.OPUS,
                enabled=True,
            )
            self.agents[task_type] = agent_class(config)

    def dispatch_task(self, task_type: TaskType, title: str, description: str, context: dict = None) -> Task:
        """Create and dispatch a task to the appropriate team."""
        task = Task(
            task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            task_type=task_type,
            title=title,
            description=description,
            context=context or {},
        )

        team_name, _ = self.teams.get(task_type, ("Unknown", None))
        task.assigned_team = team_name
        task.assigned_agent = self.agents[task_type].config.name
        task.status = TaskStatus.IN_PROGRESS

        return task

    def execute_task(self, task: Task) -> TaskResult:
        """Execute a task using the appropriate agent."""
        agent = self.agents.get(task.task_type)
        if not agent:
            result = TaskResult(
                task_id=task.task_id,
                team_name="Unknown",
                agent_name="Unknown",
                status=TaskStatus.REJECTED,
                output={"error": f"No agent found for task type: {task.task_type}"},
                summary=f"Task rejected: unknown task type {task.task_type}",
            )
            result.completed_at = datetime.now()
            return result

        return agent.execute_task(task)

    def list_available_teams(self) -> list[tuple[str, str]]:
        """List all available teams."""
        return [(task_type.value, team_name) for task_type, (team_name, _) in self.teams.items()]
