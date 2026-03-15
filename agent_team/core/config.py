"""Configuration for agent team."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml


class ModelTier(str, Enum):
    """Claude model tiers with different capability/cost tradeoffs."""

    OPUS = "claude-opus-4-6"
    SONNET = "claude-sonnet-4-6"
    HAIKU = "claude-haiku-4-5-20251001"


class Severity(str, Enum):
    """Issue severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class AgentConfig:
    """Configuration for a single agent."""

    name: str
    role: str
    model: ModelTier
    team_name: str = ""  # e.g., "Engineering Team", "Marketing Team"
    enabled: bool = True
    max_files_per_run: int = 50
    timeout_seconds: int = 120
    custom_rules: list[str] = field(default_factory=list)


@dataclass
class TeamConfig:
    """Configuration for the entire agent team."""

    agents: dict[str, AgentConfig] = field(default_factory=dict)
    parallel: bool = True
    output_format: str = "rich"  # rich, json, markdown
    target_path: str = "."
    exclude_patterns: list[str] = field(
        default_factory=lambda: [
            "node_modules",
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "dist",
            "build",
            ".egg-info",
        ]
    )

    @classmethod
    def default(cls) -> TeamConfig:
        """Create default team configuration with recommended model assignments."""
        return cls(
            agents={
                "security": AgentConfig(
                    name="Security Agent",
                    role="security",
                    model=ModelTier.OPUS,
                ),
                "architecture": AgentConfig(
                    name="Architecture Agent",
                    role="architecture",
                    model=ModelTier.SONNET,
                ),
                "performance": AgentConfig(
                    name="Performance Agent",
                    role="performance",
                    model=ModelTier.SONNET,
                ),
                "code_quality": AgentConfig(
                    name="Code Quality Agent",
                    role="code_quality",
                    model=ModelTier.HAIKU,
                ),
                "testing": AgentConfig(
                    name="Testing Agent",
                    role="testing",
                    model=ModelTier.SONNET,
                ),
            }
        )

    @classmethod
    def from_yaml(cls, path: Path) -> TeamConfig:
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        config = cls.default()

        if "agents" in data:
            for key, agent_data in data["agents"].items():
                if key in config.agents:
                    for attr, value in agent_data.items():
                        if attr == "model":
                            value = ModelTier(value)
                        setattr(config.agents[key], attr, value)

        for key in ("parallel", "output_format", "target_path", "exclude_patterns"):
            if key in data:
                setattr(config, key, data[key])

        return config

    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        data: dict[str, Any] = {
            "agents": {},
            "parallel": self.parallel,
            "output_format": self.output_format,
            "exclude_patterns": self.exclude_patterns,
        }
        for key, agent in self.agents.items():
            data["agents"][key] = {
                "name": agent.name,
                "role": agent.role,
                "model": agent.model.value,
                "enabled": agent.enabled,
                "max_files_per_run": agent.max_files_per_run,
                "timeout_seconds": agent.timeout_seconds,
                "custom_rules": agent.custom_rules,
            }

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
