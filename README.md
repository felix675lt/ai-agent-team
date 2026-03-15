# AI Agent Team

Autonomous code review and analysis system with specialized AI agents. Each agent uses a Claude model tier optimized for its role.

## Agent Roster

| Agent | Model | Role |
|-------|-------|------|
| 👑 **Orchestrator** | Opus | Team leader — coordinates agents, aggregates results |
| 🔒 **Security** | Opus | Vulnerability detection (OWASP Top 10, injection, secrets) |
| 🏗️ **Architecture** | Sonnet | Design patterns, SOLID, coupling analysis |
| ⚡ **Performance** | Sonnet | Bottleneck detection, Big-O analysis, memory leaks |
| 📝 **Code Quality** | Haiku | Style, naming, dead code, complexity |
| 🧪 **Testing** | Sonnet | Coverage gaps, test quality, missing edge cases |

## Why Different Models?

- **Opus** — Security can't afford false negatives. The orchestrator needs top-tier reasoning for final judgment.
- **Sonnet** — Architecture, performance, and testing need solid analysis but don't require maximum capability.
- **Haiku** — Code quality checks are pattern-based and benefit from speed over depth.

## Quick Start

```bash
# Install
pip install -e .

# Set API key
export ANTHROPIC_API_KEY=your-key-here

# Analyze current directory
agent-team analyze .

# Analyze specific path with JSON output
agent-team analyze ./src --output json --save report.json

# Run only security and performance agents
agent-team analyze . -a security -a performance

# Show team roster
agent-team roster

# Generate config file
agent-team init
```

## Configuration

Generate a config file with `agent-team init`, then customize:

```yaml
agents:
  security:
    name: Security Agent
    model: claude-opus-4-6
    enabled: true
    max_files_per_run: 50
    custom_rules:
      - "Check for hardcoded AWS credentials"
      - "Flag any use of eval()"

parallel: true
output_format: rich
exclude_patterns:
  - node_modules
  - .git
  - __pycache__
```

## Output Formats

- **rich** — Colorful terminal output with tables (default)
- **json** — Machine-readable JSON report
- **markdown** — Markdown report for documentation

## Architecture

```
Orchestrator (Opus) ──┬── Security Agent (Opus)
                      ├── Architecture Agent (Sonnet)
                      ├── Performance Agent (Sonnet)
                      ├── Code Quality Agent (Haiku)
                      └── Testing Agent (Sonnet)
```

The Orchestrator discovers files, dispatches them to agents in parallel, and aggregates findings into a prioritized report. Critical findings are highlighted first.

## Requirements

- Python 3.10+
- Anthropic API key
