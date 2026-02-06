# Quick Start Guide

Get up and running with SmartGen in 5 minutes!

## Prerequisites

- Python 3.12 or higher
- (Optional) Ollama installed for local LLM usage

## Installation

```bash
pip install smartgen
```

## Quick Start (3 Steps)

### Step 1: Configure LLM Provider

**Option A: Use Ollama (Recommended for beginners - Free & Local)**

```bash
# Install Ollama: https://ollama.ai
ollama pull deepseek-coder-v2

# Configure SmartGen
smartgen llmconfig add ollama local --model deepseek-coder-v2
smartgen llmconfig set-default ollama
```

**Option B: Use OpenAI (Requires API Key)**

```bash
# Get your API key from https://platform.openai.com/api-keys
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key YOUR_API_KEY
smartgen llmconfig set-default codex
```

### Step 2: Initialize Your Project

```bash
mkdir my-ddd-project
cd my-ddd-project
smartgen init --language python --pattern ddd --app api
```

This creates:
- `.smartgen.yml` - Project configuration
- `srs.md` - Template for your requirements

### Step 3: Write Requirements & Generate

1. **Edit `srs.md`** with your domain requirements:

```markdown
# E-Commerce Domain

## User Management
- Users register with email and password
- Users have profiles with name and address
- Users can have roles (Customer, Admin)

## Product Catalog
- Products have name, description, price, and stock
- Products belong to categories
- Products can be active or inactive
```

2. **Generate domain code**:

```bash
smartgen generate domain
```

3. **View generated code**:

```
src/
└── domain/
    ├── entities/
    │   ├── user.py
    │   └── product.py
    ├── value_objects/
    │   ├── email.py
    │   ├── address.py
    │   └── money.py
    └── aggregates/
        └── order.py
```

## What's Next?

- 📖 Read the [full documentation](readme.md)
- 🎯 Check out [examples](examples/)
- 🚀 Generate application layout: `smartgen generate layout`
- 🐛 Enable debug mode: `smartgen generate domain --debug`
- 💬 Join [GitHub Discussions](https://github.com/sidxz/smartgen/discussions)

## Troubleshooting

### "API key not configured"
Make sure you've added your LLM provider:
```bash
smartgen llmconfig show  # Check configured providers
```

### "srs.md not found"
Run `smartgen init` first to create the project structure.

### "LLM call failed"
- Check your internet connection (for cloud providers)
- Verify Ollama is running (for local providers): `ollama list`
- Try debug mode: `smartgen generate domain --debug`

## Need Help?

- 📚 [Documentation](readme.md)
- 💬 [GitHub Discussions](https://github.com/sidxz/smartgen/discussions)
- 🐛 [Report Issues](https://github.com/sidxz/smartgen/issues)
- 📧 Check [Examples](examples/) for more use cases

---

**Happy Coding! 🚀**
