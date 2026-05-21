# Agent Design Constraints and Security Boundaries

This directory contains core design constraints and security boundary documentation for the nanobot agent.

## Directory Structure

```
.agent/
├── design.md       # Design constraints
├── gotchas.md      # Common pitfalls
└── security.md     # Security boundaries
```

## Documentation Overview

### design.md - Design Constraints

Defines the core rules that nanobot architecture decisions must follow:

- **Keep core simple, extend at the edges** - New features added via channels, tools, skills, or MCP servers
- **Less structure, more smarts** - Prefer simple, readable code over new framework layers
- **Prefer duplication over premature abstraction** - Allow channels and providers to duplicate similar logic
- **Minimal changes** - Only change necessary code to fix bugs
- **Keep PRs reviewable** - Single focus, clear protected invariants
- **Explicit over magic** - Configuration must be explicitly declared in Pydantic models

### gotchas.md - Common Pitfalls

Common issues to watch out for during development:

- **Don't use `ruff format`** - Breaks git blame history
- **Configuration `${VAR}` references** - Parsed at load time, not shell default syntax
- **Windows compatibility** - Use `pathlib.Path`, watch for path separators
- **Prompt templates** - Modifying these files directly affects agent behavior
- **Context contamination persists** - Metadata must be bounded and sanitized
- **Heartbeat dummy tool calls** - Use structured decisions, not string matching
- **Skills as extension points** - "know-how" type capabilities should be added as skills
- **Atomic session writes** - Preserve existing atomic write patterns

### security.md - Security Boundaries

Defines the security boundaries for agent operations:

- **Workspace restriction** - Filesystem and shell tools must check allowed directories
- **SSRF protection** - All outbound HTTP requests must go through `validate_url_target`
- **Shell sandboxing** - Optional command wrapping, currently supports bwrap (bubblewrap)

## Usage Guide

These documents should serve as references during development:

1. Before adding new features, read `design.md` to ensure compliance with architectural constraints
2. When writing code, refer to `gotchas.md` to avoid common pitfalls
3. When handling security-sensitive code, follow the rules in `security.md`

## Related Resources

- [Architecture documentation](../docs/architecture.md)
- [Security documentation](../docs/security.md)
- [Developer guide](../docs/developer-guide.md)