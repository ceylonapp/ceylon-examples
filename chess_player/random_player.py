from game_env import GameEnvironment
from modals import GameState, GameAction
import random


class RandomPlayerAgent:
    __dependents__ = ["GameEnvironment"]

    def __init__(self, config=None):
        self.type = f"{config['type']}".upper()
        self.move = None
        self.total_reward = 0
        self.move_log = []  # move,reward

    async def accept_message(self, agent, message):
        if agent == GameEnvironment.__name__:
            game_state = GameState.from_dict(message["data"])

            if game_state.player == self.type:
                print(game_state)
                next_move = game_state.legal_moves[random.randint(0, len(game_state.legal_moves) - 1)]
                await self.send_message(data=GameAction(action=next_move, player=self.type).to_dict())

    async def run_agent(self, request):
        print(request)
