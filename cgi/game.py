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

from common import get_game_info,build_board,FormError



# this function handles the processing of the actual text of the HTML file.
# It writes everything from the HTML header, to the content in the body, to
# the closing tags at the bottom.
#
# Later, I ought to make this smarter, to handle cookies and such.  Or, just
# switch over to some framework which makes it all easier for me!

def write_html():
    # see https://docs.python.org/3.4/library/cgi.html for the basic usage
    # here.
    form = cgi.FieldStorage()


    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)


    if "game" not in form or "user" not in form:
        report_error("Invalid parameters.")
        return


    game = int(form["game"].value)

    (players,size,state) = get_game_info(conn, game)

    user = form["user"].value
    if user not in players:
        report_error("Sorry, the player '%s' is not part of this game." % user)
        return

    curUser = players.index(user)

    (board, nextToPlay,letter) = build_board(conn, game,size)

    # TODO: read this from the DB, later
    last = "1 Jan 1970"

    print("""<html>
<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>

<font size="+1"><b>Game %d:</b> %s (X) vs. %s (O)</font>

<p><b>Size:</b> %dx%x

<p><b>State:</b> %s

<p><b>Next to Play:</b> %s
<br><b>You Are:</b> %s

""" % (game, players[0],players[1], size,size, state, players[nextToPlay], players[curUser]), end="")


    print("""<p>
<form action="move.py" method="get">
  <input type=hidden name="user" value="%s">
  <input type=hidden name="game" value="%s">

<table border=2>
""" % (players[nextToPlay],game), end="")

    for y in range(size):
        print("  <tr height=50 valign=center>")

        for x in range(size):
            if board[x][y] != "":
                content = board[x][y]
            elif curUser != nextToPlay or state != "Active":
                content = ""
            else:
                content = """<button type=submit name="pos" value="%d,%d" style="height:100%%;width:100%%"></button>""" % (x,y)

            print("    <td width=50 align=center>"+content+"</td>")

        print("  </tr>")

    print("""</table>

""", end="")

    if curUser == nextToPlay and state == "Active":
        print("""<input type=submit value="Resign" name="resign">\n\n""")

    print("</form>\n\n")

    if state == "Active":
        print("<p>Last activity: %s\n\n" % last, end="")


    print("""<p>HTML Variables:
  <pre>
""", end="")
    for k in form:
        print("    %s=%s" % (k, repr(form.getlist(k)[0])))
    print("""  </pre>

</body>
</html>

""", end="")

    conn.close()



def report_error(msg):
    print("""<html>
<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>

<p>ERROR: %s

<p><a href="list.py">Return to game list</a>

</body>
</html>

""" % msg, end="")



# this is what actually runs, each time that we are called...
try:
    print("Content-type: text/html")
    print()

    # this will print out lots and lots of stuff - the entire response,
    # typically (except for the header).  However, sometimes, we will
    # hit an exception, which will throw us into one of the handlers
    # below.
    write_html()

except FormError as e:
    print("""<html>

<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>

<p>ERROR: %s

<p><a href="list.py">Return to game list</a>

</body>
</html>

""" % e.msg, end="")

# except(other) ...
#   other errors will be caught by the cgitb module, and pretty-printed

