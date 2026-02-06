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
    def update_llm_config(cls, default: str, api_key: str) -> None:
        """Update LLM configuration."""
        config = cls.load_config()
        if "llm" not in config:
            config["llm"] = {}
        config["llm"]["default"] = default
        config["llm"]["providers"] = config["llm"].get("providers", {})
        config["llm"]["providers"][default] = {"api_key": api_key}
        cls.save_config(config)

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
