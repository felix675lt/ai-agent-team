"""Orchestrator - The team leader that coordinates all agents.

Model: Opus (전체 조율 및 최종 판단 담당)
Manages agent lifecycle, parallel execution, and result aggregation.
"""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from agent_team.agents.base import AgentResult, BaseAgent, Finding
from agent_team.agents.security import SecurityAgent
from agent_team.agents.performance import PerformanceAgent
from agent_team.agents.architecture import ArchitectureAgent
from agent_team.agents.code_quality import CodeQualityAgent
from agent_team.agents.testing import TestingAgent
from agent_team.core.config import Severity, TeamConfig


AGENT_CLASSES: dict[str, type[BaseAgent]] = {
    "security": SecurityAgent,
    "performance": PerformanceAgent,
    "architecture": ArchitectureAgent,
    "code_quality": CodeQualityAgent,
    "testing": TestingAgent,
}

# File extensions to analyze
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs",
    ".rb", ".php", ".c", ".cpp", ".h", ".hpp", ".cs", ".swift",
    ".kt", ".scala", ".sol", ".yaml", ".yml", ".json", ".toml",
    ".sql", ".sh", ".bash", ".dockerfile", ".tf", ".hcl",
}


class Orchestrator:
    """Team leader that coordinates all specialized agents.

    The Orchestrator is the brain of the agent team:
    1. Discovers files to analyze
    2. Dispatches work to specialized agents (in parallel when configured)
    3. Aggregates and prioritizes findings
    4. Produces unified reports
    """

    def __init__(self, config: TeamConfig):
        self.config = config
        self.console = Console()
        self.agents: dict[str, BaseAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self) -> None:
        """Initialize all enabled agents with their configurations."""
        for key, agent_config in self.config.agents.items():
            if agent_config.enabled and key in AGENT_CLASSES:
                self.agents[key] = AGENT_CLASSES[key](agent_config)

    def discover_files(self, target: str = ".") -> list[tuple[str, str]]:
        """Discover all analyzable files in the target directory."""
        target_path = Path(target).resolve()
        files: list[tuple[str, str]] = []

        if target_path.is_file():
            content = target_path.read_text(errors="replace")
            return [(str(target_path), content)]

        for path in sorted(target_path.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix not in SUPPORTED_EXTENSIONS:
                continue
            if any(exc in path.parts for exc in self.config.exclude_patterns):
                continue
            try:
                content = path.read_text(errors="replace")
                rel_path = str(path.relative_to(target_path))
                files.append((rel_path, content))
            except (PermissionError, OSError):
                continue

        return files

    def run(self, target: str = ".") -> TeamReport:
        """Execute the full analysis pipeline."""
        start_time = time.time()

        # Phase 1: File Discovery
        self.console.print(Panel("🔍 Phase 1: File Discovery", style="bold blue"))
        files = self.discover_files(target)
        self.console.print(f"  Found [bold]{len(files)}[/bold] files to analyze\n")

        if not files:
            self.console.print("[yellow]No analyzable files found.[/yellow]")
            return TeamReport(results={}, total_duration=0, files_analyzed=0)

        # Phase 2: Agent Dispatch
        self.console.print(Panel("🚀 Phase 2: Agent Dispatch", style="bold green"))
        results = self._dispatch_agents(files)

        # Phase 3: Result Aggregation
        self.console.print(Panel("📊 Phase 3: Result Aggregation", style="bold magenta"))
        total_duration = time.time() - start_time

        report = TeamReport(
            results=results,
            total_duration=total_duration,
            files_analyzed=len(files),
        )

        self._display_report(report)
        return report

    def _dispatch_agents(self, files: list[tuple[str, str]]) -> dict[str, AgentResult]:
        """Dispatch analysis to all agents, optionally in parallel."""
        results: dict[str, AgentResult] = {}

        if self.config.parallel and len(self.agents) > 1:
            results = self._run_parallel(files)
        else:
            results = self._run_sequential(files)

        return results

    def _run_parallel(self, files: list[tuple[str, str]]) -> dict[str, AgentResult]:
        """Run all agents in parallel using thread pool."""
        results: dict[str, AgentResult] = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            futures = {}
            with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
                for key, agent in self.agents.items():
                    task = progress.add_task(
                        f"  {agent.config.name} ({agent.config.model.value})",
                        total=None,
                    )
                    future = executor.submit(agent.run, files)
                    futures[future] = (key, task)

                for future in as_completed(futures):
                    key, task = futures[future]
                    try:
                        result = future.result()
                        results[key] = result
                        progress.update(task, description=f"  ✅ {result.agent_name} — {len(result.findings)} findings")
                    except Exception as e:
                        results[key] = AgentResult(
                            agent_name=self.agents[key].config.name,
                            model_used=self.agents[key].config.model.value,
                            error=str(e),
                        )
                        progress.update(task, description=f"  ❌ {self.agents[key].config.name} — error")

        return results

    def _run_sequential(self, files: list[tuple[str, str]]) -> dict[str, AgentResult]:
        """Run agents one by one."""
        results: dict[str, AgentResult] = {}

        for key, agent in self.agents.items():
            self.console.print(f"  Running {agent.config.name} ({agent.config.model.value})...")
            try:
                results[key] = agent.run(files)
                self.console.print(f"  ✅ {agent.config.name} — {len(results[key].findings)} findings")
            except Exception as e:
                results[key] = AgentResult(
                    agent_name=agent.config.name,
                    model_used=agent.config.model.value,
                    error=str(e),
                )
                self.console.print(f"  ❌ {agent.config.name} — {e}")

        return results

    def _display_report(self, report: TeamReport) -> None:
        """Display the final aggregated report."""
        self.console.print()

        # Summary table
        table = Table(title="Agent Team Report", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Model", style="blue")
        table.add_column("Files", justify="right")
        table.add_column("Findings", justify="right")
        table.add_column("Critical", justify="right", style="red")
        table.add_column("High", justify="right", style="yellow")
        table.add_column("Time", justify="right", style="green")
        table.add_column("Status", justify="center")

        for result in report.results.values():
            status = "✅" if not result.error else "❌"
            table.add_row(
                result.agent_name,
                result.model_used.split("-")[-1],
                str(result.files_analyzed),
                str(len(result.findings)),
                str(result.critical_count) if result.critical_count else "-",
                str(result.high_count) if result.high_count else "-",
                f"{result.duration_seconds:.1f}s",
                status,
            )

        self.console.print(table)

        # Critical findings
        all_critical = report.get_findings_by_severity(Severity.CRITICAL)
        if all_critical:
            self.console.print(Panel(
                f"[bold red]⚠️  {len(all_critical)} CRITICAL issues found![/bold red]",
                style="red",
            ))
            for f in all_critical:
                self.console.print(f"  [red]• [{f.agent}] {f.file_path}:{f.line or '?'} — {f.title}[/red]")
                self.console.print(f"    {f.description}")
                if f.suggestion:
                    self.console.print(f"    [green]Fix: {f.suggestion}[/green]")
                self.console.print()

        # Summary stats
        total = report.total_findings
        self.console.print(Panel(
            f"Total: [bold]{total}[/bold] findings across "
            f"[bold]{report.files_analyzed}[/bold] files in "
            f"[bold]{report.total_duration:.1f}s[/bold]",
            title="Summary",
            style="bold",
        ))


class TeamReport:
    """Aggregated report from all agents."""

    def __init__(
        self,
        results: dict[str, AgentResult],
        total_duration: float,
        files_analyzed: int,
    ):
        self.results = results
        self.total_duration = total_duration
        self.files_analyzed = files_analyzed

    @property
    def all_findings(self) -> list[Finding]:
        findings: list[Finding] = []
        for result in self.results.values():
            findings.extend(result.findings)
        return findings

    @property
    def total_findings(self) -> int:
        return len(self.all_findings)

    def get_findings_by_severity(self, severity: Severity) -> list[Finding]:
        return [f for f in self.all_findings if f.severity == severity]

    def to_json(self) -> str:
        return json.dumps(
            {
                "total_duration": round(self.total_duration, 2),
                "files_analyzed": self.files_analyzed,
                "total_findings": self.total_findings,
                "agents": {k: v.to_dict() for k, v in self.results.items()},
            },
            indent=2,
            ensure_ascii=False,
        )

    def to_markdown(self) -> str:
        lines = [
            "# Agent Team Report\n",
            f"- **Files analyzed:** {self.files_analyzed}",
            f"- **Total findings:** {self.total_findings}",
            f"- **Duration:** {self.total_duration:.1f}s\n",
        ]

        for result in self.results.values():
            lines.append(f"## {result.agent_name} ({result.model_used})")
            lines.append(f"- Findings: {len(result.findings)}")
            lines.append(f"- Duration: {result.duration_seconds:.1f}s\n")

            for f in result.findings:
                icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(f.severity.value, "⚪")
                lines.append(f"### {icon} {f.title}")
                lines.append(f"- **Severity:** {f.severity.value}")
                lines.append(f"- **File:** `{f.file_path}:{f.line or '?'}`")
                lines.append(f"- **Description:** {f.description}")
                if f.suggestion:
                    lines.append(f"- **Fix:** {f.suggestion}")
                lines.append("")

        return "\n".join(lines)
