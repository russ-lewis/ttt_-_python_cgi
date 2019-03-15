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


    gameNum = 1234
    players = ["Russ","Eric"]
    size = 3
    state = "Active"
    nextToPlay = 0
    curUser = 0

    board = [["","",""],
             ["","",""],
             ["","",""]]

    last = "1 Jan 1970"

    if "new_game" in form:
        new_game = int(form["new_game"].value)
    else:
        new_game = None


    print("""<html>
<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>


""", end="")


    # connect to the database
    conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                           user   = pnsdp.SQL_USER,
                           passwd = pnsdp.SQL_PASSWD,
                           db     = pnsdp.SQL_DB)


    # search for all games that are not yet completed.  We have not yet
    # implemented the "idle" games feature, so we'll only have the two
    # classifications
    cursor = conn.cursor()
    cursor.execute("SELECT id,player1,player2,size FROM games WHERE state IS NULL;")

    active = []
    for row in cursor.fetchall():
        active.append({"key":row[0], "player0_name":row[1], "player1_name":row[2], "size":int(row[3])})

    cursor.close();


    # now, search for the games that *HAVE* been completed.
    cursor = conn.cursor()
    cursor.execute("SELECT id,player1,player2,size,state FROM games WHERE state IS NOT NULL;")

    finished = []
    for row in cursor.fetchall():
        key   =     row[0]
        p0    =     row[1]
        p1    =     row[2]
        size  = int(row[3])
        state =     row[4].split(':')

        assert len(state) == 2

        winner = state[0]
        reason = state[1]

        players = [p0,p1]
        assert winner in players
        winner = players.index(winner)

        finished.append({"key":key, "player0_name":p0, "player1_name":p1, "size":size, "winner":[winner,reason]})

    cursor.close();
    conn.close();


    idle = ""
    # idle     = [{"key":5678, "player0_name":"Russ", "player1_name":"Eric", "size":3, "last_activity":"A long time ago..."}]

    write_table("Active",   active, new_game=new_game)
    write_create_game_form()
    print("<hr>\n\n")
    write_table("Idle",     idle,     idle=True)
    write_table("Finished", finished, finished=True)

    print("""</body>
</html>

""", end="")



def write_table(desc, games, new_game=None, idle=False, finished=False):
    if idle:
        idleStr = "<td><b>Idle Since</b></td> "
    else:
        idleStr = ""

    if finished:
        finishedStr = "<td colspan=2><b>Winner</b></td> "
    else:
        finishedStr = "<td><b>Play as...</b></td>"

    print("""<p>
<font size="+1"><b>%s Games</b></font>
  <br><table border=1>
        <tr> <td><b>ID</b></td> <td><b>Players</b></td> <td><b>Size</b></td> %s%s</tr>
""" % (desc, idleStr,finishedStr), end="")

    for g in games:
        key     =  g["key"]
        players = [g["player0_name"], g["player1_name"]]
        size    =  g["size"]

        if new_game is not None and key == new_game:
            mark1 = "<font color=red><b>"
            mark2 = "</b></font>"
        else:
            mark1 = ""
            mark2 = ""


        if idle:
            idleStr = "          <td>%s</td>\n" % g["last_activity"]

        if not finished:
            finishedStr = """          <td> %s<a href="game.py?user=%s&game=%d">%s</a> <a href="game.py?user=%s&game=%d">%s</a>%s </td>
""" % (mark1, players[0],key,players[0], players[1],key,players[1], mark2)
        else:
            winner = g["winner"]
            finishedStr = "          <td>%s</td> <td>(%s)</td>\n" % (players[winner[0]],winner[1])


        print("""
        <tr>
          <td>%s%d%s</td> <td>%s%s, %s%s</td> <td>%s%dx%d%s</td>
%s%s        </tr>
""" % (mark1,key,mark2, mark1,players[0],players[1],mark2, mark1,size,size,mark2, idleStr,finishedStr), end="")

    print("""      </table>


""", end="")



def write_create_game_form():
    print("""<p><b>Create a New Game</b>

<form action="create_game.py" method="post">
  Player 1: <input type="text" size=10 name="player1">
  Player 2: <input type="text" size=10 name="player2">
  Size:     <input type="text" size=1  name="size">
  <input type=submit value="Create">
</form>

""", end="")



# this is what actually runs, each time that we are called...

#print("Content-Type: text/plain;")
#print()

print("Content-Type: text/html;charset=utf-8")
print()

write_html()

