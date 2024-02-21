from flask import Flask
from flask import render_template, make_response, request

from state import State
import chess

# creates a Flask application
app = Flask(__name__)

s = State()

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
  promotion = chess.QUEEN if request.args.get('promotion') else None

  move = chess.Move(src, to, promotion)
  if (move in s.board.legal_moves):
    print("doing move: ", move)
    s.board.push(move)
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
