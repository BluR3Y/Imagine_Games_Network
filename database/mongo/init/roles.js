// Create a role in the mongodb which will be primarily utilized by the application
db.createUser(
    {
        user: 'admin',
        pwd: 'AdminPassword@1234',
        roles: [
            {
                // Role will have read and write permissions on the ign database
                role: 'readWrite',
                db: 'imagine_games_network'
            }
        ]
    }
);