import asyncio
import chess

from constants import Error, Status
from modals import GameState, GameAction


class GameEnvironment:
    """
    decide available moves with environment rules
    """
    __dependents__ = ["RandomPlayerAgent"]

    def __init__(self, config):
        self.board = chess.Board()
        self.move_count = 0
        self.move_log = [(self.move_count, None, self.board.fen())]  # index,move,board
        self.move = None
        self.pre_move = None

    def get_next_player(self):
        return "WHITE" if self.board.turn else "BLACK"

    def get_legal_moves(self):
        return [f"{m}" for m in self.board.legal_moves]

    async def accept_message(self, agent, message):
        player_action = GameAction.from_dict(message["data"])
        print(player_action)
        next_move = chess.Move.from_uci(player_action.action)
        if next_move in self.board.legal_moves:
            self.pre_move = self.move
            self.move = next_move
        else:
            await self.send_message(data=GameState(reward=-1, player=self.get_next_player(),
                                                   code=Error.INVALID_MOVE,
                                                   legal_moves=self.get_legal_moves()).to_dict())

    async def run_agent(self, request):
        while True:
            if self.move != self.pre_move:
                self.move_count += 1
                self.board.push(self.move)
                await self.send_message(data=GameState(reward=-1, player=self.get_next_player(),
                                                       legal_moves=self.get_legal_moves(), code=Status.ACT).to_dict())
            else:
                if self.move_count == 0:
                    await self.send_message(
                        data=
                        GameState(code=Error.NOT_STARTED, player=self.get_next_player(),
                                  legal_moves=self.get_legal_moves(),
                                  reward=-1).to_dict())

            await asyncio.sleep(0.01)
