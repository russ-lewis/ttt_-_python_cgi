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

<font size="+1"><b>Game %d:</b> %s (X) vs. %s (O)</font>

<p><b>Size:</b> %dx%x

<p><b>State:</b> %s

<p><b>Next to Play:</b> %s
<br><b>You Are:</b> %s

""" % (gameNum, players[0],players[1], size,size, state, players[nextToPlay], players[curUser]), end="")


    print("""<p>                                                                             
<form action="play.py" method="get">                                            
                                                                                
<table border=2>                                                                
""", end="")

    for x in range(size):
        print("  <tr height=50 valign=center>")

        for y in range(size):
            if board[x][y] == "":
                content = """<input type=submit value="" name="%d,%d">""" % (x,y)
            else:
                content = board[x][y]

            print("    <td width=50 align=center>"+content+"</td>")

        print("  </tr>")

    print("""</table>                                                                        
                                                                                
<input type=submit value="Resign" name="resign">                                
                                                                                
</form>

""", end="")

    print("""<p>Last activity: %s

""" % last, end="")


    print("""<p>HTML Variables:
  <pre>
""", end="")
    for k in form:
        print("    %s=%s" % (k, repr(form.getlist(k)[0])))
    print("""  </pre>

</body>
</html>

""", end="")



# this is what actually runs, each time that we are called...

print("Content-Type: text/html;charset=utf-8")
print()

write_html()

