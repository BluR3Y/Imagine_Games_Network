const express = require('express');
const router = express.Router();

require('./routes/poll-routes').connect(router);

module.exports = router;