from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# Use session so each player can have a different board
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    # First, if no board in session, create a new board
    if "board" not in session:
        # Create blank board
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        # Also store whose turn it is in session, X starts
        session["turn"] = "X"

    # Inside template, need to have access to board, and whose turn it is
    return render_template("game.html", game=session["board"], turn=session["turn"])


# Use route to play when link is clicked
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    # Update board
    session["board"][row][col] = session["turn"]
    # Update turn
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    # Redirect to index game board
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)