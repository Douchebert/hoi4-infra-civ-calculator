from dataclasses import dataclass, field
from typing import List, Dict, Optional
import copy


@dataclass
class GameState:
    current_civs: int
    current_mils: int
    consumer_goods_percent: float = 0
    global_construction_bonus: float = 0.0
    states: List[Dict] = field(default_factory=list)
    current_day: int = 0

    def get_available_construction_factories(self) -> int:
        total = self.current_civs + self.current_mils
        cg_factor = 1 - (self.consumer_goods_percent / 100)
        return max(0, int(total * cg_factor))

    def get_state_by_name(self, name: str) -> Optional[Dict]:
        for s in self.states:
            if s.get("name") == name:
                return s
        return None

    def copy(self):
        return copy.deepcopy(self)


def get_infra_multiplier(infra_level: int) -> float:
    """+20% construction speed per infrastructure level"""
    return 1.0 + (infra_level * 0.2)


def build_infrastructure(state: GameState, target_name: str) -> GameState:
    new = state.copy()
    target = new.get_state_by_name(target_name)
    if target and target.get("infra", 0) < 5:
        target["infra"] += 1
    return new


def build_civilian_factory(state: GameState, target_name: str) -> GameState:
    new = state.copy()
    target = new.get_state_by_name(target_name)
    if target:
        open_slots = target.get("max_slots", 0) - target.get("used_slots", 0)
        if open_slots > 0:
            target["used_slots"] += 1
            new.current_civs += 1
    return new


def advance_time(state: GameState, days: int) -> GameState:
    new = state.copy()
    new.current_day += days
    return new