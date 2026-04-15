"""Anthropic Message Batches API client.

50% discount on calls vs synchronous API. SLA is 24h but typical completion
is 5-30 minutes. Used for the Teacher (Claude Opus) dataset generation.

Reference: https://docs.anthropic.com/en/api/creating-message-batches
"""

import time
from typing import Any

import anthropic  # imported at module level so tests can patch it


def build_anthropic_batch_requests(
    model: str,
    items: list[dict],
    max_tokens: int = 4096,
    temperature: float = 0.2,
) -> list[dict]:
    """Build the list of request dicts for the Anthropic Messages Batches API.

    Each item must have: custom_id (str), system (str), user (str).
    Optionally: max_tokens (int), temperature (float).

    Returns a list of dicts in the format expected by
    `client.messages.batches.create(requests=...)`.
    """
    out = []
    for item in items:
        params = {
            "model": model,
            "max_tokens": item.get("max_tokens", max_tokens),
            "temperature": item.get("temperature", temperature),
            "system": item["system"],
            "messages": [
                {"role": "user", "content": item["user"]},
            ],
        }
        out.append({
            "custom_id": item["custom_id"],
            "params": params,
        })
    return out


def submit_anthropic_batch(api_key: str, requests: list[dict]) -> str:
    """Submit a batch and return the batch ID."""
    client = anthropic.Anthropic(api_key=api_key)
    batch = client.messages.batches.create(requests=requests)
    return batch.id


def get_anthropic_batch_status(api_key: str, batch_id: str) -> dict:
    """Get current batch status. Returns dict with 'processing_status' and counts."""
    client = anthropic.Anthropic(api_key=api_key)
    batch = client.messages.batches.retrieve(batch_id)
    return {
        "id": batch.id,
        "processing_status": batch.processing_status,
        "request_counts": {
            "processing": batch.request_counts.processing,
            "succeeded": batch.request_counts.succeeded,
            "errored": batch.request_counts.errored,
            "canceled": batch.request_counts.canceled,
            "expired": batch.request_counts.expired,
        },
    }


def wait_for_anthropic_batch(
    api_key: str,
    batch_id: str,
    poll_interval: int = 30,
    max_wait: int = 86400,
    progress_callback=None,
) -> dict:
    """Poll until the batch is done. Returns the final status dict.

    progress_callback is called with the status dict after each poll.
    """
    waited = 0
    while waited < max_wait:
        status = get_anthropic_batch_status(api_key, batch_id)
        if progress_callback:
            progress_callback(status)
        if status["processing_status"] == "ended":
            return status
        time.sleep(poll_interval)
        waited += poll_interval
    raise TimeoutError(f"Batch {batch_id} did not finish within {max_wait}s")


def download_anthropic_batch_results(api_key: str, batch_id: str) -> dict[str, dict]:
    """Download all results, return a dict mapping custom_id → result.

    Each result has shape:
        {
            "type": "succeeded" | "errored" | ...,
            "text": str (the model's response, if succeeded),
            "raw": <the original SDK result object>,
        }
    """
    client = anthropic.Anthropic(api_key=api_key)

    results: dict[str, dict] = {}
    for entry in client.messages.batches.results(batch_id):
        custom_id = entry.custom_id
        result_type = entry.result.type

        text = ""
        if result_type == "succeeded":
            msg = entry.result.message
            if msg.content and len(msg.content) > 0:
                # First content block is the text response
                text = msg.content[0].text

        results[custom_id] = {
            "type": result_type,
            "text": text,
            "raw": entry,
        }

    return results
