import random
from typing import List, Optional, Dict

class Character:
    def __init__(self, name: str, modifier: int = 0):
        self.name = name
        self.modifier = modifier
        self.initiative: Optional[int] = None
        self.last_check_result: Optional[Dict] = None

class Engine:
    def __init__(self, characters: List[Character]):
        self.characters = characters
        self.initiative_order: List[Character] = []
        self.turn_index = 0
        self.state_log = []

    def assign_initiative(self, seed: Optional[int] = None):
        rng = random.Random(seed)
        for c in self.characters:
            c.initiative = rng.randint(1, 20) + c.modifier
        self.initiative_order = sorted(self.characters, key=lambda c: (-c.initiative, c.name))

    def next_turn(self) -> Character:
        char = self.initiative_order[self.turn_index % len(self.initiative_order)]
        self.turn_index += 1
        return char

    def skill_check(self, char: Character, dc: int, roll: Optional[int] = None) -> bool:
        if roll is None:
            roll = random.randint(1, 20)
        total = roll + char.modifier
        if roll == 1:
            result = False
            desc = 'Automatic fail'
        elif roll == 20:
            result = True
            desc = 'Automatic success'
        else:
            result = total >= dc
            desc = 'Success' if result else 'Failure'
        char.last_check_result = {'roll': roll, 'modifier': char.modifier, 'total': total, 'result': result, 'desc': desc}
        return result

    def roll_dice(self, dice: str, modifier: int = 0, seed: Optional[int] = None) -> Dict:
        rng = random.Random(seed)
        num, die = map(int, dice.lower().split('d'))
        rolls = [rng.randint(1, die) for _ in range(num)]
        return {'rolls': rolls, 'total': sum(rolls) + modifier}

    def format_gpt_prompt(self) -> str:
        order = ', '.join(f'{c.name}({c.initiative})' for c in self.initiative_order)
        current = self.initiative_order[self.turn_index % len(self.initiative_order)]
        last = getattr(current, 'last_check_result', None)
        outcome = f"{current.name}: {last}" if last else "No action yet"
        return f"Initiative: {order}\nCurrent: {current.name}\nOutcome: {outcome}"
