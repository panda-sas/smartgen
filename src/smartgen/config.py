"""Configuration management for smartgen."""
import json
from pathlib import Path
from typing import Optional


class ConfigManager:
    """Manages configuration files and settings."""

    CONFIG_DIR = Path.home() / ".smartgen"
    CONFIG_FILE = CONFIG_DIR / ".llmconfig"

    @classmethod
    def ensure_config_dir(cls) -> Path:
        """Ensure the config directory exists."""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return cls.CONFIG_DIR

    @classmethod
    def load_config(cls) -> dict:
        """Load configuration from file."""
        cls.ensure_config_dir()
        if cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    @classmethod
    def save_config(cls, config: dict) -> None:
        """Save configuration to file."""
        cls.ensure_config_dir()
        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

    @classmethod
    def add_provider(
        cls,
        name: str,
        provider_type: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        """Add or update an LLM provider."""
        config = cls.load_config()
        if "llm" not in config:
            config["llm"] = {}
        if "providers" not in config["llm"]:
            config["llm"]["providers"] = {}

        # Check if this is the first provider
        is_first_provider = len(config["llm"]["providers"]) == 0

        provider_config = {"type": provider_type}

        if api_key:
            provider_config["api_key"] = api_key
        if model:
            provider_config["model"] = model
        else:
            # Set default model for local providers
            if provider_type == "local":
                provider_config["model"] = "deepseek-coder-v2"
        if url:
            provider_config["url"] = url
        else:
            # Set default URL for local providers
            if provider_type == "local":
                provider_config["url"] = "http://localhost:11434"

        config["llm"]["providers"][name] = provider_config

        # Auto-set as default if it's the first provider
        if is_first_provider:
            config["llm"]["default"] = name

        cls.save_config(config)

    @classmethod
    def set_default_provider(cls, provider_name: str) -> None:
        """Set the default provider."""
        config = cls.load_config()
        if "llm" not in config:
            config["llm"] = {}
        providers = config["llm"].get("providers", {})
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        config["llm"]["default"] = provider_name
        cls.save_config(config)

    @classmethod
    def remove_provider(cls, provider_name: str) -> None:
        """Remove a provider."""
        config = cls.load_config()
        if "llm" not in config:
            return
        providers = config["llm"].get("providers", {})
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        del config["llm"]["providers"][provider_name]
        # If this was the default, unset default
        if config["llm"].get("default") == provider_name:
            config["llm"].pop("default", None)
        cls.save_config(config)

    @classmethod
    def update_llm_config(cls, default: str, api_key: str) -> None:
        """Update LLM configuration (legacy)."""
        cls.add_provider(name=default, provider_type="cloud", api_key=api_key)
        cls.set_default_provider(default)

    @classmethod
    def get_llm_config(cls) -> Optional[dict]:
        """Get LLM configuration."""
        config = cls.load_config()
        return config.get("llm")

    @classmethod
    def get_api_key(cls, provider: Optional[str] = None) -> Optional[str]:
        """Get API key for a provider."""
        config = cls.load_config()
        llm_config = config.get("llm", {})
        if not provider:
            provider = llm_config.get("default")
        if provider and "providers" in llm_config:
            return llm_config["providers"].get(provider, {}).get("api_key")
        return None
