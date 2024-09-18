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


# Check for winner
def check_winner(board, turn):
    is_winner = False
    current = turn
    # x_picks = []
    # y_picks = []
    #
    # if current == "X":
    #     x_picks.append([row, col])
    # else:
    #     y_picks.append([row, col])
    #
    # print(f"x_picks: {x_picks}")
    # print(f"y_picks: {y_picks}")

    # for i in board:
    #     print(f"This is i: {i}")
    #     if i.count(current) == 3:
    #         is_winner = True
    #         return is_winner
    #     elif i[0] == current:
    #         print(f"i[0] loop: {i[0]}")
    #
    #     for j in i:
    #         print(f"This is j: {j}")



# Use route to play when link is clicked
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    moves_remaining = 9
    still_playing = True
    while still_playing:
        # Update board
        session["board"][row][col] = session["turn"]

        # End if board full
        if moves_remaining < 1:
            still_playing = False

        # Check for winner
        if check_winner(session["board"], session["turn"]):
            print(f"WINNER IS: {session['turn']}")
            still_playing = False

        else:
            # Update turn
            if session["turn"] == "X":
                session["turn"] = "O"
            else:
                session["turn"] = "X"
            moves_remaining -= 1
            print(session["board"])

        # Redirect to index game board
        return redirect(url_for("index"))

    # Redirect to index game board
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)