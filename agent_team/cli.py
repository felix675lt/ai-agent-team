"""CLI interface for AI Agent Team."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_team.core.config import ModelTier, TeamConfig
from agent_team.core.orchestrator import Orchestrator

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="ai-agent-team")
def main():
    """AI Agent Team — Autonomous code review with specialized agents.

    Each agent uses a different Claude model tier optimized for its role:

    \b
    🔒 Security Agent  → Opus   (highest accuracy, zero-miss on critical)
    🏗️  Architecture    → Sonnet (balanced, design pattern analysis)
    ⚡ Performance     → Sonnet (balanced, pattern-based optimization)
    📝 Code Quality    → Haiku  (fast, lint-style checks)
    🧪 Testing         → Sonnet (balanced, test strategy analysis)
    """


@main.command()
@click.argument("target", default=".")
@click.option("--config", "-c", type=click.Path(exists=True), help="YAML config file")
@click.option("--output", "-o", type=click.Choice(["rich", "json", "markdown"]), default="rich")
@click.option("--save", "-s", type=click.Path(), help="Save report to file")
@click.option("--sequential", is_flag=True, help="Run agents sequentially instead of parallel")
@click.option("--agents", "-a", multiple=True, help="Run only specific agents (e.g., -a security -a performance)")
def analyze(target: str, config: str | None, output: str, save: str | None, sequential: bool, agents: tuple[str, ...]):
    """Run the full agent team analysis on TARGET directory or file."""
    console.print(Panel(
        "[bold]AI Agent Team[/bold] — Autonomous Code Analysis\n"
        "Coordinated by [cyan]Orchestrator (Opus)[/cyan]",
        style="bold blue",
    ))

    # Load config
    if config:
        team_config = TeamConfig.from_yaml(Path(config))
    else:
        team_config = TeamConfig.default()

    team_config.output_format = output

    if sequential:
        team_config.parallel = False

    # Filter agents if specified
    if agents:
        for key in list(team_config.agents.keys()):
            if key not in agents:
                team_config.agents[key].enabled = False

    # Show team roster
    _show_roster(team_config)

    # Run analysis
    orchestrator = Orchestrator(team_config)
    report = orchestrator.run(target)

    # Save report
    if save:
        save_path = Path(save)
        if output == "json":
            save_path.write_text(report.to_json())
        else:
            save_path.write_text(report.to_markdown())
        console.print(f"\n📄 Report saved to [bold]{save}[/bold]")


@main.command()
@click.option("--output", "-o", type=click.Path(), default="agent-team.yaml")
def init(output: str):
    """Generate a default configuration file."""
    config = TeamConfig.default()
    config.to_yaml(Path(output))
    console.print(f"✅ Configuration saved to [bold]{output}[/bold]")
    console.print("Edit this file to customize agent behavior, models, and rules.")


@main.command()
def roster():
    """Show the current agent team roster and model assignments."""
    config = TeamConfig.default()
    _show_roster(config)


def _show_roster(config: TeamConfig) -> None:
    """Display the agent team roster."""
    table = Table(title="🤖 Agent Team Roster", show_header=True)
    table.add_column("Agent", style="cyan bold")
    table.add_column("Role", style="white")
    table.add_column("Model", style="magenta")
    table.add_column("Tier", style="yellow")
    table.add_column("Status", justify="center")

    tier_names = {
        ModelTier.OPUS: "Opus (Top)",
        ModelTier.SONNET: "Sonnet (Mid)",
        ModelTier.HAIKU: "Haiku (Fast)",
    }

    role_icons = {
        "security": "🔒",
        "architecture": "🏗️",
        "performance": "⚡",
        "code_quality": "📝",
        "testing": "🧪",
    }

    for key, agent in config.agents.items():
        icon = role_icons.get(agent.role, "🤖")
        status = "[green]Active[/green]" if agent.enabled else "[red]Disabled[/red]"
        table.add_row(
            f"{icon} {agent.name}",
            agent.role,
            agent.model.value,
            tier_names.get(agent.model, "Unknown"),
            status,
        )

    # Add orchestrator row
    table.add_row(
        "👑 Orchestrator",
        "team_leader",
        ModelTier.OPUS.value,
        "Opus (Top)",
        "[green bold]Active[/green bold]",
    )

    console.print(table)
    console.print()


if __name__ == "__main__":
    main()
