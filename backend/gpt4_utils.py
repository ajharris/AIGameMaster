# gpt4_utils.py

import os
import openai

def format_prompt(character_sheet, memory, player_input):
    prompt = f"Character: {character_sheet}\nMemory: {memory}\nPlayer: {player_input}"
    return prompt

def call_gpt4_api(prompt):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=256,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def truncate_memory(memory, max_messages=5):
    return memory[-max_messages:]
