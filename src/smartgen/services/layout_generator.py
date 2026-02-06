"""Layout generation service using LLM."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
import json


class LayoutGeneratorError(RuntimeError):
    """Base error for layout generator operations."""


class MissingProjectConfigError(LayoutGeneratorError):
    """Raised when .smartgen.yml is not found."""


class MissingSRSError(LayoutGeneratorError):
    """Raised when srs.md is not found."""


class MissingPolicyError(LayoutGeneratorError):
    """Raised when policy file is not found."""


class LLMError(LayoutGeneratorError):
    """Raised when LLM call fails."""


@dataclass(frozen=True)
class LayoutGenerationResult:
    """Result of layout generation."""

    provider_name: str
    generated_files: list[Path]
    llm_response: str


class LayoutGeneratorService:
    """Service for generating application layout using LLM."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize the layout generator service.
        
        Args:
            debug: Enable debug output for all steps
        """
        self._debug = debug

    def generate_layout(self, project_dir: Path) -> LayoutGenerationResult:
        """
        Generate application, infrastructure, and interface layer structures based on SRS.
        
        Args:
            project_dir: The project directory containing .smartgen.yml
            
        Returns:
            LayoutGenerationResult with generated files and metadata
            
        Raises:
            LayoutGeneratorError: If configuration or required files are missing
        """
        if self._debug:
            self._print_debug("Starting layout generation", f"Project directory: {project_dir}")
        
        # 1. Load project configuration
        config = self._load_project_config(project_dir)
        
        if self._debug:
            self._print_debug("Configuration loaded", config, is_yaml=True)
        llm_config = config.get("llm", {})
        project_config = config.get("project", {})
        
        default_provider = llm_config.get("default")
        if not default_provider:
            raise LayoutGeneratorError("No default LLM provider configured in .smartgen.yml")
        
        providers = llm_config.get("providers", {})
        provider_config = providers.get(default_provider)
        if not provider_config:
            raise LayoutGeneratorError(f"Provider '{default_provider}' not found in configuration")
        
        # Merge with global config to get API keys
        provider_config = self._merge_with_global_config(default_provider, provider_config)
        
        # 2. Read SRS
        srs_content = self._read_srs(project_dir)
        
        if self._debug:
            self._print_debug("SRS Content", srs_content, is_text=True)
        
        # 3. Read layout policy
        language = project_config.get("language", "python")
        policy_content = self._read_policy(language)
        
        if self._debug:
            self._print_debug("Layout Policy", policy_content[:500] + "..." if len(policy_content) > 500 else policy_content, is_text=True)
        
        # 4. Read existing domain files
        domain_files_content = self._read_domain_files(project_dir)
        
        if self._debug:
            domain_summary = f"Found {len(domain_files_content)} domain file(s)"
            self._print_debug("Domain Files", domain_summary)
        
        # 5. Call LLM to generate layout structure
        if self._debug:
            self._print_debug("Calling LLM", f"Provider: {default_provider} ({provider_config.get('type')})")
        
        llm_response = self._call_llm(
            provider_config=provider_config,
            srs_content=srs_content,
            policy_content=policy_content,
            domain_files_content=domain_files_content,
        )
        
        if self._debug:
            self._print_debug("LLM Response", llm_response, is_text=True)
        
        # 6. Parse and write generated files
        generated_files = self._write_layout_files(
            project_dir=project_dir,
            llm_response=llm_response,
        )
        
        if self._debug:
            self._print_debug("Files Generated", f"Created {len(generated_files)} file(s)")
        
        return LayoutGenerationResult(
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
    
    def _merge_with_global_config(self, provider_name: str, project_config: dict[str, Any]) -> dict[str, Any]:
        """Merge project provider config with global config to get API keys.
        
        API keys are stored in ~/.smartgen/.llmconfig (global) but not in 
        .smartgen.yml (project) for security. This method merges them.
        
        Args:
            provider_name: Name of the provider
            project_config: Provider config from project .smartgen.yml
            
        Returns:
            Merged config with API keys from global config
        """
        from smartgen.config import ConfigManager
        
        merged_config = dict(project_config)
        
        # Load global config
        global_config = ConfigManager.load_config()
        global_llm = global_config.get("llm", {})
        global_providers = global_llm.get("providers", {})
        global_provider_config = global_providers.get(provider_name, {})
        
        # Merge sensitive fields from global config
        sensitive_fields = ["api_key", "api_secret", "token", "password"]
        for field in sensitive_fields:
            if field in global_provider_config and field not in merged_config:
                merged_config[field] = global_provider_config[field]
        
        return merged_config

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
                "srs.md is empty. Please provide requirements before generating layout."
            )
        
        return content

    def _read_policy(self, language: str) -> str:
        """Read the layout policy file."""
        # Get the path to the policy file relative to this module
        policies_dir = Path(__file__).parent.parent / "policies" / "ddd" / language
        policy_path = policies_dir / "layout.txt"
        
        if not policy_path.exists():
            raise MissingPolicyError(
                f"Policy file not found for language '{language}' at {policy_path}"
            )
        
        return policy_path.read_text(encoding="utf-8")

    def _read_domain_files(self, project_dir: Path) -> dict[str, str]:
        """Read all generated domain files from src/domain directory.
        
        Args:
            project_dir: The project directory
            
        Returns:
            Dictionary mapping relative file paths to their content
        """
        domain_dir = project_dir / "src" / "domain"
        domain_files = {}
        
        # If domain directory doesn't exist, return empty dict
        if not domain_dir.exists():
            return domain_files
        
        # Recursively read all Python files in the domain directory
        for file_path in domain_dir.rglob("*.py"):
            # Skip __pycache__ and other special directories
            if "__pycache__" in file_path.parts or file_path.name.startswith("."):
                continue
            
            # Get relative path from project directory
            relative_path = file_path.relative_to(project_dir)
            
            # Read file content
            try:
                content = file_path.read_text(encoding="utf-8")
                domain_files[str(relative_path)] = content
            except (OSError, UnicodeDecodeError) as e:
                # Skip files that can't be read
                if self._debug:
                    self._print_debug("Warning", f"Could not read {relative_path}: {e}")
                continue
        
        return domain_files

    def _call_llm(
        self,
        provider_config: dict[str, Any],
        srs_content: str,
        policy_content: str,
        domain_files_content: dict[str, str],
    ) -> str:
        """
        Call the LLM to generate layout structures.
        
        Args:
            provider_config: LLM provider configuration
            srs_content: Content of the SRS
            policy_content: Layout policy rules
            domain_files_content: Dictionary of domain file paths and their content
            
        Returns:
            LLM response containing generated code
        """
        provider_type = provider_config.get("type")
        
        # Build the prompt
        prompt = self._build_prompt(srs_content, policy_content, domain_files_content)
        
        if self._debug:
            self._print_debug("Prompt sent to LLM", prompt, is_text=True)
        
        if provider_type == "local":
            return self._call_ollama(provider_config, prompt)
        elif provider_type == "cloud":
            return self._call_cloud_provider(provider_config, prompt)
        else:
            raise LLMError(f"Unsupported provider type: {provider_type}")

    def _build_prompt(self, srs_content: str, policy_content: str, domain_files_content: dict[str, str]) -> str:
        """Build the prompt for the LLM."""
        # Format domain files for the prompt
        domain_files_section = ""
        if domain_files_content:
            domain_files_section = "\n# Existing Domain Layer Files:\n"
            for file_path, content in domain_files_content.items():
                domain_files_section += f"\n## {file_path}\n```python\n{content}\n```\n"
        
        return f"""You are a software architect specializing in layered architecture design. Based on the Software Requirements Specification (SRS), the existing Domain Layer files, and the layout policy provided, generate the structure (no implementations) for the Application, Infrastructure, and Interface layers.

# Layout Policy and Guidelines:
{policy_content}

# Software Requirements Specification:
{srs_content}
{domain_files_section}
# Instructions:
1. Analyze the requirements in the SRS
2. Review the existing domain models to understand what entities, value objects, and aggregates exist
3. Design the Application, Infrastructure, and Interface layers that work with these domain models
4. Organize files following the policy guidelines strictly
5. IMPORTANT: Return the generated structure in a JSON format with file paths and content as shown below:

# Output Format:
Return a JSON object with the following structure:
{{
    "files": [
        {{
            "path": "src/application/use_cases/create_order_use_case.py",
            "content": ""
        }},
        {{
            "path": "src/infrastructure/repositories/order_repository.py",
            "content": ""
        }},
        {{
            "path": "src/interface/controllers/order_controller.py",
            "content": ""
        }}
    ]
}}

Generate the application layout structure now:"""

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
        """Call cloud LLM provider (OpenAI chat models, Codex, etc.)."""
        import openai
        
        api_key = provider_config.get("api_key")
        model = provider_config.get("model", "gpt-4")
        base_url = provider_config.get("base_url")  # Support custom API endpoints
        
        # Determine if this is a Codex model (uses legacy completions API)
        is_codex = self._is_codex_model(model)
        
        try:
            client_kwargs: dict[str, Any] = {"api_key": api_key}
            base_url = provider_config.get("base_url")
            if base_url:
                client_kwargs["base_url"] = base_url
            
            client = openai.OpenAI(**client_kwargs)
            
            if is_codex:
                # Codex models use the legacy completions API
                if self._debug:
                    self._print_debug("Using Codex API", f"Model: {model} (legacy completions)")
                
                response = client.completions.create(
                    model=model,
                    prompt=prompt,
                    max_tokens=4000,
                    temperature=0.2,
                )
                return response.choices[0].text or ""
            else:
                # Modern chat models (GPT-3.5, GPT-4, etc.)
                if self._debug:
                    self._print_debug("Using Chat API", f"Model: {model}")
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert software architect. Return your response as valid JSON with this structure: {\"files\": [{\"path\": \"...\", \"content\": \"...\"}]}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                )
                return response.choices[0].message.content or ""
        except Exception as e:
            raise LLMError(f"Failed to call cloud provider: {e}") from e
    
    def _is_codex_model(self, model: str) -> bool:
        """Check if the model is a Codex model that uses completions API.
        
        Args:
            model: Model name
            
        Returns:
            True if it's a Codex model
        """
        codex_models = [
            "code-davinci-002",
            "code-davinci-001", 
            "code-cushman-002",
            "code-cushman-001",
        ]
        return model in codex_models or model.startswith("code-")
    
    def _parse_llm_json_response(self, response: str) -> dict[str, Any]:
        """Parse JSON from LLM response with robust error handling.
        
        Handles cases where the LLM wraps JSON in markdown code blocks
        or adds extra text around the JSON.
        
        Args:
            response: LLM response text
            
        Returns:
            Parsed JSON as dictionary
            
        Raises:
            LLMError: If JSON cannot be extracted or parsed
        """
        # Try to parse as-is first (if JSON mode was used)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        # Handle both ```json ... ``` and ``` ... ``` formats
        for fence in ["```json", "```"]:
            if fence in response:
                try:
                    start = response.find(fence) + len(fence)
                    end = response.find("```", start)
                    if end > start:
                        json_str = response[start:end].strip()
                        return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
        
        # Try to extract JSON by finding { ... }
        json_start = response.find("{")
        json_end = response.rfind("}")
        
        if json_start == -1 or json_end == -1 or json_end <= json_start:
            raise LLMError(
                "No valid JSON found in LLM response. "
                "Make sure the model is configured correctly and supports JSON output."
            )
        
        try:
            json_str = response[json_start:json_end + 1]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Show a helpful error message with a snippet of the response
            snippet = response[max(0, json_start):min(len(response), json_start + 200)]
            raise LLMError(
                f"Failed to parse JSON from LLM response: {e}\n"
                f"Response snippet: {snippet}..."
            ) from e

    def _write_layout_files(
        self,
        project_dir: Path,
        llm_response: str,
    ) -> list[Path]:
        """
        Parse LLM response and write layout files.
        
        Args:
            project_dir: Project directory
            llm_response: LLM response containing generated structure
            
        Returns:
            List of generated file paths
        """
        generated_files = []
        
        # Parse JSON from response
        data = self._parse_llm_json_response(llm_response)
        
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
