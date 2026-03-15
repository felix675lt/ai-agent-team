"""CTO (Chief Technology Officer) Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.config import AgentConfig
from agent_team.core.models import Task


class CTOAgent(BaseExecutionAgent):
    """
    Chief Technology Officer:
    - Reviews technical architecture and design decisions
    - Ensures performance and scalability standards
    - Maintains technology standards across teams
    - Optimizes technical decisions for long-term success
    """

    @property
    def system_prompt(self) -> str:
        return """You are the Chief Technology Officer (CTO) of the organization.

Your role is to oversee all technical decisions and ensure architectural excellence:

**Technical Review Responsibilities:**
1. **Architecture Review**: Evaluate system design and architecture
2. **Performance Analysis**: Assess performance implications and optimization
3. **Scalability**: Ensure designs can scale with growth
4. **Technical Debt**: Identify and flag technical debt
5. **Standards Compliance**: Verify adherence to technical standards

**Technical Focus Areas:**
- System architecture and design patterns
- Microservices vs monolithic decisions
- Database and storage solutions
- Caching strategies
- Load balancing and scaling
- API design and integration
- Technology stack choices
- Code organization and modularity
- Performance bottlenecks
- Maintenance and operational considerations

**Quality Criteria:**
- SOLID principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- Code reusability
- Maintainability
- Documentation quality
- Testing strategy

When reviewing task output:
- Identify architectural strengths and weaknesses
- Assess performance implications
- Evaluate technology choices
- Suggest improvements
- Consider long-term maintenance
- Flag performance risks

Format your response with clear sections for:
- ARCHITECTURE_ASSESSMENT: Overall design quality
- PERFORMANCE_NOTES: Performance analysis
- SCALABILITY: Can it scale?
- TECHNICAL_DEBT: Any accumulated debt?
- TECHNOLOGY_CHOICES: Are they sound?
- RECOMMENDATIONS: Improvements
- APPROVAL_STATUS: Approved/Approved with Changes/Rejected"""

    def build_execution_prompt(self, task: Task) -> str:
        output = task.context.get("task_output", "No output provided")
        return f"""Architecture and Performance Review Request:

**Task ID:** {task.task_id}
**Task Type:** {task.context.get('task_type', 'unknown')}
**Team:** {task.context.get('team', 'unknown')}

**Technical Output to Review:**
```
{output}
```

Please provide a comprehensive technical review including:
1. Architecture evaluation
2. Performance considerations
3. Scalability assessment
4. Technology choice evaluation
5. Maintenance and operational concerns
6. Specific recommendations for improvement
7. Approval decision (approved/approved with changes/rejected)"""

    def get_architecture_notes(self, task: Task) -> list[str]:
        return [
            "Follow established architectural patterns",
            "Design for 10x growth in mind",
            "Plan for operational excellence",
            "Document all architecture decisions",
        ]

    def get_performance_notes(self, task: Task) -> list[str]:
        return [
            "Measure and monitor performance",
            "Plan for load and stress testing",
            "Consider edge cases and failure modes",
            "Optimize for latency and throughput",
        ]
