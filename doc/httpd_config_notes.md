* Using httpd (Apache)
  * /var/www/cgi-bin/

* Previously, on Project 1...
    sudo yum install httpd

* Install mysql on your EC2 instance
    sudo yum install python3
    sudo yum install mariadb              # mysql command line
    sudo yum install mariadb-devel        # mysql_config command, needed by pip
    sudo yum install gcc                  # also needed for pip install
    pip3 install mysqlclient              # makes the MySQLdb package work inside your python3 program
    sudo yum install python3-devel

* Other useful tools
    sudo yum install git

* Setting up error logging
    sudo bash
    cd /var/log/httpd
    chmod a+x .
    mkdir cgi_err
    chown apache:apache cgi_err



Links:
  https://docs.python.org/3.4/howto/webservers.html
  https://aws.amazon.com/getting-started/tutorials/create-mysql-db/
      - public DB not required if you configure with command line
      - but have to add rule to security group, to allow DB connections from the SG
  https://pythonspot.com/mysql-with-python/



Useful SQL, MySQL Statements:
  USE <dbName>

  SELECT ...

  SHOW TABLES;

  CREATE TABLE name (fieldName TYPE [NOT NULL] [AUTO_INCREMENT], ... , PRIMARY KEY(fieldName), FOREIGN KEY(localFieldname) REFERENCES remoteTable(remoteField));

  SHOW COLUMNS FROM table;

  ALTER TABLE ...
    https://dev.mysql.com/doc/refman/8.0/en/alter-table.html

    ALTER TABLE tablename MODIFY COLUMN fieldName <new type and constraints>;

  SHOW CREATE TABLE tablename;
    # shows the CREATE TABLE command needed to duplicate the design



Debug Notes:
  - Trick: if you can't debug a 500, add the following two lines to the head of the file:
        Content-type: text/html
        <blank line>
    This will cause you to see the actual script output as RAW TEXT



Useful Design Info:
  https://en.wikipedia.org/wiki/Post/Redirect/Get

