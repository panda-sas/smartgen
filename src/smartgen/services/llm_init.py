"""LLM initialization service for project setup."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional
import json
import concurrent.futures
import time

from smartgen.config import ConfigManager


class LLMInitError(RuntimeError):
    """Base error for LLM init operations."""


class MissingConfigError(LLMInitError):
    """Raised when no LLM configuration is available."""


class MissingApiKeyError(LLMInitError):
    """Raised when a cloud provider has no API key configured."""


class UnsupportedLocalProviderError(LLMInitError):
    """Raised when a local provider is not supported."""


@dataclass(frozen=True)
class InitResult:
    """Result of initializing smartgen in a project directory."""

    provider_name: str
    provider_config: dict[str, Any]
    yaml_path: Path
    pull_response: Optional[str] = None


class LLMInitService:
    """Service for initializing smartgen with an LLM provider."""

    OLLAMA_PULL_TIMEOUT_SECONDS = 600

    def __init__(
        self,
        config_manager: type[ConfigManager] = ConfigManager,
        ollama_client_factory: Optional[Callable[[str], Any]] = None,
        ollama_progress_callback: Optional[Callable[[dict[str, Any]], None]] = None,
    ) -> None:
        self._config_manager = config_manager
        self._ollama_client_factory = ollama_client_factory
        self._ollama_progress_callback = ollama_progress_callback

    def initialize(self, target_dir: Path) -> InitResult:
        """Initialize smartgen in the target directory."""
        llm_config = self._config_manager.get_llm_config()
        if not llm_config:
            raise MissingConfigError(
                "No LLM configuration found. Run 'smartgen llmconfig set-config' first."
            )

        default_provider = llm_config.get("default")
        if not default_provider:
            raise MissingConfigError(
                "No default provider configured. Set one via 'smartgen llmconfig set-default'."
            )

        providers = llm_config.get("providers", {})
        provider_config = providers.get(default_provider)
        if not provider_config:
            raise MissingConfigError(
                f"Default provider '{default_provider}' not found in configuration."
            )

        provider_type = provider_config.get("type")
        pull_response: Optional[str] = None
        normalized_provider_config = dict(provider_config)

        if provider_type == "cloud":
            if not provider_config.get("api_key"):
                raise MissingApiKeyError(
                    f"API key not configured for provider '{default_provider}'."
                )
        elif provider_type == "local":
            if default_provider.lower() != "ollama":
                raise UnsupportedLocalProviderError(
                    "Only Ollama is supported for local providers right now."
                )
            model = provider_config.get("model") or "deepseek-coder-v2"
            url = provider_config.get("url") or "http://localhost:11434"
            normalized_provider_config["model"] = model
            normalized_provider_config["url"] = url
            pull_response = self._pull_ollama_model(model=model, url=url)
        else:
            raise LLMInitError(
                f"Unknown provider type '{provider_type}'."
            )

        yaml_path = self._write_project_config(
            target_dir=target_dir,
            provider_name=default_provider,
            provider_config=normalized_provider_config,
        )

        return InitResult(
            provider_name=default_provider,
            provider_config=normalized_provider_config,
            yaml_path=yaml_path,
            pull_response=pull_response,
        )

    def _write_project_config(
        self,
        target_dir: Path,
        provider_name: str,
        provider_config: dict[str, Any],
    ) -> Path:
        """Write the .smartgen.yml file to the target directory."""
        from yaml import safe_dump

        target_dir.mkdir(parents=True, exist_ok=True)
        yaml_path = target_dir / ".smartgen.yml"
        if yaml_path.exists():
            raise LLMInitError(
                f"'{yaml_path.name}' already exists in {target_dir}."
            )

        config_payload = {
            "llm": {
                "default": provider_name,
                "providers": {
                    provider_name: provider_config,
                },
            }
        }

        yaml_content = safe_dump(
            config_payload,
            sort_keys=False,
            default_flow_style=False,
        )
        yaml_path.write_text(yaml_content, encoding="utf-8")
        return yaml_path

    def _pull_ollama_model(self, model: str, url: str) -> str:
        """Pull the model from Ollama and return response as JSON."""
        try:
            client = self._get_ollama_client(url)
            response = None
            if self._ollama_progress_callback:
                response = self._pull_ollama_model_streaming(client, model)
            if response is None:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(client.pull, model)
                    response = future.result(timeout=self.OLLAMA_PULL_TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError as exc:
            raise LLMInitError(
                "Ollama pull timed out after "
                f"{self.OLLAMA_PULL_TIMEOUT_SECONDS}s. "
                "Ensure the Ollama server is running and reachable."
            ) from exc
        except TimeoutError as exc:
            raise LLMInitError(
                "Ollama pull timed out after "
                f"{self.OLLAMA_PULL_TIMEOUT_SECONDS}s. "
                "Ensure the Ollama server is running and reachable."
            ) from exc
        except Exception as exc:  # pragma: no cover - external dependency
            raise LLMInitError(
                f"Failed to pull model '{model}' from Ollama at {url}: {exc}. "
                "Ensure Ollama is running and the URL is correct."
            ) from exc

        return self._serialize_ollama_response(response)

    def _pull_ollama_model_streaming(self, client: Any, model: str) -> Optional[Any]:
        """Stream pull progress updates when supported by the client."""
        start_time = time.monotonic()
        try:
            response_iter = client.pull(model, stream=True)
        except TypeError:
            return None

        last_payload: Optional[Any] = None
        for payload in response_iter:
            last_payload = payload
            normalized_payload: Optional[dict[str, Any]] = None
            if isinstance(payload, dict):
                normalized_payload = payload
            elif hasattr(payload, "model_dump"):
                normalized_payload = payload.model_dump()
            elif hasattr(payload, "dict"):
                normalized_payload = payload.dict()

            try:
                if normalized_payload is not None and self._ollama_progress_callback:
                    self._ollama_progress_callback(normalized_payload)
            except Exception:
                pass
            if time.monotonic() - start_time > self.OLLAMA_PULL_TIMEOUT_SECONDS:
                raise TimeoutError("Ollama pull timed out")

        return last_payload

    def _serialize_ollama_response(self, response: Any) -> str:
        """Serialize Ollama responses to a readable JSON string."""
        if isinstance(response, str):
            return response
        if isinstance(response, dict):
            return json.dumps(response, indent=2, ensure_ascii=False)
        if hasattr(response, "model_dump"):
            return json.dumps(response.model_dump(), indent=2, ensure_ascii=False)
        if hasattr(response, "dict"):
            return json.dumps(response.dict(), indent=2, ensure_ascii=False)
        return json.dumps(str(response), indent=2, ensure_ascii=False)

    def _get_ollama_client(self, url: str) -> Any:
        """Return an Ollama client instance."""
        if self._ollama_client_factory:
            return self._ollama_client_factory(url)

        import ollama

        return ollama.Client(host=url)
