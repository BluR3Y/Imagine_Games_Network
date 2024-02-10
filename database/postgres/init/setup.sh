#!/bin/bash
# Shebang is a special syntax that tells the os which interpreter to use when executing the script i.e., bash

# Command instructs shell to immediately exit script if any errors occur
set -e

# End of SQL (EOSQL) - A delimiter used in a here document
# <<- Allows for indentation in a here document

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $POSTGRES_ACCESS_USER WITH PASSWORD '$POSTGRES_ACCESS_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_ACCESS_USER;
EOSQL