#! /usr/bin/env python3

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable()



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

    print("""<html>
<head><title>346 - Russ Lewis - Tic-Tac-Toe</title></head>

<body>


""", end="")

    active   = [{"key":1234, "player0_name":"Russ", "player1_name":"Eric", "size":3}]
    idle     = [{"key":5678, "player0_name":"Russ", "player1_name":"Eric", "size":3, "last_activity":"A long time ago..."}]
    finished = [{"key":42,   "player0_name":"Russ", "player1_name":"Eric", "size":3, "winner":[1,"complete"]},
                {"key":-1,   "player0_name":"Russ", "player1_name":"Eric", "size":3, "winner":[0,"timeout"]},
                {"key":1024, "player0_name":"Russ", "player1_name":"Eric", "size":3, "winner":[1,"resignation"]}]

    write_table("Active",   active)
    write_create_game_form()
    print("<hr>\n\n")
    write_table("Idle",     idle,     idle=True)
    write_table("Finished", finished, finished=True)

    print("""</body>
</html>

""", end="")



def write_table(desc, games, idle=False, finished=False):
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

        if idle:
            idleStr = "          <td>%s</td>\n" % g["last_activity"]

        if not finished:
            finishedStr = """          <td> <a href="game.py?user=%s&game=%d">%s</a> <a href="game.py?user=%s&game=%d">%s</a> </td>
""" % (players[0],key,players[0], players[1],key,players[1])
        else:
            winner = g["winner"]
            finishedStr = "          <td>%s</td> <td>(%s)</td>\n" % (players[winner[0]],winner[1])


        print("""
        <tr>
          <td>%d</td> <td>%s, %s</td> <td>%dx%d</td>
%s%s        </tr>
""" % (key, players[0],players[1], size,size, idleStr,finishedStr), end="")

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

print("Content-Type: text/html;charset=utf-8")
print()

write_html()

