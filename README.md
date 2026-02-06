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
```

All required dependencies (including OpenAI support) are installed automatically.

## Quick Start

### 1. Set up your LLM provider

**Option A: Use Ollama (Local, Free)**
```bash
# Install Ollama: https://ollama.ai
# Start Ollama and pull a model:
ollama pull deepseek-coder-v2

# Configure smartgen:
smartgen llmconfig add ollama local --model deepseek-coder-v2
smartgen llmconfig set-default ollama
```

**Option B: Use OpenAI Codex (Cloud, Recommended for GPT models)**
```bash
# Get API key from https://platform.openai.com/api-keys

# For code-davinci-002 (best quality):
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key sk-...

# Or use any OpenAI model:
smartgen llmconfig add gpt4 cloud --model gpt-4 --api-key sk-...

smartgen llmconfig set-default codex
```

### 2. Initialize your project

```bash
smartgen init --language python --pattern ddd --app api
```

### 3. Write your requirements

Edit `srs.md` with your requirements.

### 4. Generate domain layer

```bash
smartgen generate domain
```

With debug output:
```bash
smartgen generate domain --debug
```

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
- **Codex Models** - code-davinci-002, code-cushman-002 (specialized for code generation)
- **Chat Models** - GPT-4, GPT-3.5-turbo (general purpose)

**Recommendation:** For domain generation, Codex models typically produce higher quality code with better DDD adherence. If using chat models, ensure they can output clean JSON responses.

### Adding Providers

```bash
# Add Ollama (local)
smartgen llmconfig add ollama local --model deepseek-coder-v2 --url http://localhost:11434

# Add Codex (optimized for code generation)
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key YOUR_API_KEY

# Add GPT-4 (general purpose)
smartgen llmconfig add gpt4 cloud --model gpt-4 --api-key YOUR_API_KEY

# Set default
smartgen llmconfig set-default codex
```

**Best Practice:** Use Codex models for superior domain generation quality.

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```