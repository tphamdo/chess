from flask import Flask
from flask import render_template, make_response, request

from state import State
from value import Value
import chess
import random
import time

# creates a Flask application
app = Flask(__name__)

s = State()
v = Value()

MAX_DEPTH = 4
ct = 0

# TODO: prune search. there's a massive slowdown even at MAX_DEPTH=4.

def minimax(b, d, alpha, beta, outer=False):
  global ct
  ct += 1

  if d >= MAX_DEPTH:
    return v(b)

  if outer:
    oret = []

  if b.turn == chess.WHITE:
    ret = Value.MIN
  else:
    ret = Value.MAX


  tmoves = []
  for move in b.legal_moves:
    b.push(move)
    tmoves.append((v(b), move))
    b.pop()
  tmoves = sorted(tmoves, key=lambda x: x[0], reverse=b.turn==chess.WHITE)
  moves = [x[1] for x in tmoves]

  # prune by only looking at top 5 moves -> beam search
  if d>= 2:
    moves = moves[:5]

  for move in moves:
    b.push(move)
    val = minimax(b, d+1, alpha, beta)
    b.pop()
    if outer:
      oret.append((val, move))

    if b.turn == chess.WHITE:
      ret = max(ret, val)
      if ret > beta:
        return ret
      alpha = max(alpha, ret)
    else:
      ret = min(ret, val)
      if ret < alpha:
        return ret
      beta = min(beta, ret)

  if outer:
    return ret, oret
  else:
    return ret

def do_computer_move():
  if s.board.is_game_over():
    return

  global ct
  ct = 0

  val, moves = minimax(s.board, 0, Value.MIN, Value.MAX, outer=True)
  moves = sorted(moves, key=lambda x: x[0])
  print(f'looked at {ct} nodes')
  print(moves)
  s.board.push(moves[0][1])
  print(f'doing computer move {moves[0][1]}')
  print(f'found {v.cache_hit} cache hits in value.py')


  # random computer move
#  legal_moves = iter(s.board.legal_moves)
#  n = s.board.legal_moves.count()
#  ran = random.randint(1,n)
#  while (ran != 0):
#    move = next(legal_moves)
#    ran -= 1
#  s.board.push(move)

@app.route("/")
def start():
  res = make_response(render_template('index.html'))
  res.headers['fen'] = s.board.fen()
  res.headers['gameover'] = s.board.is_game_over()
  return res

@app.route("/move")
def move():
  src = chess.parse_square(request.args.get('source'))
  to = chess.parse_square(request.args.get('target'))
  promotion = None
  if request.args.get('piece') == "wP" and '8' in chess.square_name(to):
    promotion = chess.QUEEN

  move = chess.Move(src, to, promotion)
  if (move in s.board.legal_moves):
    print(f'doing human move: {move}')
    s.board.push(move)
    do_computer_move()
  else:
    print("invalid move")

  res = make_response(s.board.fen(), 200)
  res.headers['gameover'] = s.board.is_game_over()

  return res

@app.route("/restart")
def restart():
  s.board.reset()

  return s.board.fen(), 200

# run the application
if __name__ == "__main__":
  app.run(debug=True)
