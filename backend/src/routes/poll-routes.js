const pollController = require('../controllers/poll-controller');

module.exports.connect = function(router) {
    router.post('/polls', pollController.createPoll);
}