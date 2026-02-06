"""Domain generation service using LLM."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
import json


class GeneratorError(RuntimeError):
    """Base error for generator operations."""


class MissingProjectConfigError(GeneratorError):
    """Raised when .smartgen.yml is not found."""


class MissingSRSError(GeneratorError):
    """Raised when srs.md is not found."""


class MissingPolicyError(GeneratorError):
    """Raised when policy file is not found."""


class LLMError(GeneratorError):
    """Raised when LLM call fails."""


@dataclass(frozen=True)
class DomainGenerationResult:
    """Result of domain generation."""

    provider_name: str
    generated_files: list[Path]
    llm_response: str


class DomainGeneratorService:
    """Service for generating domain elements using LLM."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize the domain generator service.
        
        Args:
            debug: Enable debug output for all steps
        """
        self._debug = debug

    def generate_domain(self, project_dir: Path) -> DomainGenerationResult:
        """
        Generate domain elements based on SRS and DDD policy.
        
        Args:
            project_dir: The project directory containing .smartgen.yml
            
        Returns:
            DomainGenerationResult with generated files and metadata
            
        Raises:
            GeneratorError: If configuration or required files are missing
        """
        if self._debug:
            self._print_debug("Starting domain generation", f"Project directory: {project_dir}")
        
        # 1. Load project configuration
        config = self._load_project_config(project_dir)
        
        if self._debug:
            self._print_debug("Configuration loaded", config, is_yaml=True)
        llm_config = config.get("llm", {})
        project_config = config.get("project", {})
        
        default_provider = llm_config.get("default")
        if not default_provider:
            raise GeneratorError("No default LLM provider configured in .smartgen.yml")
        
        providers = llm_config.get("providers", {})
        provider_config = providers.get(default_provider)
        if not provider_config:
            raise GeneratorError(f"Provider '{default_provider}' not found in configuration")
        
        # 2. Read SRS
        srs_content = self._read_srs(project_dir)
        
        if self._debug:
            self._print_debug("SRS Content", srs_content, is_text=True)
        
        # 3. Read DDD policy
        language = project_config.get("language", "python")
        policy_content = self._read_policy(language)
        
        if self._debug:
            self._print_debug("DDD Policy", policy_content[:500] + "..." if len(policy_content) > 500 else policy_content, is_text=True)
        
        # 4. Call LLM to generate domain elements
        if self._debug:
            self._print_debug("Calling LLM", f"Provider: {default_provider} ({provider_config.get('type')})")
        
        llm_response = self._call_llm(
            provider_config=provider_config,
            srs_content=srs_content,
            policy_content=policy_content,
        )
        
        if self._debug:
            self._print_debug("LLM Response", llm_response, is_text=True)
        
        # 5. Parse and write generated files
        generated_files = self._write_domain_files(
            project_dir=project_dir,
            llm_response=llm_response,
        )
        
        if self._debug:
            self._print_debug("Files Generated", f"Created {len(generated_files)} file(s)")
        
        return DomainGenerationResult(
            provider_name=default_provider,
            generated_files=generated_files,
            llm_response=llm_response,
        )

    def _load_project_config(self, project_dir: Path) -> dict[str, Any]:
        """Load .smartgen.yml from project directory."""
        config_path = project_dir / ".smartgen.yml"
        if not config_path.exists():
            raise MissingProjectConfigError(
                f"'.smartgen.yml' not found in {project_dir}. "
                "Run 'smartgen init' first."
            )
        
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _read_srs(self, project_dir: Path) -> str:
        """Read the Software Requirements Specification."""
        srs_path = project_dir / "srs.md"
        if not srs_path.exists():
            raise MissingSRSError(
                f"'srs.md' not found in {project_dir}. "
                "Please create the SRS file first."
            )
        
        content = srs_path.read_text(encoding="utf-8")
        if not content.strip():
            raise MissingSRSError(
                "srs.md is empty. Please provide requirements before generating domain."
            )
        
        return content

    def _read_policy(self, language: str) -> str:
        """Read the DDD domain policy file."""
        # Get the path to the policy file relative to this module
        policies_dir = Path(__file__).parent.parent / "policies" / "ddd" / language
        policy_path = policies_dir / "domain.txt"
        
        if not policy_path.exists():
            raise MissingPolicyError(
                f"Policy file not found for language '{language}' at {policy_path}"
            )
        
        return policy_path.read_text(encoding="utf-8")

    def _call_llm(
        self,
        provider_config: dict[str, Any],
        srs_content: str,
        policy_content: str,
    ) -> str:
        """
        Call the LLM to generate domain elements.
        
        Args:
            provider_config: LLM provider configuration
            srs_content: Content of the SRS
            policy_content: DDD policy rules
            
        Returns:
            LLM response containing generated code
        """
        provider_type = provider_config.get("type")
        
        # Build the prompt
        prompt = self._build_prompt(srs_content, policy_content)
        
        if self._debug:
            self._print_debug("Prompt sent to LLM", prompt, is_text=True)
        
        if provider_type == "local":
            return self._call_ollama(provider_config, prompt)
        elif provider_type == "cloud":
            return self._call_cloud_provider(provider_config, prompt)
        else:
            raise LLMError(f"Unsupported provider type: {provider_type}")

    def _build_prompt(self, srs_content: str, policy_content: str) -> str:
        """Build the prompt for the LLM."""
        return f"""You are a domain modeling expert. Based on the Software Requirements Specification (SRS) and the Domain-Driven Design (DDD) policy provided, generate the domain layer code.

# DDD Policy and Guidelines:
{policy_content}

# Software Requirements Specification:
{srs_content}

# Instructions:
1. Analyze the requirements in the SRS
2. Identify domain entities, value objects, aggregates, and domain services
3. Generate Python code following the DDD policy strictly
4. Organize code into proper directories (aggregates/, entities/, value_objects/, services/, errors/)
5. Include proper docstrings and type hints
6. Ensure all invariants are enforced in the domain models

# Output Format:
Return a JSON object with the following structure:
{{
    "files": [
        {{
            "path": "src/domain/aggregates/order.py",
            "content": "# Generated code here..."
        }},
        {{
            "path": "src/domain/value_objects/email.py",
            "content": "# Generated code here..."
        }}
    ]
}}

Generate the domain layer code now:"""

    def _call_ollama(self, provider_config: dict[str, Any], prompt: str) -> str:
        """Call Ollama local LLM."""
        try:
            import ollama
        except ImportError as exc:
            raise LLMError(
                "ollama package not installed. Install it with: pip install ollama"
            ) from exc
        
        url = provider_config.get("url", "http://localhost:11434")
        model = provider_config.get("model", "deepseek-coder-v2")
        
        try:
            client = ollama.Client(host=url)
            response = client.chat(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            
            return response["message"]["content"]
        except Exception as e:
            raise LLMError(f"Failed to call Ollama: {e}") from e

    def _call_cloud_provider(self, provider_config: dict[str, Any], prompt: str) -> str:
        """Call cloud LLM provider (OpenAI, Anthropic, etc.)."""
        # For now, support OpenAI-compatible APIs
        try:
            import openai
        except ImportError as exc:
            raise LLMError(
                "openai package not installed. Install it with: pip install openai"
            ) from exc
        
        api_key = provider_config.get("api_key")
        model = provider_config.get("model", "gpt-4")
        
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            
            return response.choices[0].message.content or ""
        except Exception as e:
            raise LLMError(f"Failed to call cloud provider: {e}") from e

    def _write_domain_files(
        self,
        project_dir: Path,
        llm_response: str,
    ) -> list[Path]:
        """
        Parse LLM response and write domain files.
        
        Args:
            project_dir: Project directory
            llm_response: LLM response containing generated code
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Extract JSON from response (handle cases where LLM adds extra text)
        json_start = llm_response.find("{")
        json_end = llm_response.rfind("}") + 1
        
        if json_start == -1 or json_end == 0:
            raise LLMError("No JSON found in LLM response")
        
        try:
            json_str = llm_response[json_start:json_end]
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise LLMError(f"Failed to parse LLM response as JSON: {e}") from e
        
        files = data.get("files", [])
        if not files:
            raise LLMError("No files generated by LLM")
        
        for file_info in files:
            file_path = project_dir / file_info["path"]
            file_content = file_info["content"]
            
            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            file_path.write_text(file_content, encoding="utf-8")
            generated_files.append(file_path)
            
            if self._debug:
                self._print_debug("Created file", str(file_path.relative_to(project_dir)))
        
        return generated_files
    
    def _print_debug(self, title: str, content: Any, is_yaml: bool = False, is_text: bool = False) -> None:
        """Print debug information with nice formatting.
        
        Args:
            title: Section title
            content: Content to display
            is_yaml: Format as YAML
            is_text: Format as plain text with text wrapping
        """
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.syntax import Syntax
            from rich.text import Text
            
            console = Console()
            
            if is_yaml:
                yaml_str = yaml.dump(content, default_flow_style=False, sort_keys=False)
                syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
                console.print(Panel(syntax, title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))
            elif is_text:
                # Wrap long text for readability
                text_obj = Text(str(content))
                console.print(Panel(text_obj, title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))
            else:
                console.print(Panel(str(content), title=f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))
            console.print()  # Empty line for spacing
        except ImportError:
            # Fallback if rich is not available
            print(f"\n=== {title} ===")
            print(content)
            print()
