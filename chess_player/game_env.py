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
        self.actor = self.get_next_player()

    def get_next_player(self, turn=None):
        turn = self.board.turn if turn is None else turn
        return "WHITE" if turn else "BLACK"

    def get_legal_moves(self):
        return [f"{m}" for m in self.board.legal_moves]

    async def accept_message(self, agent, message):
        player_action = GameAction.from_dict(message["data"])
        print("move", player_action, self.pre_move, self.actor)
        next_move = chess.Move.from_uci(player_action.action)
        if next_move in self.board.legal_moves:
            self.move = next_move
        else:
            print("Move illegal", self.board.legal_moves, player_action.action)
            await self.send_message(data=GameState(id=self.move_count, reward=-1, player=self.actor,
                                                   code=Error.INVALID_MOVE,
                                                   legal_moves=self.get_legal_moves()).to_dict())

    async def run_agent(self, request):
        while True:
            if self.move != self.pre_move:
                self.move_count += 1
                self.board.push(self.move)
                self.print_status()
                self.actor = self.get_next_player()

                await self.send_message(data=GameState(id=self.move_count, reward=-1, player=self.actor,
                                                       is_check=self.board.is_check(),
                                                       is_check_mate=self.board.is_checkmate(),
                                                       is_game_over=self.board.is_game_over(),
                                                       legal_moves=self.get_legal_moves(), code=Status.ACT).to_dict())
                self.pre_move = self.move

                if self.board.is_variant_draw() \
                        or self.board.is_insufficient_material() \
                        or self.board.can_claim_threefold_repetition() \
                        or self.board.is_game_over():
                    break


            else:
                if self.move_count == 0:
                    await self.send_message(
                        data=
                        GameState(id=self.move_count, code=Error.NOT_STARTED, player=self.actor,
                                  legal_moves=self.get_legal_moves(),
                                  reward=-1).to_dict())

            await asyncio.sleep(0.01)

    def print_status(self):
        if self.board.is_game_over():
            print(f"Count {self.move_count} Is Game Over {self.board.is_game_over()}")
        if self.board.is_variant_draw():
            print(f"Count {self.move_count} Is Draw {self.board.is_variant_draw()}")
        if self.board.is_insufficient_material():
            print(f"Count {self.move_count} Is Matrial Not enough {self.board.is_insufficient_material()}")
        if self.board.can_claim_threefold_repetition():
            print(f"Count {self.move_count} Is Threefold repetition {self.board.can_claim_threefold_repetition()}")
        if self.board.is_checkmate():
            print(f"Count {self.move_count} Is checkmate {self.board.is_checkmate()}")
