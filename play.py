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

MAX_DEPTH = 3

# TODO: prune search. there's a massive slowdown even at MAX_DEPTH=4.
def minimax(b, d, outer=False):
  if d >= MAX_DEPTH:
    return v.value(b)

  if outer:
    oret = []

  if b.turn == chess.WHITE:
    ret = Value.MIN
  else:
    ret = Value.MAX

  for move in b.legal_moves:
    b.push(move)
    val = minimax(b, d+1)
    b.pop()
    if outer:
      oret.append((val, move))

    if b.turn == chess.WHITE:
      ret = max(ret, val)
    else:
      ret = min(ret, val)

  if outer:
    return ret, oret
  else:
    return ret

def do_computer_move():
  if s.board.is_game_over():
    return

  val, moves = minimax(s.board, 0, outer=True)
  moves = sorted(moves, key=lambda x: x[0])
  print(val)
  print(moves)
  s.board.push(moves[0][1])


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
    print("doing move: ", move)
    s.board.push(move)
    print(v.value(s.board))
    do_computer_move()
    print(v.value(s.board))
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
