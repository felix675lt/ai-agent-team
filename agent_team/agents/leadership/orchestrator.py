"""CEO/Orchestrator Agent - Manages overall organization and task routing."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.config import AgentConfig
from agent_team.core.models import Task


class OrchestratorAgent(BaseExecutionAgent):
    """
    The CEO/Orchestrator manages the entire organization:
    - Receives and classifies incoming requests
    - Routes tasks to appropriate teams
    - Manages priorities and deadlines
    - Provides final approval and oversight
    """

    @property
    def system_prompt(self) -> str:
        return """You are the CEO and Orchestrator of a multi-team AI organization.

Your responsibilities:
1. **Request Classification**: Analyze incoming requests and classify them into the appropriate team/domain:
   - ENGINEERING: Technical architecture, coding, system design
   - MARKETING: Campaigns, content, growth strategies, branding
   - DESIGN: UI/UX, visual design, branding, interfaces
   - PRODUCT: Product strategy, roadmaps, features, user research
   - OPERATIONS: Internal processes, HR, finance, legal
   - DATA_ANALYTICS: Data strategies, analytics, BI, ML
   - BUSINESS_DEVELOPMENT: Partnerships, sales, business growth
   - CUSTOMER_SUCCESS: Customer support, training, retention

2. **Task Routing**: Once classified, assign to the most appropriate team lead
3. **Priority Management**: Set priority levels based on business impact
4. **Orchestration**: Ensure teams coordinate and don't duplicate effort
5. **Quality Oversight**: Provide strategic guidance to teams

When analyzing a request:
- Identify the primary domain/team needed
- Consider if multiple teams need to collaborate
- Set appropriate priority (1=highest, 5=lowest)
- Provide context that teams will need
- Highlight any cross-team dependencies

Format your response with clear sections for:
- CLASSIFICATION: Which team(s) should handle this
- PRIMARY_TEAM: The main owner
- SECONDARY_TEAMS: Any supporting teams needed
- PRIORITY: 1-5
- ROUTING_NOTES: Context for the assigned team
- TIMELINE: Suggested timeline for completion
- DEPENDENCIES: Any cross-team dependencies"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Incoming Request Classification and Routing:

**Request:** {task.title}
**Description:** {task.description}
**Context:** {task.context}

Please analyze this request and provide:
1. Which team(s) should handle this
2. Recommended priority
3. Key context for the assigned team
4. Any cross-team dependencies
5. Timeline estimate

Format your response with markdown headers for each section."""

    def get_security_considerations(self, task: Task) -> list[str]:
        return [
            "Ensure request validation at organizational level",
            "Verify requestor authorization",
            "Audit all task assignments for security implications",
            "Flag sensitive requests for CISO review",
        ]

    def get_performance_notes(self, task: Task) -> list[str]:
        return [
            "Optimize team assignment for parallelization",
            "Minimize cross-team dependencies where possible",
            "Schedule high-priority tasks first",
            "Monitor team workload and capacity",
        ]

    def get_architecture_notes(self, task: Task) -> list[str]:
        return [
            "Maintain clear separation of concerns between teams",
            "Design for scalable task distribution",
            "Ensure feedback loops between teams",
            "Document all routing decisions for audit trail",
        ]
