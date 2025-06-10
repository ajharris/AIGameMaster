import pytest
from unittest.mock import patch
from backend import gpt4_utils

# --- Tests ---
def test_prompt_formatting():
    character = "Name: Hero, System: D&D"
    memory = ["You enter a cave.", "A goblin appears."]
    player_input = "I attack!"
    prompt = gpt4_utils.format_prompt(character, memory, player_input)
    assert "Hero" in prompt and "goblin" in prompt and "I attack!" in prompt

def test_gpt4_api_call_success():
    prompt = "Test prompt"
    with patch("backend.gpt4_utils.call_gpt4_api", return_value="AI response") as mock_call:
        response = gpt4_utils.call_gpt4_api(prompt)
        assert response == "AI response"
        mock_call.assert_called_once_with(prompt)

def test_gpt4_api_call_error():
    prompt = "Test prompt"
    with patch("backend.gpt4_utils.call_gpt4_api", side_effect=Exception("API error")):
        with pytest.raises(Exception) as exc:
            gpt4_utils.call_gpt4_api(prompt)
        assert "API error" in str(exc.value)

def test_session_memory_truncation():
    memory = [f"msg{i}" for i in range(10)]
    truncated = gpt4_utils.truncate_memory(memory, max_messages=5)
    assert truncated == ["msg5", "msg6", "msg7", "msg8", "msg9"]
    assert len(truncated) == 5

def test_character_sheet_in_prompt():
    character = "Name: TestHero, System: D&D"
    memory = ["Scene 1"]
    player_input = "Look around."
    prompt = gpt4_utils.format_prompt(character, memory, player_input)
    assert "TestHero" in prompt and "Look around." in prompt
