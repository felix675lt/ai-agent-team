"""Data models for the business execution agent team."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class TaskType(str, Enum):
    """Types of tasks that can be assigned to teams."""

    ENGINEERING = "engineering"
    MARKETING = "marketing"
    DESIGN = "design"
    PRODUCT = "product"
    OPERATIONS = "operations"
    DATA_ANALYTICS = "data_analytics"
    BUSINESS_DEVELOPMENT = "business_development"
    CUSTOMER_SUCCESS = "customer_success"


class TaskStatus(str, Enum):
    """Status of a task throughout its lifecycle."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SECURITY_REVIEW = "security_review"
    ARCHITECTURE_REVIEW = "architecture_review"
    COMPLETED = "completed"
    REJECTED = "rejected"


class ReviewStatus(str, Enum):
    """Status of security/performance/architecture reviews."""

    PENDING = "pending"
    APPROVED = "approved"
    APPROVED_WITH_CHANGES = "approved_with_changes"
    REJECTED = "rejected"


@dataclass
class Task:
    """A task to be executed by an agent or team."""

    task_id: str
    task_type: TaskType
    title: str
    description: str
    priority: int = 1  # 1=highest, 5=lowest
    assigned_team: str = ""
    assigned_agent: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "assigned_team": self.assigned_team,
            "assigned_agent": self.assigned_agent,
            "context": self.context,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class SecurityReview:
    """Security review of a task result."""

    reviewer: str  # CISO name
    status: ReviewStatus = ReviewStatus.PENDING
    findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    reviewed_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "reviewer": self.reviewer,
            "status": self.status.value,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
        }


@dataclass
class ArchitectureReview:
    """Architecture and performance review of a task result."""

    reviewer: str  # CTO name
    status: ReviewStatus = ReviewStatus.PENDING
    architecture_notes: list[str] = field(default_factory=list)
    performance_notes: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    reviewed_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "reviewer": self.reviewer,
            "status": self.status.value,
            "architecture_notes": self.architecture_notes,
            "performance_notes": self.performance_notes,
            "recommendations": self.recommendations,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
        }


@dataclass
class TaskResult:
    """Result from executing a task."""

    task_id: str
    team_name: str
    agent_name: str
    status: TaskStatus = TaskStatus.PENDING

    # The actual output: documents, code, strategies, designs, etc.
    output: dict[str, Any] = field(default_factory=dict)  # Keys: "document", "code", "analysis", etc.
    summary: str = ""

    # Reviews
    security_review: SecurityReview = field(default_factory=lambda: SecurityReview("CISO"))
    architecture_review: ArchitectureReview = field(default_factory=lambda: ArchitectureReview("CTO"))

    # Metadata
    execution_time_seconds: float = 0.0
    model_used: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "team_name": self.team_name,
            "agent_name": self.agent_name,
            "status": self.status.value,
            "output": self.output,
            "summary": self.summary,
            "security_review": self.security_review.to_dict(),
            "architecture_review": self.architecture_review.to_dict(),
            "execution_time_seconds": round(self.execution_time_seconds, 2),
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class TeamReport:
    """Aggregated report from multiple task results."""

    report_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    task_results: list[TaskResult] = field(default_factory=list)
    orchestrator_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp.isoformat(),
            "task_count": len(self.task_results),
            "results": [r.to_dict() for r in self.task_results],
            "orchestrator_notes": self.orchestrator_notes,
        }

    def to_json(self) -> str:
        """Export as JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        """Export as Markdown report."""
        md_parts = [
            f"# Team Report: {self.report_id}",
            f"**Generated:** {self.timestamp.isoformat()}",
            f"**Total Tasks:** {len(self.task_results)}",
            "",
        ]

        if self.orchestrator_notes:
            md_parts.extend([
                "## Orchestrator Notes",
                self.orchestrator_notes,
                "",
            ])

        for result in self.task_results:
            md_parts.extend([
                f"## Task: {result.task_id}",
                f"**Team:** {result.team_name}  ",
                f"**Agent:** {result.agent_name}  ",
                f"**Status:** {result.status.value}  ",
                f"**Model:** {result.model_used}  ",
                f"**Execution Time:** {result.execution_time_seconds:.2f}s  ",
                "",
                "### Summary",
                result.summary,
                "",
            ])

            if result.output:
                md_parts.append("### Output")
                for key, value in result.output.items():
                    if isinstance(value, str):
                        md_parts.extend([
                            f"**{key}:**",
                            f"```\n{value}\n```",
                            "",
                        ])
                    else:
                        md_parts.extend([
                            f"**{key}:**",
                            f"```\n{str(value)}\n```",
                            "",
                        ])

            # Security Review
            sec_review = result.security_review
            if sec_review.status != ReviewStatus.PENDING:
                md_parts.extend([
                    "### Security Review",
                    f"**Status:** {sec_review.status.value}",
                    f"**Reviewer:** {sec_review.reviewer}",
                ])
                if sec_review.findings:
                    md_parts.append("**Findings:**")
                    for finding in sec_review.findings:
                        md_parts.append(f"- {finding}")
                if sec_review.recommendations:
                    md_parts.append("**Recommendations:**")
                    for rec in sec_review.recommendations:
                        md_parts.append(f"- {rec}")
                md_parts.append("")

            # Architecture Review
            arch_review = result.architecture_review
            if arch_review.status != ReviewStatus.PENDING:
                md_parts.extend([
                    "### Architecture Review",
                    f"**Status:** {arch_review.status.value}",
                    f"**Reviewer:** {arch_review.reviewer}",
                ])
                if arch_review.architecture_notes:
                    md_parts.append("**Architecture Notes:**")
                    for note in arch_review.architecture_notes:
                        md_parts.append(f"- {note}")
                if arch_review.performance_notes:
                    md_parts.append("**Performance Notes:**")
                    for note in arch_review.performance_notes:
                        md_parts.append(f"- {note}")
                if arch_review.recommendations:
                    md_parts.append("**Recommendations:**")
                    for rec in arch_review.recommendations:
                        md_parts.append(f"- {rec}")
                md_parts.append("")

            md_parts.append("---\n")

        return "\n".join(md_parts)
