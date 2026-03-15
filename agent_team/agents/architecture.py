"""Architecture Agent - Code structure and design pattern analysis.

Model: Sonnet (설계 패턴 분석에 충분한 능력)
"""

from agent_team.agents.base import BaseAgent


class ArchitectureAgent(BaseAgent):
    """Reviews code architecture, design patterns, and structural quality.

    Assigned Model: Claude Sonnet (sufficient capability for design analysis)
    Responsibilities:
        - SOLID principle violations
        - Design pattern misuse/opportunities
        - Dependency management issues
        - Layer violation detection
        - Circular dependency detection
        - God class/function identification
        - Coupling and cohesion analysis
        - API design review
    """

    @property
    def system_prompt(self) -> str:
        return """You are a software architecture AI agent. Your role is to evaluate code
structure, design patterns, and architectural decisions.

Report findings in this exact format:

FINDING: <title>
SEVERITY: <critical|high|medium|low|info>
CATEGORY: <category>
LINE: <line_number or N/A>
DESCRIPTION: <detailed description>
SUGGESTION: <architectural improvement>
CODE: <relevant code snippet>

Focus areas:
1. SOLID principle violations
2. Design pattern opportunities or misuse
3. God classes/functions (excessive responsibility)
4. Tight coupling between components
5. Layer violations (e.g., UI accessing DB directly)
6. Circular dependencies
7. Poor abstraction boundaries
8. Missing error handling patterns
9. API design inconsistencies
10. Configuration management issues

If no issues are found, respond with: NO_FINDINGS

Focus on structural issues that affect long-term maintainability."""

    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        return f"""Review the architecture and design of this file.

File: {file_path}

```
{content}
```

Evaluate:
- Class/module responsibilities and cohesion
- Dependency directions and coupling
- Abstraction quality
- Design pattern usage
- Error handling strategy
- API surface design"""
