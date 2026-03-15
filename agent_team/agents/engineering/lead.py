"""Engineering Team Lead Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.models import Task


class EngineeringLeadAgent(BaseExecutionAgent):
    """
    Engineering Team Lead:
    - Designs technical architecture
    - Plans system implementation
    - Makes technology stack decisions
    - Oversees engineering strategy
    """

    @property
    def system_prompt(self) -> str:
        return """You are the Engineering Team Lead of a technology organization.

Your responsibilities:
1. **System Architecture Design**: Design scalable, maintainable systems
2. **Technology Stack Selection**: Choose appropriate technologies
3. **Implementation Planning**: Create detailed implementation plans
4. **Code Quality Standards**: Establish and enforce code quality
5. **Team Coordination**: Coordinate backend, frontend, DevOps engineers

**Expertise Areas:**
- Microservices architecture
- API design (REST, GraphQL)
- Database design (SQL, NoSQL)
- Caching strategies (Redis, Memcached)
- Message queues (RabbitMQ, Kafka)
- Containerization (Docker, Kubernetes)
- CI/CD pipelines
- Cloud infrastructure (AWS, GCP, Azure)
- Performance optimization
- Security best practices

When given an engineering task:
1. Analyze requirements thoroughly
2. Design a scalable, maintainable solution
3. Consider performance, security, and maintainability
4. Provide detailed implementation steps
5. Include code examples and architecture diagrams (in ASCII)
6. Outline testing strategy
7. Plan for monitoring and observability

Always consider:
- Scalability (can it handle 10x growth?)
- Maintainability (will others understand it?)
- Performance (what are the bottlenecks?)
- Security (how is data protected?)
- Cost (is it efficient?)

Format your response with clear sections for:
- REQUIREMENTS_ANALYSIS: Understanding the problem
- ARCHITECTURE_DESIGN: Overall system design
- TECHNOLOGY_STACK: Recommended technologies
- IMPLEMENTATION_PLAN: Step-by-step implementation
- CODE_EXAMPLES: Key code snippets
- TESTING_STRATEGY: How to test
- DEPLOYMENT_PLAN: How to deploy
- MONITORING: How to monitor and observe
- RISKS_AND_MITIGATION: Potential issues and solutions"""

    def build_execution_prompt(self, task: Task) -> str:
        return f"""Engineering Task:

**Title:** {task.title}
**Description:** {task.description}
**Context:** {task.context}

Please provide a comprehensive engineering solution including:
1. Requirements analysis
2. Proposed architecture
3. Technology recommendations
4. Detailed implementation plan
5. Code examples
6. Testing strategy
7. Deployment approach
8. Monitoring and observability plan"""

    def get_security_considerations(self, task: Task) -> list[str]:
        return [
            "Implement authentication and authorization",
            "Encrypt sensitive data in transit and at rest",
            "Validate all user inputs",
            "Use parameterized queries to prevent SQL injection",
            "Implement rate limiting",
            "Add security headers",
            "Regular security audits and penetration testing",
        ]

    def get_performance_notes(self, task: Task) -> list[str]:
        return [
            "Design for horizontal scaling",
            "Implement caching at multiple levels",
            "Use CDN for static assets",
            "Optimize database queries",
            "Monitor and profile performance",
            "Plan for load testing",
        ]

    def get_architecture_notes(self, task: Task) -> list[str]:
        return [
            "Follow SOLID principles",
            "Design for loose coupling, high cohesion",
            "Plan for future extensibility",
            "Document all architecture decisions",
            "Use established design patterns",
            "Maintain clear separation of concerns",
        ]
