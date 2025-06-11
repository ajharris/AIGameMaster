# Universe logic for managing multiple RPG systems and merged rules
from typing import List, Dict, Optional

class Universe:
    def __init__(self, name: str, owner_id: str):
        self.name = name
        self.owner_id = owner_id
        self.systems: List[str] = []
        self.rules: Dict[str, str] = {}  # e.g., {'combat': '...', 'skills': '...'}
        self.user_overrides: Dict[str, str] = {}

    def add_system(self, system: str, rules: Dict[str, str]):
        if system in self.systems:
            raise ValueError(f"System '{system}' already added.")
        self.systems.append(system)
        self._merge_rules(rules)

    def _merge_rules(self, new_rules: Dict[str, str]):
        # Naive merge: if conflict, concatenate with separator
        for k, v in new_rules.items():
            if k in self.rules and self.rules[k] != v:
                self.rules[k] = self._resolve_conflict(k, self.rules[k], v)
            else:
                self.rules[k] = v

    def _resolve_conflict(self, key: str, rule1: str, rule2: str) -> str:
        # Simulate AI merge: prefer user override, else join
        if key in self.user_overrides:
            return self.user_overrides[key]
        return f"[Merged] {rule1} | {rule2}"

    def set_user_override(self, key: str, value: str):
        self.user_overrides[key] = value
        self.rules[key] = value

    def get_rule(self, key: str) -> Optional[str]:
        return self.rules.get(key)

    def has_system(self, system: str) -> bool:
        return system in self.systems

    def all_systems(self) -> List[str]:
        return list(self.systems)
