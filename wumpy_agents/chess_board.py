import chess
import chess.svg

from player_coordinator import PlayerCoordinatorAgent


class ChessBoardAgent:
    __dependents__ = [PlayerCoordinatorAgent]

    def __init__(self, config=None):
        self.board = chess.Board()
        self.command = ""
        print(self.board)

    async def accept_message(self, agent, message):
        pass

    async def run_agent(self, request):
        response = {}
        move_str = request["move"]
        try:
            move = chess.Move.from_uci(move_str)
            is_legal_move = move in self.board.legal_moves
        except Exception as e:
            return {
                "error": f"{e}"
            }

        if not is_legal_move:
            response = {
                **response,
                "result": "move is not legal",
            }
        else:
            self.board.push(move)
            response = {
                **response,
                "result": "SUCCESS",
            }

        response = {
            **response,
            "board": f"{chess.svg.board(board=self.board, size=500)}"
        }

        return response
