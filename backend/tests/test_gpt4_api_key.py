import os
import pytest
from backend import gpt4_utils


def test_openai_api_key_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-1234")
    # Should not raise error when key is set
    try:
        # Patch openai.ChatCompletion.create to avoid real API call
        import openai
        def fake_create(*args, **kwargs):
            return {'choices': [{'message': {'content': 'ok'}}]}
        monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
        result = gpt4_utils.call_gpt4_api("test prompt")
        assert result == "ok"
    except Exception as e:
        pytest.fail(f"Should not raise error when OPENAI_API_KEY is set: {e}")


def test_openai_api_key_missing(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as exc:
        gpt4_utils.call_gpt4_api("test prompt")
    assert "OPENAI_API_KEY environment variable not set" in str(exc.value)
