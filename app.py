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
def index(winner=None):

    # First, if no board in session, create a new board
    if "board" not in session:
        # Create blank board
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        # Also store whose turn it is in session, X starts
        session["turn"] = "X"

    # Inside template, need to have access to board, and whose turn it is
    return render_template("game.html", game=session["board"], turn=session["turn"], winner=winner)


# Check for winner
def check_winner(row, col, board, turn):
    is_winner = False
    current = turn
    check = []
    middle = board[1][1]
    check2 = []

    for i in board:
        # print(f"This is i: {i}")
        if i.count(current) == 3:
            is_winner = True
            return is_winner
        if i[col] == current:
            check.append(i[col])

        # print(f"check: {check}")
        if check.count(current) == 3:
            is_winner = True
            return is_winner

    if middle and middle == current:
        check2.append(middle)
        if board[0][0] == current:
            check2.append(current)
            if board[2][2] == current:
                check2.append(current)
        elif board[0][2] == current:
            check2.append(current)
            if board[2][0] == current:
                check2.append(current)


    # print(f"check2: {check2}")
    if check2.count(current) == 3:
        is_winner = True
        return is_winner



# Use route to play when link is clicked
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    moves_remaining = 9
    still_playing = True
    while still_playing:
        winner = None
        # Update board
        session["board"][row][col] = session["turn"]

        # End if board full
        if moves_remaining < 1:
            still_playing = False

        # Check for winner
        if check_winner(row, col, session["board"], session["turn"]):
            print(f"WINNER IS: {session['turn']}")
            still_playing = False
            winner = session["turn"]

            # Redirect to index game board
            return redirect(url_for("index", winner=winner))

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