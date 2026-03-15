"""Core orchestration and configuration."""

from .config import AgentConfig, TeamConfig

__all__ = ["AgentConfig", "TeamConfig"]


def get_orchestrator():
    """Lazy import to avoid circular dependencies."""
    from .orchestrator import Orchestrator
    return Orchestrator
