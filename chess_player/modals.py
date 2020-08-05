from dataclasses import dataclass
from typing import List, Any
from constants import Error
from mashumaro import DataClassJSONMixin


@dataclass
class GameState(DataClassJSONMixin):
    id: int
    reward: int
    player: str
    legal_moves: List[str]
    code: Any
    is_attack: bool = False
    is_check: bool = False
    is_check_mate: bool = False
    is_game_over: bool = False


@dataclass
class GameAction(DataClassJSONMixin):
    action: str
    player: str
