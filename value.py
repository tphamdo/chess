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
    self.memo = {}
    self.cache_hit = 0

  def __call__(self, b):
    key = b.fen()
    if key not in self.memo:
      self.memo[key] = self.value(b)
    else:
      self.cache_hit += 1
    
    return self.memo[key]

  def value(self, b):
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

    for p in b.piece_map().values():
      val = self.values[p.piece_type]
      if p.color == chess.WHITE:
        tot_val += val
      else:
        tot_val -= val

    return tot_val

