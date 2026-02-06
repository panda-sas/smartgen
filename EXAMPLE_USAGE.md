# Example Usage of smartgen generate domain

This document demonstrates how to use the new `smartgen generate domain` command.

## Prerequisites

1. Initialize your project:
```bash
smartgen init --language python --pattern ddd --app api
```

2. Configure your LLM provider (if not already done):
```bash
# For Ollama (local)
smartgen llmconfig add ollama local --model deepseek-coder-v2

# For OpenAI (cloud) - requires API key
smartgen llmconfig add openai cloud --model gpt-4 --api-key YOUR_API_KEY

# Set default provider
smartgen llmconfig set-default ollama
```

## Step 1: Define Your Requirements

Edit the generated `srs.md` file with your software requirements:

```markdown
# Software Requirements Specification

## Project: Task Management System

### Overview
A simple task management system for teams to organize and track their work.

### Core Features

#### 1. Task Management
- Users can create tasks with title, description, priority, and due date
- Tasks can be assigned to team members
- Tasks have states: Draft, Todo, InProgress, Done, Cancelled
- Task priority: Low, Medium, High, Critical

#### 2. Project Management
- Tasks are organized into projects
- Each project has a name, description, and owner
- Projects can have multiple team members

#### 3. User Management
- Users have email, name, and role (Member, Admin)
- Email must be valid and unique
- Users can be assigned to multiple projects

### Business Rules

1. **Task Assignment**: Only active project members can be assigned to tasks
2. **Task State Transitions**: 
   - Draft → Todo (when task is ready)
   - Todo → InProgress (when work starts)
   - InProgress → Done (when completed)
   - Any state → Cancelled (if no longer needed)
3. **Project Ownership**: At least one admin must be assigned to each project
4. **Task Priority**: Critical priority tasks must have a due date
```

## Step 2: Generate Domain Layer

Run the generation command:

```bash
smartgen generate domain
```

### Debug Mode

For detailed visibility into the generation process, use debug mode:

```bash
smartgen generate domain --debug
```

Debug mode displays:
- ✓ Project configuration from `.smartgen.yml`
- ✓ Complete SRS content
- ✓ DDD policy rules being applied
- ✓ Full prompt sent to the LLM
- ✓ Complete LLM response
- ✓ Each file being created with its path

This is extremely useful for:
- Understanding what the LLM is seeing
- Debugging generation issues
- Verifying the prompt structure
- Learning how the system works

#### Sample Debug Output

When running with `--debug`, you'll see formatted panels showing each step:

```
╭─ Starting domain generation ────────────────────────────────╮
│ Project directory: /Users/you/myproject                     │
╰──────────────────────────────────────────────────────────────╯

╭─ Configuration loaded ───────────────────────────────────────╮
│ project:                                                      │
│   language: python                                           │
│   pattern: ddd                                               │
│   app: api                                                   │
│ llm:                                                         │
│   default: ollama                                            │
│   providers:                                                 │
│     ollama:                                                  │
│       type: local                                            │
│       model: deepseek-coder-v2                              │
│       url: http://localhost:11434                           │
╰──────────────────────────────────────────────────────────────╯

╭─ SRS Content ────────────────────────────────────────────────╮
│ # Software Requirements Specification                        │
│                                                              │
│ ## Project: Task Management System                          │
│ ...                                                          │
╰──────────────────────────────────────────────────────────────╯

╭─ DDD Policy ─────────────────────────────────────────────────╮
│ ### **Domain Layer Design Rules**                           │
│                                                              │
│ #### **1. Dependency Rule**                                 │
│ ...                                                          │
╰──────────────────────────────────────────────────────────────╯

╭─ Calling LLM ────────────────────────────────────────────────╮
│ Provider: ollama (local)                                     │
╰──────────────────────────────────────────────────────────────╯

╭─ Prompt sent to LLM ─────────────────────────────────────────╮
│ You are a domain modeling expert. Based on the Software...  │
│ [Full prompt displayed here]                                 │
╰──────────────────────────────────────────────────────────────╯

╭─ LLM Response ───────────────────────────────────────────────╮
│ {                                                            │
│   "files": [                                                 │
│     {                                                        │
│       "path": "src/domain/aggregates/task.py",              │
│       "content": "..."                                       │
│     },                                                       │
│     ...                                                      │
│   ]                                                          │
│ }                                                            │
╰──────────────────────────────────────────────────────────────╯

╭─ Created file ───────────────────────────────────────────────╮
│ src/domain/aggregates/task.py                               │
╰──────────────────────────────────────────────────────────────╯

╭─ Created file ───────────────────────────────────────────────╮
│ src/domain/value_objects/email.py                           │
╰──────────────────────────────────────────────────────────────╯

...

✓ Domain elements generated using provider 'ollama'.
```

## Expected Output

The command will:

1. Read your `.smartgen.yml` configuration
2. Load your `srs.md` requirements
3. Apply DDD policies from `policies/ddd/python/domain.txt`
4. Generate domain code following DDD principles

### Generated Structure

```
src/
└── domain/
    ├── __init__.py
    ├── aggregates/
    │   ├── __init__.py
    │   ├── project.py      # Project aggregate root
    │   └── task.py         # Task aggregate root
    ├── entities/
    │   ├── __init__.py
    │   └── team_member.py  # Team member entity
    ├── value_objects/
    │   ├── __init__.py
    │   ├── email.py        # Email value object
    │   ├── task_id.py      # Task identifier
    │   ├── project_id.py   # Project identifier
    │   ├── priority.py     # Priority enum
    │   └── task_state.py   # Task state enum
    ├── services/
    │   └── __init__.py
    └── errors/
        ├── __init__.py
        └── domain_errors.py
```

### Example Generated Code

The generator will create code like:

**src/domain/value_objects/email.py**
```python
"""Email value object."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """Represents a valid email address."""
    
    value: str
    
    def __post_init__(self):
        """Validate email on creation."""
        if not self._is_valid(self.value):
            raise ValueError(f"Invalid email address: {self.value}")
    
    @staticmethod
    def _is_valid(email: str) -> bool:
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
```

**src/domain/aggregates/task.py**
```python
"""Task aggregate root."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.value_objects.task_id import TaskId
from domain.value_objects.priority import Priority
from domain.value_objects.task_state import TaskState
from domain.errors.domain_errors import InvalidStateTransitionError


@dataclass
class Task:
    """Task aggregate root."""
    
    id: TaskId
    title: str
    description: str
    priority: Priority
    state: TaskState
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Enforce invariants."""
        self._validate_invariants()
    
    def _validate_invariants(self) -> None:
        """Validate business rules."""
        if self.priority == Priority.CRITICAL and self.due_date is None:
            raise ValueError("Critical priority tasks must have a due date")
    
    def start(self) -> None:
        """Transition task to InProgress state."""
        if self.state != TaskState.TODO:
            raise InvalidStateTransitionError(
                f"Cannot start task in state {self.state}"
            )
        self.state = TaskState.IN_PROGRESS
    
    def complete(self) -> None:
        """Mark task as done."""
        if self.state != TaskState.IN_PROGRESS:
            raise InvalidStateTransitionError(
                f"Cannot complete task in state {self.state}"
            )
        self.state = TaskState.DONE
```

## Benefits

1. **DDD Compliance**: All generated code follows DDD principles
2. **Type Safety**: Full type hints and validation
3. **Documentation**: Comprehensive docstrings
4. **Invariant Enforcement**: Business rules enforced at model level
5. **Pure Domain**: No framework dependencies
6. **Testable**: Easy to unit test without mocks

## Next Steps

After generation:

1. Review the generated code
2. Adjust as needed for your specific use case
3. Add application services for orchestration
4. Implement infrastructure layer (repositories, etc.)
5. Write comprehensive tests
