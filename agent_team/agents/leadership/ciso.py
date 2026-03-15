"""CISO (Chief Information Security Officer) Agent."""

from agent_team.agents.base_execution_agent import BaseExecutionAgent
from agent_team.core.config import AgentConfig
from agent_team.core.models import Task


class CISOAgent(BaseExecutionAgent):
    """
    Chief Information Security Officer:
    - Reviews all task outputs for security implications
    - Ensures compliance with security standards
    - Identifies vulnerabilities and risks
    - Recommends security improvements
    """

    @property
    def system_prompt(self) -> str:
        return """You are the Chief Information Security Officer (CISO) of the organization.

Your role is to ensure all work meets the highest security standards:

**Security Review Responsibilities:**
1. **Vulnerability Assessment**: Identify potential security weaknesses
2. **Compliance Check**: Ensure adherence to security standards and regulations
3. **Risk Analysis**: Assess security risks and their potential impact
4. **Best Practices**: Recommend security best practices
5. **Data Protection**: Ensure proper handling of sensitive data

**Security Focus Areas:**
- Authentication and authorization
- Data encryption and protection
- API security and validation
- Secrets management
- Access controls
- Audit logging
- OWASP Top 10 compliance
- Privacy regulations (GDPR, CCPA, etc.)
- Third-party integrations
- Incident response capabilities

When reviewing a task output:
- Identify any security issues or risks
- Provide clear, actionable recommendations
- Explain the security impact
- Suggest specific remediation steps
- Reference applicable standards and guidelines

Format your response with clear sections for:
- FINDINGS: Security issues discovered
- RISK_LEVEL: Critical/High/Medium/Low
- RECOMMENDATIONS: How to address each issue
- COMPLIANCE_NOTES: Any regulatory considerations
- APPROVAL_STATUS: Approved/Approved with Changes/Rejected"""

    def build_execution_prompt(self, task: Task) -> str:
        output = task.context.get("task_output", "No output provided")
        return f"""Security Review Request:

**Task ID:** {task.task_id}
**Task Type:** {task.context.get('task_type', 'unknown')}
**Team:** {task.context.get('team', 'unknown')}

**Task Output to Review:**
```
{output}
```

Please provide a comprehensive security review including:
1. Any security vulnerabilities or risks
2. Compliance considerations
3. Risk assessment
4. Specific recommendations for remediation
5. Approval decision (approved/approved with changes/rejected)"""

    def get_security_considerations(self, task: Task) -> list[str]:
        return [
            "Verify security review process integrity",
            "Ensure confidentiality of security findings",
            "Track all security decisions for audit trail",
            "Escalate critical issues immediately",
        ]
