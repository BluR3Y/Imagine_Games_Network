#!/bin/bash
# Shebang is a special syntax that tells the os which interpreter to use when executing the script i.e., bash

# Command instructs shell to immediately exit script if any errors occur
set -e

# End of SQL (EOSQL) - A delimiter used in a here document
# <<- Allows for indentation in a here document

# Configure the access key
awslocal configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}

# Configure the secret access key
awslocal configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}

# Create a new user using the CreateUser API
awslocal iam create-user --user-name terraform_user

# Create an access key pair for the user using the CreateAccessKey API
awslocal iam create-access-key --user-name terraform_user