from flask import Flask 
from flask import render_template, make_response

from state import State
  
# creates a Flask application 
app = Flask(__name__) 
  
s = State()
  
@app.route("/") 
def hello(): 
  res = make_response(render_template('index.html'))
  res.headers['fen'] = s.board.fen()
  return res
  
# run the application 
if __name__ == "__main__": 
    app.run(debug=True)
