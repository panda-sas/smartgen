"""Pytest configuration and fixtures."""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_srs():
    """Sample SRS content for testing."""
    return """# E-Commerce Domain

## User Management
- Users register with email and password
- Users have profiles with name and address
- Users can have roles (Customer, Admin)

## Product Catalog
- Products have name, description, price, and stock
- Products belong to categories
"""


@pytest.fixture
def sample_smartgen_config():
    """Sample .smartgen.yml configuration."""
    return """project:
  language: python
  pattern: ddd
  app: api

llm:
  default: ollama
  providers:
    ollama:
      type: local
      model: deepseek-coder-v2
"""
