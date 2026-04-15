"""Tests for batch API clients (Anthropic + OpenAI).

These tests mock the SDK calls so they run instantly without network.
"""

import sys
import os
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.batch_anthropic import (
    build_anthropic_batch_requests,
    submit_anthropic_batch,
    get_anthropic_batch_status,
    download_anthropic_batch_results,
)
from services.batch_openai import (
    build_openai_batch_line,
    submit_openai_batch,
    download_openai_batch_results,
)


# --- Anthropic batch tests ---

def test_anthropic_batch_request_construction():
    """Pure function: build correct request payload structure."""
    items = [
        {"custom_id": "ART_001:ner", "system": "JSON only.", "user": "Extract entities..."},
        {"custom_id": "ART_001:summary", "system": "Write Arabic.", "user": "Summarize..."},
    ]
    requests = build_anthropic_batch_requests(model="claude-opus-4-6", items=items)

    assert len(requests) == 2

    r0 = requests[0]
    assert r0["custom_id"] == "ART_001:ner"
    assert r0["params"]["model"] == "claude-opus-4-6"
    assert r0["params"]["system"] == "JSON only."
    assert r0["params"]["messages"][0]["role"] == "user"
    assert r0["params"]["messages"][0]["content"] == "Extract entities..."
    assert r0["params"]["max_tokens"] == 4096
    assert r0["params"]["temperature"] == 0.2

    r1 = requests[1]
    assert r1["custom_id"] == "ART_001:summary"


def test_anthropic_batch_per_item_overrides():
    """Per-item max_tokens and temperature should override defaults."""
    items = [
        {"custom_id": "x", "system": "s", "user": "u", "max_tokens": 8192, "temperature": 0.7},
    ]
    requests = build_anthropic_batch_requests(model="claude-opus-4-6", items=items)
    assert requests[0]["params"]["max_tokens"] == 8192
    assert requests[0]["params"]["temperature"] == 0.7


@patch("services.batch_anthropic.anthropic")
def test_submit_anthropic_batch_returns_id(mock_anthropic):
    """submit_anthropic_batch should return the batch.id from the SDK."""
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client
    mock_batch = MagicMock()
    mock_batch.id = "msgbatch_test_123"
    mock_client.messages.batches.create.return_value = mock_batch

    batch_id = submit_anthropic_batch(
        api_key="fake-key",
        requests=[{"custom_id": "x", "params": {}}],
    )
    assert batch_id == "msgbatch_test_123"
    mock_anthropic.Anthropic.assert_called_once_with(api_key="fake-key")
    mock_client.messages.batches.create.assert_called_once()


@patch("services.batch_anthropic.anthropic")
def test_get_anthropic_batch_status(mock_anthropic):
    """Status should return processing_status and request_counts."""
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client

    mock_batch = MagicMock()
    mock_batch.id = "msgbatch_xyz"
    mock_batch.processing_status = "in_progress"
    mock_batch.request_counts.processing = 50
    mock_batch.request_counts.succeeded = 50
    mock_batch.request_counts.errored = 0
    mock_batch.request_counts.canceled = 0
    mock_batch.request_counts.expired = 0

    mock_client.messages.batches.retrieve.return_value = mock_batch

    status = get_anthropic_batch_status(api_key="k", batch_id="msgbatch_xyz")
    assert status["id"] == "msgbatch_xyz"
    assert status["processing_status"] == "in_progress"
    assert status["request_counts"]["succeeded"] == 50
    assert status["request_counts"]["processing"] == 50


@patch("services.batch_anthropic.anthropic")
def test_download_anthropic_batch_results(mock_anthropic):
    """Results should be keyed by custom_id with text content."""
    mock_client = MagicMock()
    mock_anthropic.Anthropic.return_value = mock_client

    # Build a fake successful entry
    succeeded_entry = MagicMock()
    succeeded_entry.custom_id = "ART_001:ner"
    succeeded_entry.result.type = "succeeded"
    text_block = MagicMock()
    text_block.text = '{"PERSON": ["Ahmed"]}'
    succeeded_entry.result.message.content = [text_block]

    # Build a fake errored entry
    errored_entry = MagicMock()
    errored_entry.custom_id = "ART_002:ner"
    errored_entry.result.type = "errored"
    errored_entry.result.message = None

    mock_client.messages.batches.results.return_value = iter([succeeded_entry, errored_entry])

    results = download_anthropic_batch_results(api_key="k", batch_id="b")
    assert "ART_001:ner" in results
    assert results["ART_001:ner"]["type"] == "succeeded"
    assert results["ART_001:ner"]["text"] == '{"PERSON": ["Ahmed"]}'
    assert results["ART_002:ner"]["type"] == "errored"


# --- OpenAI batch tests ---

def test_openai_batch_jsonl_format():
    """build_openai_batch_line should return a valid JSONL line."""
    line = build_openai_batch_line(
        custom_id="ART_001:judge_summary",
        model="gpt-5.2",
        system_prompt="You are a judge.",
        user_prompt="Score this summary...",
        json_mode=True,
    )

    parsed = json.loads(line)
    assert parsed["custom_id"] == "ART_001:judge_summary"
    assert parsed["method"] == "POST"
    assert parsed["url"] == "/v1/chat/completions"
    body = parsed["body"]
    assert body["model"] == "gpt-5.2"
    assert body["response_format"] == {"type": "json_object"}
    assert body["messages"][0]["role"] == "system"
    assert body["messages"][0]["content"] == "You are a judge."
    assert body["messages"][1]["role"] == "user"
    assert body["messages"][1]["content"] == "Score this summary..."


def test_openai_batch_jsonl_no_json_mode():
    """When json_mode=False, response_format should NOT be in body."""
    line = build_openai_batch_line(
        custom_id="x",
        model="gpt-5.2",
        system_prompt="s",
        user_prompt="u",
        json_mode=False,
    )
    parsed = json.loads(line)
    assert "response_format" not in parsed["body"]


@patch("services.batch_openai.OpenAI")
def test_submit_openai_batch_uploads_and_creates(mock_openai_cls):
    """submit_openai_batch should upload file and create batch."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    mock_file = MagicMock()
    mock_file.id = "file_abc"
    mock_client.files.create.return_value = mock_file

    mock_batch = MagicMock()
    mock_batch.id = "batch_xyz"
    mock_client.batches.create.return_value = mock_batch

    batch_id = submit_openai_batch(
        api_key="fake",
        lines=[
            '{"custom_id": "1", "method": "POST", "url": "/v1/chat/completions", "body": {}}',
        ],
    )

    assert batch_id == "batch_xyz"
    mock_client.files.create.assert_called_once()
    mock_client.batches.create.assert_called_once_with(
        input_file_id="file_abc",
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )


@patch("services.batch_openai.OpenAI")
def test_download_openai_batch_results_parses_jsonl(mock_openai_cls):
    """download_openai_batch_results should parse JSONL output and extract content."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    # Mock batch status
    mock_batch = MagicMock()
    mock_batch.id = "b1"
    mock_batch.status = "completed"
    mock_batch.request_counts.total = 1
    mock_batch.request_counts.completed = 1
    mock_batch.request_counts.failed = 0
    mock_batch.output_file_id = "file_out"
    mock_batch.error_file_id = None
    mock_client.batches.retrieve.return_value = mock_batch

    # Mock the output file content (a single JSONL line)
    output_line = json.dumps({
        "custom_id": "ART_001:judge_summary",
        "response": {
            "body": {
                "choices": [{"message": {"content": '{"factual_accuracy": 3}'}}]
            }
        },
    })
    mock_file_resp = MagicMock()
    mock_file_resp.text = output_line
    mock_client.files.content.return_value = mock_file_resp

    results = download_openai_batch_results(api_key="k", batch_id="b1")

    assert "ART_001:judge_summary" in results
    assert results["ART_001:judge_summary"]["status"] == "ok"
    assert results["ART_001:judge_summary"]["text"] == '{"factual_accuracy": 3}'
