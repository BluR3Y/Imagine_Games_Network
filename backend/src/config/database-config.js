const { MongoClient } = require('mongodb');
const mongoose = require('mongoose');
const redis = require('redis');
const {
    MONGO_ACCESS_USER,
    MONGO_ACCESS_PASSWORD,
    MONGO_HOST,
    MONGO_PORT,
    MONGO_DATABASE,
    REDIS_HOST,
    REDIS_PORT
} = process.env;

// MongoDB Client
const mongoUri = `mongodb://${MONGO_ACCESS_USER}:${encodeURIComponent(MONGO_ACCESS_PASSWORD)}@${MONGO_HOST}:${MONGO_PORT}/${MONGO_DATABASE}`;
const mongoClient = new MongoClient(mongoUri);
// Mongo Connection
const mongoConnect = async () => {
    try {
        // Connect the client to the server
        await mongoClient.connect();
        // Send a ping to confirm a successful connection
        await mongoClient.db("admin").command({ ping: 1 });
        // Connect mongoose to the server
        mongoose.connect(mongoUri);
    } finally {
        // Ensures that the client will close when you finish/error
        await mongoClient.close();
    }
}

// Redis Client
const redisClient = redis.createClient({
    url: `redis://${REDIS_HOST}:${REDIS_PORT}`
});

const ready = Promise.all([
    mongoConnect(),
    redisClient.connect()
]);

module.exports = {
    ready,
    // Returns mongo client
    mongoClient,
    // Returns redis client
    redisClient
}