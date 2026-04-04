"""Shared LLM client with retry logic and call logging.
Supports OpenAI, Anthropic (Claude), and AWS Bedrock APIs."""

import time
import json
import re
from openai import OpenAI
from sqlalchemy.orm import Session
from models import LLMCallLog


def _is_claude_model(model: str) -> bool:
    return "claude" in model.lower()


def _is_bedrock_model(model: str) -> bool:
    """Detect AWS Bedrock model IDs (e.g. mistral.mistral-large-2402-v1:0)."""
    return any(
        model.lower().startswith(p)
        for p in ["mistral.", "us.meta.", "amazon.", "anthropic.", "ai21.", "cohere."]
    )


def _call_anthropic(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    json_mode: bool = False,
    max_tokens: int = 4096,
) -> tuple[str, dict]:
    """Call Anthropic Claude API. Returns (content, usage_dict)."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    response = client.messages.create(**kwargs)
    content = response.content[0].text if response.content else ""
    usage = {
        "prompt_tokens": response.usage.input_tokens if response.usage else None,
        "completion_tokens": response.usage.output_tokens if response.usage else None,
    }
    return content, usage


def _call_bedrock(
    model: str,
    system_prompt: str,
    user_prompt: str,
    json_mode: bool = False,
) -> tuple[str, dict]:
    """Call AWS Bedrock via converse API. Returns (content, usage_dict)."""
    import boto3
    import os

    client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    messages = [{"role": "user", "content": [{"text": user_prompt}]}]
    system = [{"text": system_prompt}]

    kwargs = {
        "modelId": model,
        "messages": messages,
        "system": system,
        "inferenceConfig": {"temperature": 0.2, "maxTokens": 4096},
    }

    response = client.converse(**kwargs)
    content = response["output"]["message"]["content"][0]["text"]
    usage = {
        "prompt_tokens": response.get("usage", {}).get("inputTokens"),
        "completion_tokens": response.get("usage", {}).get("outputTokens"),
    }
    return content, usage


def _call_openai(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    base_url: str | None = None,
    json_mode: bool = False,
) -> tuple[str, dict]:
    """Call OpenAI-compatible API. Returns (content, usage_dict)."""
    client = OpenAI(api_key=api_key, base_url=base_url)

    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    # Qwen thinking models: disable thinking to get clean output
    if "qwen" in model.lower() and ("dashscope" in (base_url or "")):
        kwargs["extra_body"] = {"enable_thinking": False}

    response = client.chat.completions.create(**kwargs)
    content = response.choices[0].message.content or ""
    usage = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
        "completion_tokens": response.usage.completion_tokens if response.usage else None,
    }
    return content, usage


def call_llm(
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    base_url: str | None = None,
    json_mode: bool = False,
    db: Session | None = None,
    task_type: str | None = None,
    max_retries: int = 3,
) -> str:
    """Call an LLM with exponential backoff retry.
    Auto-detects: Claude (Anthropic SDK), Bedrock (boto3), or OpenAI-compatible."""
    is_claude = _is_claude_model(model) and not _is_bedrock_model(model)
    is_bedrock = _is_bedrock_model(model)

    # For Claude/Bedrock JSON mode, add instruction to the prompt
    if (is_claude or is_bedrock) and json_mode:
        user_prompt = user_prompt + "\n\nIMPORTANT: Return valid JSON only. No markdown fences. No preamble."

    last_error = None
    for attempt in range(max_retries):
        start = time.time()
        try:
            if is_claude:
                content, usage = _call_anthropic(
                    api_key=api_key, model=model,
                    system_prompt=system_prompt, user_prompt=user_prompt,
                    json_mode=json_mode,
                )
            elif is_bedrock:
                content, usage = _call_bedrock(
                    model=model,
                    system_prompt=system_prompt, user_prompt=user_prompt,
                    json_mode=json_mode,
                )
            else:
                content, usage = _call_openai(
                    api_key=api_key, model=model, base_url=base_url,
                    system_prompt=system_prompt, user_prompt=user_prompt,
                    json_mode=json_mode,
                )

            latency_ms = int((time.time() - start) * 1000)

            if db:
                log = LLMCallLog(
                    model=model,
                    prompt_tokens=usage.get("prompt_tokens"),
                    completion_tokens=usage.get("completion_tokens"),
                    latency_ms=latency_ms,
                    success=True,
                    task_type=task_type,
                )
                db.add(log)
                db.commit()

            return content

        except Exception as e:
            last_error = e
            latency_ms = int((time.time() - start) * 1000)

            if db:
                log = LLMCallLog(
                    model=model,
                    latency_ms=latency_ms,
                    success=False,
                    error_message=str(e),
                    task_type=task_type,
                )
                db.add(log)
                db.commit()

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    raise last_error


def parse_json_response(text: str) -> dict | list:
    """Parse JSON from LLM response, stripping markdown fences if present."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    return json.loads(text)


def unwrap_json_list(data) -> list:
    """Unwrap a JSON response that may be a list or a dict wrapping a list."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                return v
    return []
