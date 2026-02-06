# Security: API Keys in SmartGen

## Overview

SmartGen follows security best practices by separating configuration into two files:

### 1. Global Configuration (`~/.smartgen/.llmconfig`)
**Location:** `~/.smartgen/.llmconfig` in your home directory  
**Purpose:** Stores sensitive information like API keys  
**Visibility:** Private to you, never committed to git

```json
{
  "llm": {
    "default": "codex",
    "providers": {
      "codex": {
        "type": "cloud",
        "model": "code-davinci-002",
        "api_key": "sk-proj-abc123..."
      },
      "gpt4": {
        "type": "cloud",
        "model": "gpt-4",
        "api_key": "sk-proj-xyz789..."
      },
      "ollama": {
        "type": "local",
        "model": "deepseek-coder-v2",
        "url": "http://localhost:11434"
      }
    }
  }
}
```

### 2. Project Configuration (`.smartgen.yml`)
**Location:** Project root directory  
**Purpose:** Project-specific settings (language, pattern, provider references)  
**Visibility:** Safe to commit to git - contains no secrets

```yaml
project:
  language: python
  pattern: ddd
  app: api

llm:
  default: codex
  providers:
    codex:
      type: cloud
      model: code-davinci-002
      # api_key is NOT here - it's in ~/.smartgen/.llmconfig
    
    ollama:
      type: local
      model: deepseek-coder-v2
      url: http://localhost:11434
```

## How It Works

### During `smartgen init`

1. Reads your global config from `~/.smartgen/.llmconfig`
2. Gets the default provider configuration
3. **Removes API keys** before writing to `.smartgen.yml`
4. Writes sanitized config to project directory

```bash
$ smartgen init

# Creates .smartgen.yml WITHOUT api_key
✓ Initialized with provider 'codex'.
✓ Created .smartgen.yml
```

### During `smartgen generate domain`

1. Reads `.smartgen.yml` from project (no API keys)
2. Reads `~/.smartgen/.llmconfig` from global config (has API keys)
3. **Merges them together** to get complete configuration
4. Uses the merged config to call the LLM

```bash
$ smartgen generate domain

# Automatically merges project + global config
✓ Domain elements generated using provider 'codex'.
```

## Benefits

### ✅ Security
- API keys never in version control
- No accidental key exposure in commits
- Keys stored only in your home directory

### ✅ Team Collaboration
- Everyone has their own API keys
- `.smartgen.yml` can be shared safely
- Team uses same provider/model settings

### ✅ Multi-Project
- Configure API key once
- Use across all projects
- Update key in one place

### ✅ Git-Friendly
```gitignore
# .gitignore
# No need to ignore .smartgen.yml - it's safe!
# But you might want to ignore generated code:
src/domain/
```

## Example Workflow

### Developer A (Using OpenAI)
```bash
# Setup once
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key sk-...
smartgen llmconfig set-default codex

# Clone team repo
git clone https://github.com/team/project.git
cd project

# Generate domain (uses their own API key)
smartgen generate domain
```

### Developer B (Using Ollama)
```bash
# Setup once
smartgen llmconfig add ollama local --model deepseek-coder-v2
smartgen llmconfig set-default ollama

# Clone same team repo
git clone https://github.com/team/project.git
cd project

# Edit .smartgen.yml to use ollama
vim .smartgen.yml  # Change default: codex -> default: ollama

# Generate domain (uses local Ollama, no API key needed)
smartgen generate domain
```

## Migration

If you have old `.smartgen.yml` files with API keys:

```bash
# 1. Backup the API key
cat .smartgen.yml  # Note down the api_key

# 2. Add to global config
smartgen llmconfig add myprovider cloud --model MODEL --api-key KEY

# 3. Remove from project file
# Edit .smartgen.yml and delete the api_key line

# 4. Verify it still works
smartgen generate domain --debug
```

## Environment Variables (Alternative)

For CI/CD pipelines, you can also use environment variables:

```bash
# Set API key via environment
export OPENAI_API_KEY=sk-...

# SmartGen will automatically use it
smartgen generate domain
```

## Troubleshooting

### Error: "API key not configured"

```
✗ API key not configured for provider 'codex'.
```

**Solution:** Add the API key to global config:
```bash
smartgen llmconfig add codex cloud --model code-davinci-002 --api-key sk-...
```

### API key in `.smartgen.yml`

If you manually edited `.smartgen.yml` and added an `api_key`:

**Warning:** Remove it! It will work but is insecure.

```yaml
# ❌ Don't do this:
codex:
  type: cloud
  model: code-davinci-002
  api_key: sk-...  # INSECURE!

# ✅ Do this instead:
codex:
  type: cloud
  model: code-davinci-002
  # api_key in ~/.smartgen/.llmconfig
```

## Summary

| File | Location | Contains | Git? |
|------|----------|----------|------|
| `.llmconfig` | `~/.smartgen/` | API keys, secrets | Never commit |
| `.smartgen.yml` | Project root | Model names, settings | Safe to commit |

**Remember:** API keys belong in `~/.smartgen/.llmconfig`, not in `.smartgen.yml`! 🔒
