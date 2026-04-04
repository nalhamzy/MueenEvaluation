"""Model registry — pre-configured LLM providers and models for evaluation.

Each model entry specifies:
  - provider: which API provider hosts this model
  - model_id: the actual model ID to send to the API
  - display_name: human-readable name for the UI
  - api_base: the OpenAI-compatible base URL
  - env_key: which .env variable holds the API key
  - requires_thinking_off: whether to disable thinking mode (Qwen3.5+)
"""

PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "base_url": None,  # default OpenAI endpoint
        "env_key": "OPENAI_API_KEY",
    },
    "anthropic": {
        "name": "Anthropic",
        "base_url": None,  # uses Anthropic SDK directly
        "env_key": "CLAUDE_API_KEY",
    },
    "dashscope": {
        "name": "Alibaba Dashscope",
        "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "env_key": "QWEN",
    },
    "mistral": {
        "name": "Mistral AI",
        "base_url": "https://api.mistral.ai/v1",
        "env_key": "MISTRAL_API_KEY",
    },
    "together": {
        "name": "Together AI",
        "base_url": "https://api.together.xyz/v1",
        "env_key": "TOGETHER_API_KEY",
    },
    "fireworks": {
        "name": "Fireworks AI",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "env_key": "FIREWORKS_API_KEY",
    },
    "groq": {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
    },
    "bedrock": {
        "name": "AWS Bedrock",
        "base_url": None,  # uses boto3 converse API
        "env_key": "AWS_ACCESS_KEY_ID",  # checks if AWS creds are configured
    },
}

MODELS = [
    # --- OpenAI ---
    {
        "id": "gpt-4o-mini",
        "display_name": "GPT-4o Mini",
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "category": "openai",
    },
    {
        "id": "gpt-4o",
        "display_name": "GPT-4o",
        "provider": "openai",
        "model_id": "gpt-4o",
        "category": "openai",
    },
    {
        "id": "gpt-5.2",
        "display_name": "GPT-5.2",
        "provider": "openai",
        "model_id": "gpt-5.2",
        "category": "openai",
    },
    {
        "id": "gpt-5.4-pro",
        "display_name": "GPT-5.4 Pro",
        "provider": "openai",
        "model_id": "gpt-5.4-pro",
        "category": "openai",
    },

    # --- Anthropic (Claude) ---
    {
        "id": "claude-haiku-4-5",
        "display_name": "Claude Haiku 4.5",
        "provider": "anthropic",
        "model_id": "claude-haiku-4-5-20251001",
        "category": "anthropic",
    },
    {
        "id": "claude-sonnet-4-6",
        "display_name": "Claude Sonnet 4.6",
        "provider": "anthropic",
        "model_id": "claude-sonnet-4-6",
        "category": "anthropic",
    },
    {
        "id": "claude-opus-4-6",
        "display_name": "Claude Opus 4.6",
        "provider": "anthropic",
        "model_id": "claude-opus-4-6",
        "category": "anthropic",
    },

    # --- Qwen (Dashscope) ---
    {
        "id": "qwen3.5-397b-a17b",
        "display_name": "Qwen 3.5 397B-A17B (MoE)",
        "provider": "dashscope",
        "model_id": "qwen3.5-397b-a17b",
        "category": "qwen",
    },
    {
        "id": "qwen3.5-35b-a3b",
        "display_name": "Qwen 3.5 35B-A3B",
        "provider": "dashscope",
        "model_id": "qwen3.5-35b-a3b",
        "category": "qwen",
    },
    {
        "id": "qwen3-235b-a22b",
        "display_name": "Qwen 3 235B-A22B (MoE)",
        "provider": "dashscope",
        "model_id": "qwen3-235b-a22b",
        "category": "qwen",
    },
    {
        "id": "qwen3-max",
        "display_name": "Qwen 3 Max",
        "provider": "dashscope",
        "model_id": "qwen3-max",
        "category": "qwen",
    },

    # --- Mistral (AWS Bedrock) ---
    {
        "id": "mistral-large-bedrock",
        "display_name": "Mistral Large (Bedrock)",
        "provider": "bedrock",
        "model_id": "mistral.mistral-large-2402-v1:0",
        "category": "mistral",
    },

    # --- Mistral (Mistral AI API — requires MISTRAL_API_KEY) ---
    {
        "id": "mistral-large-latest",
        "display_name": "Mistral Large (API)",
        "provider": "mistral",
        "model_id": "mistral-large-latest",
        "category": "mistral",
    },
    {
        "id": "mistral-small-latest",
        "display_name": "Mistral Small (API)",
        "provider": "mistral",
        "model_id": "mistral-small-latest",
        "category": "mistral",
    },

    # --- Meta Llama (AWS Bedrock) ---
    {
        "id": "llama-3.3-70b-bedrock",
        "display_name": "Llama 3.3 70B Instruct (Bedrock)",
        "provider": "bedrock",
        "model_id": "us.meta.llama3-3-70b-instruct-v1:0",
        "category": "llama",
    },

    # --- Meta Llama (via Together AI — requires TOGETHER_API_KEY) ---
    {
        "id": "llama-4-maverick-17b",
        "display_name": "Llama 4 Maverick 17B (Together)",
        "provider": "together",
        "model_id": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-Turbo",
        "category": "llama",
    },
    {
        "id": "llama-3.3-70b-together",
        "display_name": "Llama 3.3 70B (Together)",
        "provider": "together",
        "model_id": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "category": "llama",
    },

    # --- Meta Llama (via Groq — requires GROQ_API_KEY) ---
    {
        "id": "llama-3.3-70b-groq",
        "display_name": "Llama 3.3 70B (Groq)",
        "provider": "groq",
        "model_id": "llama-3.3-70b-versatile",
        "category": "llama",
    },

    # --- DeepSeek (via Dashscope) ---
    {
        "id": "deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "dashscope",
        "model_id": "deepseek-v3.2",
        "category": "deepseek",
    },
]


def get_model_registry() -> list[dict]:
    """Return all models with their provider info resolved."""
    result = []
    for model in MODELS:
        provider = PROVIDERS.get(model["provider"], {})
        result.append({
            **model,
            "provider_name": provider.get("name", model["provider"]),
            "base_url": provider.get("base_url"),
            "env_key": provider.get("env_key", ""),
        })
    return result


def get_model_by_id(model_id: str) -> dict | None:
    """Look up a model by its registry ID."""
    for model in MODELS:
        if model["id"] == model_id:
            provider = PROVIDERS.get(model["provider"], {})
            return {
                **model,
                "provider_name": provider.get("name", model["provider"]),
                "base_url": provider.get("base_url"),
                "env_key": provider.get("env_key", ""),
            }
    return None


def get_api_key_for_model(model_id: str) -> tuple[str, str | None]:
    """Returns (api_key, base_url) for a model, reading from environment."""
    import os
    model = get_model_by_id(model_id)
    if not model:
        return "", None

    env_key = model.get("env_key", "")
    api_key = os.environ.get(env_key, "")

    # Fallback: try reading from .env directly
    if not api_key:
        try:
            from config import settings
            api_key = getattr(settings, env_key, "")
        except Exception:
            pass

    return api_key, model.get("base_url")
