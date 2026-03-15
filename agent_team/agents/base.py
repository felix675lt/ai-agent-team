"""Base agent class for all specialized agents."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic

from agent_team.core.config import AgentConfig, ModelTier, Severity


@dataclass
class Finding:
    """A single finding from an agent's analysis."""

    agent: str
    severity: Severity
    category: str
    file_path: str
    line: int | None
    title: str
    description: str
    suggestion: str | None = None
    code_snippet: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "severity": self.severity.value,
            "category": self.category,
            "file_path": self.file_path,
            "line": self.line,
            "title": self.title,
            "description": self.description,
            "suggestion": self.suggestion,
            "code_snippet": self.code_snippet,
        }


@dataclass
class AgentResult:
    """Result from an agent's analysis run."""

    agent_name: str
    model_used: str
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""
    files_analyzed: int = 0
    duration_seconds: float = 0.0
    error: str | None = None

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Severity.HIGH)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "model_used": self.model_used,
            "summary": self.summary,
            "files_analyzed": self.files_analyzed,
            "duration_seconds": round(self.duration_seconds, 2),
            "findings_count": len(self.findings),
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "findings": [f.to_dict() for f in self.findings],
            "error": self.error,
        }


class BaseAgent(ABC):
    """Base class for all specialized agents."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = anthropic.Anthropic()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt defining this agent's expertise and behavior."""

    @abstractmethod
    def build_analysis_prompt(self, file_path: str, content: str) -> str:
        """Build the analysis prompt for a specific file."""

    def analyze_file(self, file_path: str, content: str) -> list[Finding]:
        """Analyze a single file and return findings."""
        prompt = self.build_analysis_prompt(file_path, content)

        try:
            response = self.client.messages.create(
                model=self.config.model.value,
                max_tokens=4096,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            return self.parse_response(file_path, response.content[0].text)
        except Exception as e:
            return [
                Finding(
                    agent=self.config.name,
                    severity=Severity.INFO,
                    category="error",
                    file_path=file_path,
                    line=None,
                    title="Analysis Error",
                    description=f"Failed to analyze: {e}",
                )
            ]

    def parse_response(self, file_path: str, response_text: str) -> list[Finding]:
        """Parse the model's response into structured findings."""
        findings: list[Finding] = []
        current: dict[str, Any] = {}

        for line in response_text.split("\n"):
            line = line.strip()
            if line.startswith("FINDING:"):
                if current:
                    findings.append(self._build_finding(file_path, current))
                current = {"title": line[8:].strip()}
            elif line.startswith("SEVERITY:") and current:
                sev = line[9:].strip().lower()
                current["severity"] = sev
            elif line.startswith("CATEGORY:") and current:
                current["category"] = line[9:].strip()
            elif line.startswith("LINE:") and current:
                try:
                    current["line"] = int(line[5:].strip())
                except ValueError:
                    current["line"] = None
            elif line.startswith("DESCRIPTION:") and current:
                current["description"] = line[12:].strip()
            elif line.startswith("SUGGESTION:") and current:
                current["suggestion"] = line[11:].strip()
            elif line.startswith("CODE:") and current:
                current["code_snippet"] = line[5:].strip()
            elif current and "description" in current:
                # Continuation of description
                current["description"] = current.get("description", "") + " " + line

        if current:
            findings.append(self._build_finding(file_path, current))

        return findings

    def _build_finding(self, file_path: str, data: dict[str, Any]) -> Finding:
        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
        }
        return Finding(
            agent=self.config.name,
            severity=severity_map.get(data.get("severity", "info"), Severity.INFO),
            category=data.get("category", "general"),
            file_path=file_path,
            line=data.get("line"),
            title=data.get("title", "Untitled"),
            description=data.get("description", ""),
            suggestion=data.get("suggestion"),
            code_snippet=data.get("code_snippet"),
        )

    def run(self, files: list[tuple[str, str]]) -> AgentResult:
        """Run analysis on a list of (file_path, content) tuples."""
        start = time.time()
        all_findings: list[Finding] = []

        limited_files = files[: self.config.max_files_per_run]

        for file_path, content in limited_files:
            findings = self.analyze_file(file_path, content)
            all_findings.extend(findings)

        duration = time.time() - start

        return AgentResult(
            agent_name=self.config.name,
            model_used=self.config.model.value,
            findings=all_findings,
            files_analyzed=len(limited_files),
            duration_seconds=duration,
            summary=self._generate_summary(all_findings),
        )

    def _generate_summary(self, findings: list[Finding]) -> str:
        if not findings:
            return "No issues found."

        by_severity: dict[str, int] = {}
        for f in findings:
            by_severity[f.severity.value] = by_severity.get(f.severity.value, 0) + 1

        parts = [f"{count} {sev}" for sev, count in sorted(by_severity.items())]
        return f"Found {len(findings)} issues: {', '.join(parts)}"
