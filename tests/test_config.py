"""Tests for configuration management."""
import pytest
from pathlib import Path
from smartgen.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_ensure_config_dir(self, temp_dir, monkeypatch):
        """Test that config directory is created."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        config_dir = ConfigManager.ensure_config_dir()
        assert config_dir.exists()
        assert config_dir.is_dir()
    
    def test_load_config_nonexistent(self, temp_dir, monkeypatch):
        """Test loading config when file doesn't exist."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        config = ConfigManager.load_config()
        assert config == {}
    
    def test_save_and_load_config(self, temp_dir, monkeypatch):
        """Test saving and loading config."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        test_config = {"llm": {"default": "test"}}
        ConfigManager.save_config(test_config)
        
        loaded_config = ConfigManager.load_config()
        assert loaded_config == test_config
    
    def test_add_provider(self, temp_dir, monkeypatch):
        """Test adding a provider."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        ConfigManager.add_provider(
            name="test_provider",
            provider_type="local",
            model="test-model"
        )
        
        config = ConfigManager.load_config()
        assert "llm" in config
        assert "providers" in config["llm"]
        assert "test_provider" in config["llm"]["providers"]
        assert config["llm"]["providers"]["test_provider"]["type"] == "local"
        assert config["llm"]["providers"]["test_provider"]["model"] == "test-model"
        # First provider should be auto-set as default
        assert config["llm"]["default"] == "test_provider"
    
    def test_set_default_provider(self, temp_dir, monkeypatch):
        """Test setting default provider."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        ConfigManager.add_provider("provider1", "local", model="model1")
        ConfigManager.add_provider("provider2", "local", model="model2")
        ConfigManager.set_default_provider("provider2")
        
        config = ConfigManager.load_config()
        assert config["llm"]["default"] == "provider2"
    
    def test_set_default_provider_nonexistent(self, temp_dir, monkeypatch):
        """Test setting default provider that doesn't exist."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        with pytest.raises(ValueError, match="not found"):
            ConfigManager.set_default_provider("nonexistent")
    
    def test_remove_provider(self, temp_dir, monkeypatch):
        """Test removing a provider."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        ConfigManager.add_provider("provider1", "local", model="model1")
        ConfigManager.add_provider("provider2", "local", model="model2")
        ConfigManager.set_default_provider("provider1")
        
        ConfigManager.remove_provider("provider2")
        
        config = ConfigManager.load_config()
        assert "provider2" not in config["llm"]["providers"]
        assert config["llm"]["default"] == "provider1"  # Default unchanged
    
    def test_remove_default_provider(self, temp_dir, monkeypatch):
        """Test removing the default provider."""
        monkeypatch.setattr(ConfigManager, "CONFIG_DIR", temp_dir / ".smartgen")
        monkeypatch.setattr(ConfigManager, "CONFIG_FILE", temp_dir / ".smartgen" / ".llmconfig")
        
        ConfigManager.add_provider("provider1", "local", model="model1")
        ConfigManager.remove_provider("provider1")
        
        config = ConfigManager.load_config()
        assert "provider1" not in config["llm"]["providers"]
        assert "default" not in config["llm"]  # Default should be unset
