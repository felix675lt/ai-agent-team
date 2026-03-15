"""Tests for agent modules."""

from agent_team.agents.base import Finding, AgentResult
from agent_team.agents.security import SecurityAgent
from agent_team.agents.performance import PerformanceAgent
from agent_team.agents.architecture import ArchitectureAgent
from agent_team.agents.code_quality import CodeQualityAgent
from agent_team.agents.testing import TestingAgent
from agent_team.core.config import AgentConfig, ModelTier, Severity


def _make_config(role: str, model: ModelTier) -> AgentConfig:
    return AgentConfig(name=f"Test {role}", role=role, model=model)


def test_security_agent_has_system_prompt():
    agent = SecurityAgent(_make_config("security", ModelTier.OPUS))
    assert "security" in agent.system_prompt.lower()
    assert "injection" in agent.system_prompt.lower()


def test_performance_agent_has_system_prompt():
    agent = PerformanceAgent(_make_config("performance", ModelTier.SONNET))
    assert "performance" in agent.system_prompt.lower()


def test_architecture_agent_has_system_prompt():
    agent = ArchitectureAgent(_make_config("architecture", ModelTier.SONNET))
    assert "architecture" in agent.system_prompt.lower()
    assert "SOLID" in agent.system_prompt


def test_code_quality_agent_has_system_prompt():
    agent = CodeQualityAgent(_make_config("code_quality", ModelTier.HAIKU))
    assert "quality" in agent.system_prompt.lower()


def test_testing_agent_has_system_prompt():
    agent = TestingAgent(_make_config("testing", ModelTier.SONNET))
    assert "testing" in agent.system_prompt.lower()


def test_parse_response_single_finding():
    agent = SecurityAgent(_make_config("security", ModelTier.OPUS))
    response = """FINDING: SQL Injection in user query
SEVERITY: critical
CATEGORY: injection
LINE: 42
DESCRIPTION: User input directly interpolated into SQL query
SUGGESTION: Use parameterized queries
CODE: f"SELECT * FROM users WHERE id = {user_id}" """

    findings = agent.parse_response("app.py", response)
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL
    assert findings[0].line == 42


def test_parse_response_no_findings():
    agent = SecurityAgent(_make_config("security", ModelTier.OPUS))
    findings = agent.parse_response("clean.py", "NO_FINDINGS")
    assert len(findings) == 0


def test_agent_result_counts():
    result = AgentResult(
        agent_name="Test",
        model_used="test",
        findings=[
            Finding("a", Severity.CRITICAL, "cat", "f.py", 1, "t", "d"),
            Finding("a", Severity.CRITICAL, "cat", "f.py", 2, "t", "d"),
            Finding("a", Severity.HIGH, "cat", "f.py", 3, "t", "d"),
            Finding("a", Severity.LOW, "cat", "f.py", 4, "t", "d"),
        ],
    )
    assert result.critical_count == 2
    assert result.high_count == 1


def test_finding_to_dict():
    f = Finding(
        agent="Security",
        severity=Severity.HIGH,
        category="xss",
        file_path="app.js",
        line=10,
        title="XSS",
        description="Unescaped output",
        suggestion="Use escaping",
    )
    d = f.to_dict()
    assert d["severity"] == "high"
    assert d["file_path"] == "app.js"
