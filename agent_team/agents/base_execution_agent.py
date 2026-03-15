"""Base execution agent for business task handling."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import anthropic

from agent_team.core.config import AgentConfig
from agent_team.core.models import Task, TaskResult, TaskStatus


class BaseExecutionAgent(ABC):
    """Base class for agents that execute business tasks."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = anthropic.Anthropic()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt defining this agent's expertise and role."""

    @abstractmethod
    def build_execution_prompt(self, task: Task) -> str:
        """Build the execution prompt for a specific task."""

    def execute_task(self, task: Task) -> TaskResult:
        """Execute a task and return the result."""
        start_time = time.time()

        try:
            # Build the prompt for Claude
            prompt = self.build_execution_prompt(task)

            # Call Claude API
            response = self.client.messages.create(
                model=self.config.model.value,
                max_tokens=4096,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse the response
            output_text = response.content[0].text
            parsed_output = self.parse_response(output_text)

            # Build result
            result = TaskResult(
                task_id=task.task_id,
                team_name=self.config.team_name,
                agent_name=self.config.name,
                status=TaskStatus.COMPLETED,
                output=parsed_output,
                summary=self._generate_summary(parsed_output),
                model_used=self.config.model.value,
                execution_time_seconds=time.time() - start_time,
            )
            result.completed_at = datetime.now()

            return result

        except Exception as e:
            # Handle errors
            result = TaskResult(
                task_id=task.task_id,
                team_name=self.config.team_name,
                agent_name=self.config.name,
                status=TaskStatus.REJECTED,
                output={"error": str(e)},
                summary=f"Task execution failed: {str(e)}",
                model_used=self.config.model.value,
                execution_time_seconds=time.time() - start_time,
            )
            result.completed_at = datetime.now()
            return result

    def parse_response(self, response_text: str) -> dict[str, Any]:
        """
        Parse Claude's response into structured output.

        Default implementation expects markdown-style headers like:
        # Section Title
        content here

        Override this method for custom parsing.
        """
        sections = {}
        current_section = "output"
        current_content = []

        for line in response_text.split("\n"):
            if line.startswith("# ") or line.startswith("## ") or line.startswith("### "):
                # Save previous section
                if current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                # Start new section
                current_section = line.lstrip("#").strip().lower().replace(" ", "_")
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content).strip()

        # If no sections, put everything in 'output'
        if not sections:
            sections["output"] = response_text

        return sections

    def _generate_summary(self, output: dict[str, Any]) -> str:
        """Generate a summary from the task output."""
        if not output:
            return "No output generated."

        if "error" in output:
            return f"Task failed with error: {output['error']}"

        # Create a brief summary
        sections = ", ".join(key for key in output.keys() if key != "error")
        return f"Task completed successfully. Generated sections: {sections}"

    def get_security_considerations(self, task: Task) -> list[str]:
        """Get security considerations for this task. Override in subclasses."""
        return [
            "Ensure all API keys and secrets are properly stored",
            "Implement proper authentication and authorization",
            "Validate all user inputs",
            "Follow OWASP guidelines",
        ]

    def get_performance_notes(self, task: Task) -> list[str]:
        """Get performance considerations for this task. Override in subclasses."""
        return [
            "Optimize for scalability",
            "Consider caching strategies",
            "Monitor resource usage",
        ]

    def get_architecture_notes(self, task: Task) -> list[str]:
        """Get architecture considerations for this task. Override in subclasses."""
        return [
            "Follow SOLID principles",
            "Design for maintainability",
            "Plan for future extensibility",
        ]
