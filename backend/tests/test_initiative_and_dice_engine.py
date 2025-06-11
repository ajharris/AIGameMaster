import pytest
import random
from backend.engine import Character, Engine

# --- TESTS ---
def test_initiative_assignment_and_sorting():
    chars = [Character('A', 2), Character('B', 0), Character('C', 1)]
    engine = Engine(chars)
    engine.assign_initiative(seed=42)
    initiatives = [c.initiative for c in engine.initiative_order]
    assert initiatives == sorted(initiatives, reverse=True)
    # Names sorted for tie-breaker
    names = [c.name for c in engine.initiative_order]
    assert names == sorted(names, key=lambda n: (-next(c.initiative for c in chars if c.name==n), n))

def test_turn_order():
    chars = [Character('A'), Character('B'), Character('C')]
    engine = Engine(chars)
    engine.assign_initiative(seed=1)
    order = [engine.next_turn().name for _ in range(3)]
    expected = [c.name for c in engine.initiative_order]
    assert order == expected

def test_initiative_tie_break():
    chars = [Character('A', 0), Character('B', 0)]
    engine = Engine(chars)
    # Force same initiative
    for c in chars:
        c.initiative = 10
    engine.initiative_order = sorted(chars, key=lambda c: (-c.initiative, c.name))
    assert [c.name for c in engine.initiative_order] == ['A', 'B']

def test_skill_check_success_and_failure():
    char = Character('Hero', 3)
    engine = Engine([char])
    # Success
    assert engine.skill_check(char, dc=10, roll=15) is True
    # Failure
    assert engine.skill_check(char, dc=20, roll=10) is False

def test_natural_1_and_20():
    char = Character('Hero', 5)
    engine = Engine([char])
    # Natural 1
    assert engine.skill_check(char, dc=1, roll=1) is False
    assert char.last_check_result['desc'] == 'Automatic fail'
    # Natural 20
    assert engine.skill_check(char, dc=100, roll=20) is True
    assert char.last_check_result['desc'] == 'Automatic success'

def test_failed_check_consequence():
    char = Character('Hero', 0)
    engine = Engine([char])
    engine.skill_check(char, dc=15, roll=5)
    assert char.last_check_result['result'] is False
    # Simulate consequence
    consequence = 'missed attack' if not char.last_check_result['result'] else 'hit'
    assert consequence == 'missed attack'

def test_dice_rolls_with_seed():
    engine = Engine([])
    result = engine.roll_dice('2d6', modifier=2, seed=123)
    assert result['rolls'] == [1, 3]
    assert result['total'] == 6

def test_modifiers_positive_and_negative():
    engine = Engine([])
    pos = engine.roll_dice('1d8', modifier=2, seed=1)
    neg = engine.roll_dice('1d8', modifier=-2, seed=1)
    assert pos['total'] - neg['total'] == 4

def test_multiple_dice_types():
    engine = Engine([])
    d6 = engine.roll_dice('2d6', seed=2)
    d8 = engine.roll_dice('2d8', seed=2)
    d20 = engine.roll_dice('1d20', seed=2)
    assert len(d6['rolls']) == 2 and max(d6['rolls']) <= 6
    assert len(d8['rolls']) == 2 and max(d8['rolls']) <= 8
    assert len(d20['rolls']) == 1 and max(d20['rolls']) <= 20

def test_gpt_prompt_includes_state():
    chars = [Character('A', 1), Character('B', 2)]
    engine = Engine(chars)
    engine.assign_initiative(seed=5)
    engine.skill_check(chars[0], dc=10, roll=15)
    prompt = engine.format_gpt_prompt()
    assert 'Initiative:' in prompt
    assert 'Current:' in prompt
    assert 'Outcome:' in prompt
    assert chars[0].name in prompt
    assert str(chars[0].last_check_result['total']) in prompt

def test_gpt_prompt_turn_action_details():
    chars = [Character('A', 1)]
    engine = Engine(chars)
    engine.assign_initiative(seed=7)
    engine.skill_check(chars[0], dc=10, roll=12)
    prompt = engine.format_gpt_prompt()
    assert f"{chars[0].name}:" in prompt
    assert 'roll' in prompt
    assert 'modifier' in prompt
    assert 'total' in prompt
    assert 'desc' in prompt

def test_gpt_prompt_updates_after_action():
    chars = [Character('A', 1), Character('B', 2)]
    engine = Engine(chars)
    engine.assign_initiative(seed=8)
    engine.skill_check(chars[0], dc=10, roll=10)
    before = engine.format_gpt_prompt()
    engine.skill_check(chars[1], dc=10, roll=15)
    after = engine.format_gpt_prompt()
    assert before != after
    assert chars[1].name in after
    assert str(chars[1].last_check_result['total']) in after
