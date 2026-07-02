import copy
from core.game_state import GameState
CIVILIAN_FACTORY_COST = 10800
INFRASTRUCTURE_COST = 3000
CIVILIAN_FACTORY_OUTPUT = 5

#output = civi factory - ((civ factory + mil factory)*consumer goods percent)
#construction speed = output * (1 + infra level * 0.2) * (1 + global construction bonus + state construction bonus)


class GameEngine:
    def __init__(self, game_state: GameState, construction_queue=None):
        self.game_state = game_state
        self.construction_queue = {}  # Infras and Civs to build, keyed by state name
        self.game_event_queue = []  # List of events to process from manual input or focus tree
    def copy(self):
        return copy.deepcopy(self)
    def prepare_for_simulation(self):
        # Prepare the game state for simulation, e.g., calculate effective construction speed
        pass
    

