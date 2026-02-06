# SmartGen
A DDD/Clean Architecture friendly code generator.

## Features

- **Project Initialization**: Set up new projects with DDD patterns
- **LLM Configuration**: Configure and manage LLM providers (Ollama, OpenAI, etc.)
- **Domain Generation**: Generate domain layer code based on requirements

## Installation

```bash
# Install smartgen with all dependencies
pip install smartgen


## Usage

### 1. Initialize a New Project

```bash
smartgen init --language python --pattern ddd --app api
```

This creates:
- `.smartgen.yml` - Project configuration
- `srs.md` - Software Requirements Specification
- `stories/` - User stories directory
- `src/` - Source code directory

### 2. Configure Your SRS

Edit `srs.md` and add your software requirements. Example:

```markdown
# Software Requirements Specification

## Overview
Build an e-commerce system...

## Features
- User registration and authentication
- Product catalog management
- Shopping cart
- Order processing
...
```

### 3. Generate Domain Layer

```bash
smartgen generate domain
```

This command:
1. Reads the LLM configuration from `.smartgen.yml`
2. Reads your requirements from `srs.md`
3. Applies DDD policy rules from `policies/ddd/python/domain.txt`
4. Generates domain layer code with proper structure:
   - Aggregates
   - Entities
   - Value Objects
   - Domain Services
   - Domain Errors

The generated code follows DDD best practices:
- Pure domain models (no framework dependencies)
- Proper invariant enforcement
- Clear separation of concerns
- Comprehensive documentation

## Commands

### `smartgen init`
Initialize a new project with smartgen configuration.

**Options:**
- `--language` - Project language (default: python)
- `--pattern` - Architecture pattern (default: ddd)
- `--app` - Application type (default: api)

### `smartgen llmconfig`
Manage LLM provider configuration.

**Subcommands:**
- `add` - Add a new LLM provider
- `list` - List configured providers
- `set-default` - Set default provider
- `remove` - Remove a provider

### `smartgen generate domain`
Generate domain layer code based on SRS and DDD policies.

**Options:**
- `--debug` - Enable debug mode to display all inputs/outputs including LLM prompts and responses

**Requirements:**
- `.smartgen.yml` must exist (run `smartgen init` first)
- `srs.md` must contain requirements

**Example:**
```bash
# Normal mode
smartgen generate domain

# Debug mode - shows all steps, prompts, and LLM responses
smartgen generate domain --debug
```

**Debug Output Includes:**
- Project configuration
- SRS content
- DDD policy rules
- Complete prompt sent to LLM
- Full LLM response
- Each file being created

## Configuration

The `.smartgen.yml` file contains:

```yaml
project:
  language: python
  pattern: ddd
  app: api

llm:
  default: ollama
  providers:
    ollama:
      type: local
      model: deepseek-coder-v2
      url: http://localhost:11434
    
    # OpenAI GPT-4 (chat model)
    # Note: api_key is stored in ~/.smartgen/.llmconfig
    gpt4:
      type: cloud
      model: gpt-4
    
    # OpenAI Codex (completions model)
    codex:
      type: cloud
      model: code-davinci-002
```

### Supported LLM Providers

#### Local Providers
- **Ollama** - Run models locally (deepseek-coder-v2, codellama, etc.)

#### Cloud Providers (OpenAI API)
- **Chat Models** - GPT-4, GPT-3.5-turbo (uses chat completions API)
- **Codex Models** - code-davinci-002, code-cushman-002 (uses legacy completions API)
- **Custom Endpoints** - Any OpenAI-compatible API (add `base_url` field)

### Adding Providers

```bash
# Add Ollama (local)
smartgen llmconfig add ollama local --model deepseek-coder-v2 --url http://localhost:11434

# Add GPT-4 (chat model)
smartgen llmconfig add gpt4 cloud --model gpt-4 --api-key YOUR_API_KEY

# Add Codex (optimized for code generation)
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key YOUR_API_KEY

# Set default
smartgen llmconfig set-default codex
```

**Note:** Codex models are specifically designed for code generation and often produce more accurate domain models with better adherence to DDD principles.

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```