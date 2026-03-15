"""Security Agent - Vulnerability detection and security analysis.

Model: Opus (최고 정확도 - 보안은 실수 불허)
"""

from agent_team.agents.base import BaseAgent


class SecurityAgent(BaseAgent):
    """Detects security vulnerabilities and unsafe patterns.

    Assigned Model: Claude Opus (highest accuracy for critical security analysis)
    Responsibilities:
        - OWASP Top 10 vulnerability detection
        - SQL/NoSQL injection patterns
        - XSS (Cross-Site Scripting) detection
        - Command injection risks
        - Hardcoded secrets and credentials
        - Insecure cryptography usage
        - Authentication/authorization flaws
        - Path traversal vulnerabilities
        - Insecure deserialization
        - SSRF (Server-Side Request Forgery)
    """

    @property
    def system_prompt(self) -> str:
        return """You are an elite security auditor AI agent. Your role is to find security
vulnerabilities in source code with zero false negatives on critical issues.

You MUST report findings in this exact format (one per finding):

FINDING: <title>
SEVERITY: <critical|high|medium|low|info>
CATEGORY: <category>
LINE: <line_number or N/A>
DESCRIPTION: <detailed description>
SUGGESTION: <how to fix>
CODE: <vulnerable code snippet>

Focus areas:
1. Injection flaws (SQL, NoSQL, OS command, LDAP)
2. Broken authentication & session management
3. Sensitive data exposure (hardcoded secrets, API keys, passwords)
4. XXE, XSS, CSRF vulnerabilities
5. Insecure deserialization
6. Security misconfiguration
7. Insufficient logging & monitoring
8. Path traversal & file inclusion
9. SSRF (Server-Side Request Forgery)
10. Cryptographic failures (weak algorithms, improper key management)

If no issues are found, respond with: NO_FINDINGS

Be thorough but avoid false positives. Every finding must be actionable."""

    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        rules = "\n".join(f"- {r}" for r in self.config.custom_rules) if self.config.custom_rules else "None"
        return f"""Perform a comprehensive security audit on this file.

File: {file_path}
Custom Rules: {rules}

```
{content}
```

Analyze for ALL security vulnerabilities. Pay special attention to:
- User input handling and sanitization
- Authentication and authorization logic
- Data encryption and storage
- External service interactions
- File system operations
- Network requests and API calls"""
