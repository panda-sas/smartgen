# SmartGen 🚀

<div align="center">

**AI-Powered Domain-Driven Design Code Generator**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

*Generate clean, maintainable DDD code from requirements using AI*

[Features](#-features) • [Quick Start](#-quick-start) • [Examples](#-examples) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ What is SmartGen?

SmartGen is an **AI-powered code generator** that transforms your Software Requirements Specification (SRS) into production-ready Domain-Driven Design (DDD) code. Instead of manually scaffolding entities, value objects, and aggregates, SmartGen uses Large Language Models (LLMs) to generate architecturally sound domain code that follows DDD principles.

### 🎯 Why SmartGen?

**The Problem:**
- Setting up DDD projects is time-consuming and error-prone
- Maintaining architectural consistency across teams is challenging
- Learning DDD patterns requires significant expertise
- Manual code generation is repetitive and boring

**The Solution:**
- ⚡ **Fast**: Generate domain layers in seconds, not hours
- 🎯 **Accurate**: Policy-driven generation ensures DDD compliance
- 🔧 **Flexible**: Works with local (Ollama) or cloud (OpenAI) LLMs
- 📚 **Educational**: Learn DDD patterns by seeing generated code
- 🔒 **Secure**: API keys never leave your machine

---

## 🌟 Features

- 🏗️ **DDD-Compliant Generation**: Automatically generates entities, value objects, aggregates, and domain services following DDD principles
- 🤖 **Multi-LLM Support**: Use local models (Ollama) or cloud providers (OpenAI Codex, GPT-4)
- 📋 **Policy-Driven**: Enforces architectural patterns through configurable policies
- 🔍 **Debug Mode**: See exactly what prompts are sent to the LLM and how code is generated
- 🎨 **Clean Architecture**: Generates code following Clean Architecture layer separation
- ⚙️ **Easy Configuration**: Simple YAML-based project configuration
- 🔐 **Secure**: API keys stored securely, never committed to repositories

---

## 🚀 Quick Start

### Installation

```bash
pip install smartgen
```

### 1️⃣ Set Up Your LLM Provider

**Option A: Use Ollama (Local, Free)**
```bash
# Install Ollama: https://ollama.ai
ollama pull deepseek-coder-v2

# Configure smartgen:
smartgen llmconfig add ollama local --model deepseek-coder-v2
smartgen llmconfig set-default ollama
```

**Option B: Use OpenAI (Cloud)**
```bash
# Get API key from https://platform.openai.com/api-keys
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key sk-...
smartgen llmconfig set-default codex
```

### 2️⃣ Initialize Your Project

```bash
smartgen init --language python --pattern ddd --app api
```

### 3️⃣ Write Your Requirements

Edit `srs.md` with your domain requirements:

```markdown
# E-Commerce Domain

## User Management
- Users can register with email and password
- Users have profiles with name and address
- Users can have multiple roles (Customer, Admin)

## Product Catalog
- Products have name, description, price, and stock
- Products belong to categories
- Products can be active or inactive
```

### 4️⃣ Generate Domain Layer

```bash
smartgen generate domain
```

That's it! SmartGen will analyze your requirements and generate:
- Domain entities (User, Product, etc.)
- Value objects (Email, Address, Money, etc.)
- Aggregates with proper boundaries
- Domain services where needed

### 5️⃣ Generate Application Layout (Optional)

```bash
smartgen generate layout
```

This creates the application, infrastructure, and interface layer structure.

---

## 📊 SmartGen vs Alternatives

| Feature | SmartGen | Manual Setup | ChatGPT/Copilot | Other Generators |
|---------|----------|-------------|-----------------|------------------|
| **DDD Compliance** | ✅ Policy-enforced | ⚠️ Manual | ❌ No guarantees | ⚠️ Varies |
| **Speed** | ⚡ Seconds | 🐌 Hours | ⚡ Fast | ⚡ Fast |
| **Consistency** | ✅ Always | ⚠️ Team-dependent | ❌ Inconsistent | ⚠️ Template-based |
| **Learning** | ✅ Shows patterns | ❌ No guidance | ⚠️ Limited | ❌ No explanation |
| **LLM Flexibility** | ✅ Local + Cloud | N/A | ❌ Cloud only | ❌ Usually none |
| **Policy-Driven** | ✅ Yes | ❌ No | ❌ No | ⚠️ Sometimes |
| **Cost** | 💰 Free (local) or Pay-per-use | 💰 Time | 💰 Subscription | 💰 Varies |

### Why Choose SmartGen?

- **Policy-Driven**: Unlike ChatGPT or Copilot, SmartGen enforces DDD patterns through configurable policies, ensuring architectural consistency
- **Transparent**: Debug mode shows exactly how code is generated, making it educational
- **Flexible**: Use free local models or premium cloud APIs based on your needs
- **Secure**: API keys never leave your machine or get committed to repositories

---

## 📖 Documentation

### Commands

#### `smartgen init`
Initialize a new project with SmartGen configuration.

```bash
smartgen init --language python --pattern ddd --app api
```

**Options:**
- `--language` - Project language (default: `python`)
- `--pattern` - Architecture pattern (default: `ddd`)
- `--app` - Application type (default: `api`)

#### `smartgen llmconfig`
Manage LLM provider configuration.

```bash
# Add a provider
smartgen llmconfig add ollama local --model deepseek-coder-v2

# List providers
smartgen llmconfig show

# Set default provider
smartgen llmconfig set-default ollama

# Remove a provider
smartgen llmconfig remove ollama
```

#### `smartgen generate domain`
Generate domain layer code based on SRS and DDD policies.

```bash
# Normal mode
smartgen generate domain

# Debug mode - shows all steps, prompts, and LLM responses
smartgen generate domain --debug
```

**Requirements:**
- `.smartgen.yml` must exist (run `smartgen init` first)
- `srs.md` must contain requirements

**Debug Output Includes:**
- Project configuration
- SRS content
- DDD policy rules
- Complete prompt sent to LLM
- Full LLM response
- Each file being created

#### `smartgen generate layout`
Generate application layout structure (application, infrastructure, interface layers).

```bash
smartgen generate layout
```

---

## ⚙️ Configuration

### Project Configuration (`.smartgen.yml`)

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
  - ✅ Free
  - ✅ Private (data stays local)
  - ✅ No API costs

#### Cloud Providers (OpenAI API)
- **Codex Models** - code-davinci-002, code-cushman-002 (specialized for code generation)
  - ✅ Best code quality
  - ✅ Optimized for code generation
  - ⚠️ Requires API key
- **Chat Models** - GPT-4, GPT-3.5-turbo (general purpose)
  - ✅ Versatile
  - ⚠️ May require JSON mode configuration

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

---

## 📸 Examples

### Example: E-Commerce Domain

**Input (`srs.md`):**
```markdown
# E-Commerce Domain

## User Management
- Users register with email and password
- Users have profiles with name and address
- Users can have roles (Customer, Admin)

## Product Catalog
- Products have name, description, price, and stock
- Products belong to categories
```

**Output (Generated Code):**
```python
# src/domain/entities/user.py
class User:
    def __init__(self, user_id: UserId, email: Email, ...):
        # Generated DDD-compliant entity
        ...

# src/domain/value_objects/email.py
class Email:
    def __init__(self, value: str):
        # Generated value object with validation
        ...
```

See the [`examples/`](examples/) directory for complete examples.

---

## 🏗️ Generated Project Structure

SmartGen generates code following Clean Architecture principles:

```
your-project/
├── src/
│   ├── domain/              # Domain layer (entities, value objects, aggregates)
│   │   └── {domain}/
│   │       ├── entities/
│   │       ├── value_objects/
│   │       └── aggregates/
│   ├── application/         # Application layer (use cases)
│   │   └── {domain}/
│   │       └── use_cases/
│   ├── infrastructure/      # Infrastructure layer (repositories, external services)
│   │   └── {domain}/
│   │       └── repositories/
│   └── interface/         # Interface layer (API, CLI, etc.)
│       └── http/
├── srs.md                  # Your requirements
└── .smartgen.yml           # Project configuration
```

---

## 🔒 Security

SmartGen follows security best practices:

- **API Keys**: Stored in `~/.smartgen/.llmconfig` (global config), never in project files
- **Project Config**: `.smartgen.yml` contains no sensitive data and is safe to commit
- **Local Option**: Use Ollama for completely private, local code generation

See [SECURITY.md](SECURITY.md) for details.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sidxz/smartgen.git
cd smartgen

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
black --check .
```

---

## 📚 Learn More

- [Examples](examples/) - See SmartGen in action
- [Roadmap](ROADMAP.md) - Upcoming features
- [Security](SECURITY.md) - Security best practices
- [Contributing](CONTRIBUTING.md) - How to contribute

---

## 🛣️ Roadmap

- [ ] Support for TypeScript/JavaScript
- [ ] Support for Java/Kotlin
- [ ] Interactive mode with prompts
- [ ] Custom template support
- [ ] VS Code extension
- [ ] Web UI for visual domain modeling
- [ ] Integration with popular frameworks (FastAPI, Django, etc.)

See [ROADMAP.md](ROADMAP.md) for the full roadmap.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by Clean Architecture principles by Robert C. Martin
- Domain-Driven Design concepts by Eric Evans
- Built with [Typer](https://typer.tiangolo.com/), [Rich](https://github.com/Textualize/rich), and [Ollama](https://ollama.ai)

---

<div align="center">

**Made with ❤️ for the DDD/Clean Architecture community**

⭐ **Star this repo if you find it useful!**

[Report Bug](https://github.com/sidxz/smartgen/issues) • [Request Feature](https://github.com/sidxz/smartgen/issues) • [Discussions](https://github.com/sidxz/smartgen/discussions)

</div>
