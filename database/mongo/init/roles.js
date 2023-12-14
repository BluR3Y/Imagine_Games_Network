// Create a role in the mongodb which will be associated with the ign application
db.createUser(
    {
        user: 'ignUser',
        pwd: 'Password@1234',
        roles: [
            {
                // Role will have read and write permissions on the ign database
                role: 'readWrite',
                db: 'ign'
            }
        ]
    }
);