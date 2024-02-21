import chess

# basic chess evaluation class
# TODO: replace this with neural net
class Value:
  values = {chess.PAWN:1,
            chess.KNIGHT:3,
            chess.BISHOP:3,
            chess.ROOK:5,
            chess.QUEEN:9,
            chess.KING:0}
  MAX = 9999999
  MIN = -MAX
  DRAW = 0

  def __init__(self):
    self.count = 0

  def __call__(self, b):
    self.count += 1
    return self.value(b)

  def value(self, b):
    assert isinstance(b, chess.Board)

    if b.is_game_over():
      if b.result() == "1-0":
        return self.MAX
      elif b.result() == "0-1":
        return self.MIN
      else:
        return self.DRAW

    tot_val = 0.0
    if b.turn == chess.WHITE:
      tot_val += 0.05 * b.legal_moves.count()
    else:
      tot_val -= 0.05 * b.legal_moves.count()

    for sq in chess.SQUARES:
      piece = b.piece_type_at(sq)
      if piece:
        if b.color_at(sq) == chess.WHITE:
          tot_val += self.values[piece]
        else:
          tot_val -= self.values[piece]


    return tot_val

