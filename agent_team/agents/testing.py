"""Testing Agent - Test coverage and test quality analysis.

Model: Sonnet (테스트 분석에 적합한 균형 모델)
"""

from agent_team.agents.base import BaseAgent


class TestingAgent(BaseAgent):
    """Analyzes test coverage, test quality, and testing strategy.

    Assigned Model: Claude Sonnet (balanced capability for test analysis)
    Responsibilities:
        - Test coverage gap identification
        - Test quality assessment
        - Missing edge case detection
        - Test isolation issues
        - Flaky test pattern detection
        - Mock/stub misuse
        - Assertion quality
        - Integration test opportunities
    """

    @property
    def system_prompt(self) -> str:
        return """You are a testing strategy AI agent. Your role is to identify testing
gaps, quality issues, and suggest improvements to test suites.

Report findings in this exact format:

FINDING: <title>
SEVERITY: <critical|high|medium|low|info>
CATEGORY: <category>
LINE: <line_number or N/A>
DESCRIPTION: <description>
SUGGESTION: <testing improvement>
CODE: <relevant snippet>

Focus areas:
1. Untested code paths and edge cases
2. Missing error/exception test cases
3. Test isolation problems (shared state)
4. Flaky test patterns (timing, order dependency)
5. Insufficient assertions
6. Over-mocking (testing implementation, not behavior)
7. Missing integration/E2E tests
8. Boundary value test gaps
9. Missing negative test cases
10. Test naming and organization

If no issues are found, respond with: NO_FINDINGS

For source files without tests, suggest key test cases needed."""

    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        return f"""Analyze testing quality and coverage for this file.

File: {file_path}

```
{content}
```

If this is a test file: evaluate test quality, coverage, and patterns.
If this is a source file: identify what tests are missing or needed."""
