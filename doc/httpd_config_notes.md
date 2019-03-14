* Using httpd (Apache)
  * /var/www/cgi-bin/

* Worthwhile tools to install:
  * python3
  * git
  
  
  
Links:
  https://docs.python.org/3.4/howto/webservers.html



Debug Notes:
  - Trick: if you can't debug a 500, add the following two lines to the head of the file:
        Content-type: text/html
        <blank line>
    This will cause you to see the actual script output as RAW TEXT



Useful Design Info:
  https://en.wikipedia.org/wiki/Post/Redirect/Get

