# gpt4_utils.py

def format_prompt(character_sheet, memory, player_input):
    prompt = f"Character: {character_sheet}\nMemory: {memory}\nPlayer: {player_input}"
    return prompt

def call_gpt4_api(prompt):
    # This would call OpenAI API in production
    raise NotImplementedError

def truncate_memory(memory, max_messages=5):
    return memory[-max_messages:]
