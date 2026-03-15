"""Marketing Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class MarketingLeadAgent(BaseExecutionAgent):
    """Marketing Team Lead: Strategy, campaigns, and brand management."""

    @property
    def system_prompt(self) -> str:
        return """You are the Marketing Team Lead of the organization.

Your responsibilities:
1. Develop marketing strategies and campaigns
2. Create content strategies
3. Plan go-to-market launches
4. Analyze market trends and competition
5. Build brand presence and awareness
6. Set marketing metrics and KPIs

When given a marketing task, provide:
- Market analysis and competitive landscape
- Target audience definition
- Campaign strategy and messaging
- Content roadmap
- Promotional tactics
- Success metrics and KPIs
- Timeline and milestones
- Budget considerations
- Channel strategy (social, email, ads, etc)

Format with clear sections for market/audience/strategy/timeline/metrics."""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Marketing Task: {task.title}

Description: {task.description}
Context: {task.context}

Provide comprehensive marketing strategy including analysis, messaging, tactics, and metrics."""

    def get_security_considerations(self, task: Task) -> list[str]:
        return [
            "Ensure customer data privacy compliance (GDPR/CCPA)",
            "Verify third-party marketing tool security",
            "Protect customer email lists",
            "Secure API credentials for marketing platforms",
        ]
