"""Tests for configuration module."""

from pathlib import Path
import tempfile

from agent_team.core.config import AgentConfig, ModelTier, TeamConfig


def test_default_config_has_all_agents():
    config = TeamConfig.default()
    assert "security" in config.agents
    assert "architecture" in config.agents
    assert "performance" in config.agents
    assert "code_quality" in config.agents
    assert "testing" in config.agents


def test_security_uses_opus():
    config = TeamConfig.default()
    assert config.agents["security"].model == ModelTier.OPUS


def test_code_quality_uses_haiku():
    config = TeamConfig.default()
    assert config.agents["code_quality"].model == ModelTier.HAIKU


def test_yaml_roundtrip():
    config = TeamConfig.default()
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        path = Path(f.name)

    config.to_yaml(path)
    loaded = TeamConfig.from_yaml(path)

    assert set(loaded.agents.keys()) == set(config.agents.keys())
    assert loaded.agents["security"].model == ModelTier.OPUS
    path.unlink()


def test_agent_config_defaults():
    agent = AgentConfig(name="Test", role="test", model=ModelTier.SONNET)
    assert agent.enabled is True
    assert agent.max_files_per_run == 50
    assert agent.timeout_seconds == 120
