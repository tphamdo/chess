from flask import Flask
from flask import render_template, make_response, request

from state import State
import chess
import random
import time

# creates a Flask application
app = Flask(__name__)

s = State()

def do_computer_move():
  if s.board.is_game_over():
    return

  # random computer move
  legal_moves = iter(s.board.legal_moves)
  n = s.board.legal_moves.count()
  ran = random.randint(1,n)
  while (ran != 0):
    move = next(legal_moves)
    ran -= 1
  s.board.push(move)

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
