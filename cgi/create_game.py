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

class FormError(BaseException):
    def __init__(this, msg):
        this.msg = msg

def process_form():
    # see https://docs.python.org/3.4/library/cgi.html for the basic usage
    # here.
    form = cgi.FieldStorage()


    if "player1" not in form or "player2" not in form or "size" not in form:
        raise FormError("Invalid parameters.")

    player1 = form["player1"].value
    player2 = form["player2"].value
    for c in player1+player2:
        if c not in "_-" and not c.isdigit() and not c.isalpha():
            raise FormError("Invalid parameters: The player names can only contains upper and lowercase characters, digits, underscores, and hypens")
            return

    try:
        size = int(form["size"].value)
    except:
        raise FormError("Invalid parameters: 'size' is not an integer.")
        return


    raise FormError("I see that you are trying to create a new game.  This is not implemented yet.  player1='%s' player2='%s' size=%d" % (player1,player2,size))



# this is what actually runs, each time that we are called...

try:
#    print("Content-type: text/html")
#    print()

    # this will not print out *ANYTHING* !!!
    process_form()

    # https://en.wikipedia.org/wiki/Post/Redirect/Get
    # https://stackoverflow.com/questions/6122957/webpage-redirect-to-the-main-page-with-cgi-python
    print("Status: 303 See other")
    print("""Location: http://54.184.40.90/cgi-bin/list.py?new_game=1234""")
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


