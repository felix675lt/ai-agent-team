"""CLI interface for AI Agent Team."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_team.core.config import ModelTier, TeamConfig
from agent_team.core.dispatcher import TaskDispatcher
from agent_team.core.models import TaskType
from agent_team.core.orchestrator import Orchestrator

console = Console()


@click.group()
@click.version_option(version="2.0.0", prog_name="ai-agent-team")
def main():
    """AI Agent Team — Business Execution with Specialized Teams.

    Multi-team organization with specialized agents:

    **Leadership:**
    👑 CEO/Orchestrator  → Manages organization and task routing
    🔐 CISO              → Security oversight and compliance
    🏗️  CTO               → Architecture and performance standards

    **Core Teams:**
    🛠️  Engineering       → Technical architecture and implementation
    📢 Marketing         → Strategy, campaigns, and growth
    🎨 Design            → UX/UI and visual design
    📊 Product           → Roadmaps, features, and strategy
    ⚙️  Operations        → Processes, HR, finance, legal

    **Optional Teams:**
    📈 Data & Analytics  → Data strategies and insights
    💼 Business Dev      → Partnerships and sales
    😊 Customer Success  → Support and retention
    """


@main.command()
@click.argument("request")
@click.option("--team", "-t", type=click.Choice([
    "engineering", "marketing", "design", "product", "operations",
    "data_analytics", "business_development", "customer_success"
]), help="Specific team to handle the request")
@click.option("--save", "-s", type=click.Path(), help="Save result to file")
def execute(request: str, team: str | None, save: str | None):
    """Execute a business task using the appropriate team.

    REQUEST can be:
    - A text description of the task
    - A file path containing the task description

    Example:
        agent-team execute "Engineering: Design a microservices architecture for handling 10k requests/sec"
    """
    console.print(Panel(
        "[bold]AI Agent Team[/bold] — Business Task Execution\n"
        "Orchestrated by [cyan]CEO/Orchestrator[/cyan]",
        style="bold blue",
    ))

    # Load request from file if it's a path
    if Path(request).exists():
        task_description = Path(request).read_text()
    else:
        task_description = request

    # Determine task type
    task_type = TaskType.ENGINEERING  # default
    if team:
        try:
            task_type = TaskType(team)
        except ValueError:
            console.print(f"[red]Invalid team: {team}[/red]")
            return

    # Initialize dispatcher
    dispatcher = TaskDispatcher()

    # Show team roster
    _show_team_roster(dispatcher)

    # Dispatch and execute task
    console.print(f"\n[yellow]Executing task...[/yellow]")
    task = dispatcher.dispatch_task(task_type, "Business Task", task_description)
    result = dispatcher.execute_task(task)

    # Display result
    console.print(f"\n[green]✅ Task Completed[/green]")
    console.print(f"Task ID: {result.task_id}")
    console.print(f"Team: {result.team_name}")
    console.print(f"Agent: {result.agent_name}")
    console.print(f"Execution Time: {result.execution_time_seconds:.2f}s")
    console.print(f"\n[bold]Summary:[/bold]\n{result.summary}")

    if result.output:
        console.print(f"\n[bold]Output:[/bold]")
        for key, value in result.output.items():
            console.print(f"\n[cyan]{key}:[/cyan]")
            if isinstance(value, str):
                console.print(value[:500] + "..." if len(value) > 500 else value)
            else:
                console.print(str(value)[:500])

    # Save result
    if save:
        save_path = Path(save)
        import json
        save_path.write_text(json.dumps(result.to_dict(), indent=2))
        console.print(f"\n📄 Result saved to [bold]{save}[/bold]")


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
    """Show the current agent team roster and model assignments (legacy)."""
    config = TeamConfig.default()
    _show_roster(config)


@main.command()
def team_status():
    """Show the current team structure and members."""
    dispatcher = TaskDispatcher()
    _show_team_roster(dispatcher)


def _show_team_roster(dispatcher: TaskDispatcher) -> None:
    """Display the business execution team roster."""
    table = Table(title="🤖 AI Agent Team - Business Execution", show_header=True)
    table.add_column("Team", style="cyan bold")
    table.add_column("Team Lead", style="white")
    table.add_column("Lead Model", style="magenta")
    table.add_column("Focus Area", style="yellow")

    team_info = {
        "Engineering": ("Engineering Lead", "Claude Opus", "Technical Architecture & Implementation"),
        "Marketing": ("Marketing Lead", "Claude Opus", "Strategy, Campaigns & Growth"),
        "Design": ("Design Lead", "Claude Opus", "UX/UI, Visual Design & Brand"),
        "Product Management": ("Product Lead", "Claude Opus", "Roadmaps, Features & Strategy"),
        "Operations": ("Operations Lead", "Claude Opus", "Processes, HR, Finance & Legal"),
        "Data & Analytics": ("Analytics Lead", "Claude Sonnet", "Data Strategies & Insights"),
        "Business Development": ("BD Lead", "Claude Sonnet", "Partnerships, Sales & Growth"),
        "Customer Success": ("CS Lead", "Claude Sonnet", "Support, Training & Retention"),
    }

    leadership = {
        "Leadership": ("CEO/Orchestrator", "Claude Opus", "Organization & Task Routing"),
        "Security": ("CISO", "Claude Opus", "Security & Compliance Oversight"),
        "Technology": ("CTO", "Claude Opus", "Architecture & Performance Standards"),
    }

    # Leadership section
    console.print("[bold cyan]Leadership[/bold cyan]")
    for role, (name, model, focus) in leadership.items():
        table.add_row(f"👑 {role}", name, model, focus)

    console.print(table)
    console.print()

    # Core teams section
    console.print("[bold cyan]Core Teams[/bold cyan]")
    core_table = Table(show_header=True)
    core_table.add_column("Team", style="cyan bold")
    core_table.add_column("Team Lead", style="white")
    core_table.add_column("Lead Model", style="magenta")
    core_table.add_column("Focus Area", style="yellow")

    core_teams = {k: v for k, v in team_info.items() if k in ["Engineering", "Marketing", "Design", "Product Management", "Operations"]}
    for team, (lead, model, focus) in core_teams.items():
        icon = "🛠️" if team == "Engineering" else "📢" if team == "Marketing" else "🎨" if team == "Design" else "📊" if team == "Product Management" else "⚙️"
        core_table.add_row(f"{icon} {team}", lead, model, focus)

    console.print(core_table)
    console.print()

    # Optional teams section
    console.print("[bold cyan]Optional Teams (Activate as Needed)[/bold cyan]")
    opt_table = Table(show_header=True)
    opt_table.add_column("Team", style="cyan bold")
    opt_table.add_column("Team Lead", style="white")
    opt_table.add_column("Lead Model", style="magenta")
    opt_table.add_column("Focus Area", style="yellow")

    optional_teams = {k: v for k, v in team_info.items() if k not in ["Engineering", "Marketing", "Design", "Product Management", "Operations"]}
    for team, (lead, model, focus) in optional_teams.items():
        icon = "📈" if team == "Data & Analytics" else "💼" if team == "Business Development" else "😊"
        opt_table.add_row(f"{icon} {team}", lead, model, focus)

    console.print(opt_table)
    console.print()


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
