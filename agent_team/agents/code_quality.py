"""Code Quality Agent - Style, readability, and best practices.

Model: Haiku (빠른 처리 우선 - 린트/스타일 체크)
"""

from agent_team.agents.base import BaseAgent


class CodeQualityAgent(BaseAgent):
    """Checks code style, readability, and adherence to best practices.

    Assigned Model: Claude Haiku (fast processing for lint-style checks)
    Responsibilities:
        - Naming conventions
        - Code duplication detection
        - Dead code identification
        - Magic numbers/strings
        - Comment quality
        - Import organization
        - Type annotation coverage
        - Complexity metrics (cyclomatic)
    """

    @property
    def system_prompt(self) -> str:
        return """You are a code quality AI agent. Your role is to identify code quality
issues, style violations, and maintainability concerns.

Report findings in this exact format:

FINDING: <title>
SEVERITY: <critical|high|medium|low|info>
CATEGORY: <category>
LINE: <line_number or N/A>
DESCRIPTION: <description>
SUGGESTION: <improvement>
CODE: <relevant snippet>

Focus areas:
1. Naming convention violations
2. Code duplication (DRY violations)
3. Dead/unreachable code
4. Magic numbers and hardcoded strings
5. Missing or misleading comments
6. Excessive function/method length
7. High cyclomatic complexity
8. Inconsistent error handling
9. Missing type annotations (where applicable)
10. Import organization issues

If no issues are found, respond with: NO_FINDINGS

Keep suggestions practical and actionable. Prioritize readability."""

    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        return f"""Review code quality and style of this file.

File: {file_path}

```
{content}
```

Check for readability, maintainability, and best practice adherence."""
