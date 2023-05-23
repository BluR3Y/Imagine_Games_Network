const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');

const dbConnect = require('./config/database-config');
const router = require('./router');
const errorHandler = require('./middlewares/error-handler');

dbConnect.ready.then(_ => {

    // For parsing application/json
    app.use(bodyParser.json());
    // For parsing application/x-www-form-urlencoded
    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(cors({
        origin: '*',
        credentials: true
    }));
    // Set the router entry point
    app.use('/', router);
    // Set the Error Handler Middleware
    app.use(errorHandler);
    // Run Server
    app.listen(3000, () => console.log('Server is listening at http://localhost:3000'));
})
.catch(err => {
    console.log('Error occured while connection to database:', err);
})