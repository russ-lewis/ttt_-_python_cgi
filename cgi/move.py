#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import get_game_info,build_board



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


    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)


    if "user" not in form or "game" not in form:
        raise FormError("Invalid parameters.")
    if "pos" not in form and "resign" not in form:
        raise FormError("Invalid parameters.")

    game = int(form["game"].value)


    (players,size,state) = get_game_info(conn, game)

    user = form["user"].value
    if user not in players:
        raise FormError("Invalid player ID - player is not part of this game")


    if "resign" in form:
        resign = True
    else:
        resign = False
        pos = form["pos"].value.split(",")
        assert len(pos) == 2
        x = int(pos[0])
        y = int(pos[1])


    (board,nextPlayer,letter) = build_board(conn, game,size)

    if user != players[nextPlayer]:
        raise FormError("Internal error, incorrect player is attempting to move.")


    if resign:
        # this user is choosing to resign.  Update the game state to reflect that.
        other_player_name = players[1-nextPlayer]

        cursor = conn.cursor()
        cursor.execute("""UPDATE games SET state="%s:resignation" WHERE id=%d;""" % (other_player_name,game))
        cursor.close()

    else:
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
    print("""Location: http://%s/cgi-bin/game.py?user=%s&game=%s""" % (pnsdp.WEB_HOST, user,game))
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
    print("""Content-Type: text/html;charset=utf-8\n\n""")

    raise    # throw the error again, now that we've printed the lead text - and this will cause cgitb to report the error


