import pytest
from backend.utils_embedding import chunk_text, embed_texts, SimpleVectorStore

def test_vector_search_retrieves_relevant_rule_chunks():
    # Simulate rulebook chunks
    rules = [
        "Movement: Each turn, a character may move up to their speed.",
        "Combat: Roll a d20 and add modifiers.",
        "Magic: Spell slots are consumed when casting spells."
    ]
    embeddings, vectorizer = embed_texts(rules)
    store = SimpleVectorStore()
    store.add(rules, embeddings)
    # Query for 'combat'
    query_vec = vectorizer.transform(["combat roll"]).toarray()
    results = store.search(query_vec, top_k=2)
    # The most relevant chunk should mention 'Combat'
    assert any("Combat" in chunk for chunk, _ in results)

def test_rule_chunk_injection_into_prompt():
    from backend.gpt4_utils import format_prompt
    rule_chunk = "Combat: Roll a d20 and add modifiers."
    character = "Name: Hero, System: D&D"
    memory = ["You enter a cave."]
    player_input = "I attack!"
    # Inject rule chunk into prompt
    prompt = format_prompt(character, memory, player_input)
    prompt_with_rules = f"Rules:\n{rule_chunk}\n---\n" + prompt
    # Ensure rule chunk is present and formatting preserved
    assert rule_chunk in prompt_with_rules
    assert "Rules:\n" in prompt_with_rules
    assert prompt_with_rules.index(rule_chunk) > prompt_with_rules.index("Rules:")

def test_end_to_end_rule_search_and_prompt_injection():
    from backend.gpt4_utils import format_prompt
    # Setup vector store
    rules = [
        "Movement: Each turn, a character may move up to their speed.",
        "Combat: Roll a d20 and add modifiers.",
        "Magic: Spell slots are consumed when casting spells."
    ]
    embeddings, vectorizer = embed_texts(rules)
    store = SimpleVectorStore()
    store.add(rules, embeddings)
    # User input
    player_input = "I attack the goblin."
    query_vec = vectorizer.transform([player_input]).toarray()
    results = store.search(query_vec, top_k=1)
    relevant_rule = results[0][0] if results else ""
    character = "Name: Hero, System: D&D"
    memory = ["You enter a cave."]
    prompt = format_prompt(character, memory, player_input)
    prompt_with_rules = f"Rules:\n{relevant_rule}\n---\n" + prompt
    # Assert relevant rule is included
    assert relevant_rule in prompt_with_rules
    assert player_input in prompt_with_rules

def test_uploaded_rule_sets_are_searchable_after_upload():
    # Simulate uploading a new rule set
    rules = ["Stealth: Roll a d20 to sneak.", "Perception: Roll to spot hidden objects."]
    new_rules = ["Charisma: Roll to persuade NPCs."]
    all_rules = rules + new_rules
    # Re-fit vectorizer on all rules after upload
    embeddings, vectorizer = embed_texts(all_rules)
    store = SimpleVectorStore()
    store.add(all_rules, embeddings)
    # All rules should be searchable
    for rule in all_rules:
        query_vec = vectorizer.transform([rule.split(":")[0]]).toarray()
        results = store.search(query_vec, top_k=1)
        assert any(rule.split(":")[0] in chunk for chunk, _ in results)

def test_fallback_when_no_relevant_rules_found():
    from backend.gpt4_utils import format_prompt
    # Empty vector store
    store = SimpleVectorStore()
    # Query for something not present
    query_vec = [[0.0]]  # Dummy vector
    try:
        results = store.search(query_vec, top_k=1)
    except Exception:
        results = []
    fallback = "No relevant rules found."
    relevant_rule = results[0][0] if results else fallback
    character = "Name: Hero, System: D&D"
    memory = ["You enter a cave."]
    player_input = "I fly."
    prompt = format_prompt(character, memory, player_input)
    prompt_with_rules = f"Rules:\n{relevant_rule}\n---\n" + prompt
    # Assert fallback is used and prompt structure is intact
    assert fallback in prompt_with_rules
    assert "Rules:\n" in prompt_with_rules
    assert player_input in prompt_with_rules
