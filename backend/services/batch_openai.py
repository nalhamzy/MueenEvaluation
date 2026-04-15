"""OpenAI Batch API client.

50% discount on calls vs synchronous API. SLA is 24h but typical completion
is 10-60 minutes. Used for the Judge (GPT-5.2) scoring.

Also works for any OpenAI-compatible Batch API (DeepSeek, etc).

Reference: https://platform.openai.com/docs/api-reference/batch
"""

import io
import json
import time

from openai import OpenAI  # module-level for test patching


def build_openai_batch_line(
    custom_id: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    json_mode: bool = False,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> str:
    """Build a single JSONL line for the OpenAI batch input file."""
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    line_obj = {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": body,
    }
    return json.dumps(line_obj, ensure_ascii=False)


def _make_client(api_key: str, base_url: str | None = None):
    return OpenAI(api_key=api_key, base_url=base_url)


def submit_openai_batch(
    api_key: str,
    lines: list[str],
    base_url: str | None = None,
    completion_window: str = "24h",
) -> str:
    """Upload a JSONL batch input file and create a batch. Returns batch_id."""
    client = _make_client(api_key, base_url)

    # Upload as a file object (BytesIO acts as file-like)
    content = "\n".join(lines).encode("utf-8")
    file_obj = io.BytesIO(content)
    file_obj.name = "batch_input.jsonl"  # required by OpenAI SDK

    uploaded = client.files.create(file=file_obj, purpose="batch")
    batch = client.batches.create(
        input_file_id=uploaded.id,
        endpoint="/v1/chat/completions",
        completion_window=completion_window,
    )
    return batch.id


def get_openai_batch_status(api_key: str, batch_id: str, base_url: str | None = None) -> dict:
    """Get current batch status."""
    client = _make_client(api_key, base_url)
    batch = client.batches.retrieve(batch_id)
    return {
        "id": batch.id,
        "status": batch.status,
        "request_counts": {
            "total": batch.request_counts.total if batch.request_counts else 0,
            "completed": batch.request_counts.completed if batch.request_counts else 0,
            "failed": batch.request_counts.failed if batch.request_counts else 0,
        },
        "output_file_id": batch.output_file_id,
        "error_file_id": batch.error_file_id,
    }


def wait_for_openai_batch(
    api_key: str,
    batch_id: str,
    base_url: str | None = None,
    poll_interval: int = 30,
    max_wait: int = 86400,
    progress_callback=None,
) -> dict:
    """Poll until the batch reaches a terminal state."""
    terminal = {"completed", "failed", "expired", "cancelled"}
    waited = 0
    while waited < max_wait:
        status = get_openai_batch_status(api_key, batch_id, base_url)
        if progress_callback:
            progress_callback(status)
        if status["status"] in terminal:
            return status
        time.sleep(poll_interval)
        waited += poll_interval
    raise TimeoutError(f"Batch {batch_id} did not finish within {max_wait}s")


def download_openai_batch_results(
    api_key: str,
    batch_id: str,
    base_url: str | None = None,
) -> dict[str, dict]:
    """Download results, return dict mapping custom_id → result.

    Each result has:
        {
            "status": "ok" | "error",
            "text": str (the model's content, if ok),
            "error": str (error details if any),
        }
    """
    client = _make_client(api_key, base_url)
    status = get_openai_batch_status(api_key, batch_id, base_url)

    results: dict[str, dict] = {}

    if status.get("output_file_id"):
        file_content = client.files.content(status["output_file_id"])
        text = file_content.text if hasattr(file_content, "text") else file_content.read().decode("utf-8")
        for line in text.strip().split("\n"):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                cid = obj.get("custom_id", "")
                response = obj.get("response", {})
                body = response.get("body", {}) if response else {}
                choices = body.get("choices", [])
                content = ""
                if choices:
                    content = choices[0].get("message", {}).get("content", "") or ""
                results[cid] = {"status": "ok", "text": content, "error": None}
            except Exception as e:
                results[obj.get("custom_id", "?") if isinstance(obj, dict) else "?"] = {
                    "status": "error",
                    "text": "",
                    "error": str(e),
                }

    if status.get("error_file_id"):
        try:
            err_content = client.files.content(status["error_file_id"])
            err_text = err_content.text if hasattr(err_content, "text") else err_content.read().decode("utf-8")
            for line in err_text.strip().split("\n"):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    cid = obj.get("custom_id", "?")
                    results[cid] = {
                        "status": "error",
                        "text": "",
                        "error": json.dumps(obj.get("error", obj)),
                    }
                except Exception:
                    pass
        except Exception:
            pass

    return results
