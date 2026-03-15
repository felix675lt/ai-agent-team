"""Performance Agent - Performance analysis and optimization suggestions.

Model: Sonnet (패턴 기반 분석에 적합한 균형 모델)
"""

from agent_team.agents.base import BaseAgent


class PerformanceAgent(BaseAgent):
    """Identifies performance bottlenecks and optimization opportunities.

    Assigned Model: Claude Sonnet (balanced accuracy/speed for pattern analysis)
    Responsibilities:
        - Algorithm complexity analysis (Big-O)
        - Memory leak detection
        - N+1 query patterns
        - Unnecessary allocations
        - Cache optimization opportunities
        - Async/concurrency anti-patterns
        - Database query optimization
        - I/O bottleneck detection
    """

    @property
    def system_prompt(self) -> str:
        return """You are a performance engineering AI agent. Your role is to identify
performance bottlenecks, inefficiencies, and optimization opportunities in code.

Report findings in this exact format:

FINDING: <title>
SEVERITY: <critical|high|medium|low|info>
CATEGORY: <category>
LINE: <line_number or N/A>
DESCRIPTION: <detailed description with complexity analysis>
SUGGESTION: <optimization approach>
CODE: <problematic code snippet>

Focus areas:
1. Algorithm complexity (O(n²) loops, unnecessary iterations)
2. Memory leaks and excessive allocations
3. N+1 query problems in database access
4. Blocking I/O in async contexts
5. Missing caching opportunities
6. Unnecessary deep copies or serialization
7. Inefficient data structure choices
8. Redundant computations
9. Connection pool exhaustion risks
10. Large payload processing without streaming

If no issues are found, respond with: NO_FINDINGS

Quantify impact where possible (e.g., "O(n²) → O(n log n)")."""

    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        return f"""Analyze this file for performance issues and optimization opportunities.

File: {file_path}

```
{content}
```

Look for:
- Hot loops and algorithmic inefficiency
- Memory usage patterns
- Database and I/O patterns
- Concurrency issues
- Data structure choices
- Caching opportunities"""
