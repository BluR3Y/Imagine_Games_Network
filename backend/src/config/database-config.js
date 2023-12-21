const mongoose = require('mongoose');
const mysql = require('mysql');

// Mongo Connection
const mongoConnect = () => {
    const { NODE_ENV, MONGO_HOST, MONGO_ACCESS_USER, MONGO_ACCESS_PASSWORD, MONGO_PORT, MONGO_DATABASE } = process.env;
    const mongoUri = NODE_ENV === 'production' ?
        `mongodb+srv://${MONGO_ACCESS_USER}:${encodeURIComponent(MONGO_ACCESS_PASSWORD)}@${MONGO_HOST}/${MONGO_DATABASE}` :
        `mongodb://${MONGO_ACCESS_USER}:${encodeURIComponent(MONGO_ACCESS_PASSWORD)}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DATABASE}`;
    const mongoConfig = {
        useNewUrlParser: true,
        useUnifiedTopology: true
    };
    // Throw mongoose error if querying fields aren't defined
    mongoose.set('strictQuery', true);
    return mongoose.connect(mongoUri, mongoConfig);
}

// MYSQL Connection
const mysqlConnection = () => {
    const { MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_ACCESS_USER, MYSQL_ACCESS_PASSWORD } = process.env;
    return mysql.createConnection({
        host: MYSQL_HOST,
        port: MYSQL_PORT,
        database: MYSQL_DATABASE,
        user: MYSQL_ACCESS_USER,
        password: MYSQL_ACCESS_PASSWORD
    });
}

const ready = Promise.all([
    mongoConnect(),
    mysqlConnection().connect()
]);

module.exports = {
    ready,
    // Returns the current mongoose instance
    getMongoose: () => mongoose
}