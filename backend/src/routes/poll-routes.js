const pollController = require('../controllers/poll-controller');

module.exports.connect = function(router) {
    router.post('/polls', pollController.createPoll);
    router.patch('/polls/:pollId', pollController.updatePoll);
    router.get('/polls/:pollId', pollController.getPoll);
    router.delete('/polls/:pollId', pollController.deletePoll);
}