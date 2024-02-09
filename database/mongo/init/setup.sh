#!/bin/bash
# Shebang is a special syntax that tells the os which interpreter to use when executing the script i.e., bash

# Command instructs shell to immediately exit script if any errors occur
set -e

# (<<) - In bash, it is known as a "here document"
# (-) - Including the hyphen before the label in a here doc allows the indentation of lines within the here doc, improving readability
# (MONGO_SCRIPT) - An arbitrary label chosen to mark the beginning and end of the here document.

echo "Creating mongo access user"

mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD -host localhost <<-MONGO_SCRIPT
    use $MONGO_INITDB_DATABASE
    db.createUser({
        user: "$MONGO_ACCESS_USERNAME",
        pwd: "$MONGO_ACCESS_PASSWORD",
        roles: [ { role: "readWrite", db: "$MONGO_INITDB_DATABASE" } ]
    })
MONGO_SCRIPT

echo "Finished creating mongo access user"