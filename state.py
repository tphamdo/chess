import chess

class State:

  def __init__(self):
    self.board = chess.Board()
    self.board.push_san("e4")

