#!/bin/bash
# Shebang is a special syntax that tells the os which interpreter to use when executing the script i.e., bash

# Command instructs shell to immediately exit script if any errors occur
set -e

# (<<) - In bash, it is known as a "here document"
# (-) - Including the hyphen before the label in a here doc allows the indentation of lines within the here doc, improving readability
# (MYSQL_SCRIPT) - An arbitrary label chosen to mark the beginning and end of the here document.

mysql -u root -p$MYSQL_ROOT_PASSWORD -h localhost -P 3306 <<-MYSQL_SCRIPT
    ALTER USER '$MYSQL_USER' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PASSWORD';
    FLUSH PRIVILEGES;
MYSQL_SCRIPT