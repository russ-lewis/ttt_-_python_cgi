#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable()

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp



# this function handles the processing of the actual text of the HTML file.
# It writes everything from the HTML header, to the content in the body, to
# the closing tags at the bottom.
#
# Later, I ought to make this smarter, to handle cookies and such.  Or, just
# switch over to some framework which makes it all easier for me!

class FormError(BaseException):
    def __init__(this, msg):
        this.msg = msg

def process_form():
    # see https://docs.python.org/3.4/library/cgi.html for the basic usage
    # here.
    form = cgi.FieldStorage()


#    if "user" not in form:
#        raise FormError("Invalid parameters.")
#
#    player1 = form["player1"].value
#    player2 = form["player2"].value
#    for c in player1+player2:
#        if c not in "_-" and not c.isdigit() and not c.isalpha():
#            raise FormError("Invalid parameters: The player names can only contains upper and lowercase characters, digits, underscores, and hypens")
#            return
#
#    try:
#        size = int(form["size"].value)
#    except:
#        raise FormError("Invalid parameters: 'size' is not an integer.")
#        return
    user = "Eric"
    game = 1025
    pos  = "0,1"


    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)


    # get the basic game properties
    cursor = conn.cursor()
    cursor.execute("SELECT player1,player2,size FROM games WHERE id = %d;" % game)
    if cursor.rowcount != 1:
        raise FormError("Invalid game ID")

    row = cursor.fetchall()[0]
    players = [row[0],row[1]]
    size    =  row[2]

    cursor.close()


    if user not in players:
        raise FormError("Invalid player ID - player is not part of this game")


    # we'll build the empty board, and then fill in with the move list that
    # we get from the DB.
    board = []
    for i in range(size):
        board.append([""]*size)


    # search for all moves that have happenend during this game.
    cursor = conn.cursor()
    cursor.execute("SELECT x,y,letter FROM moves WHERE gameID = %d;" % game)

    counts = {"X":0, "O":0}
    for move in cursor.fetchall():
        (x,y,letter) = move

        x = int(x)
        y = int(y)
        assert x >= 0 and x < size
        assert y >= 0 and y < size

        assert letter in "XO"

        assert board[x][y] == ""
        board[x][y] = letter

        counts[letter] += 1

    cursor.close()

    assert counts["X"] >= counts["O"]
    assert counts["X"] <= counts["O"]+1

    if counts["X"] == counts["O"]:
        next = 0
    else:
        next = 1
    letter = "XO"[next]


    if user != players[next]:
        raise FormError("Internal error, incorrect player is attempting to move.")


    pos = pos.split(",")
    assert len(pos) == 2
    x = int(pos[0])
    y = int(pos[1])

    assert x >= 0 and x < size
    assert y >= 0 and y < size

    assert board[x][y] == ""


    # we've done all of our sanity checks.  We now know enough to say that
    # it's safe to add a new move.
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO moves(gameID,x,y,letter,time) VALUES(%d,%d,%d,"%s",NOW());""" % (game,x,y,letter))

    if cursor.rowcount != 1:
        raise FormError("Could not make move, reason unknown.")

    cursor.close()

    # we've made changes, make sure to commit them!
    conn.commit()
    conn.close()


    # return the parms to the caller, so that they can build a good redirect
    return (user,game)



# this is what actually runs, each time that we are called...

try:
#    print("Content-type: text/html")
#    print()

    # this will not print out *ANYTHING* !!!
    (user,game) = process_form()

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    print("""Location: http://54.184.40.90/cgi-bin/game.py?user=%s&game=%s""" % (user,game))
    print()

except FormError as e:
    print("""Content-Type: text/html;charset=utf-8

<html>

<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>

<p>ERROR: %s

<p><a href="list.py">Return to game list</a>

</body>
</html>

""" % e.msg, end="")

except:
    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error


