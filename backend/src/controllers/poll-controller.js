const Poll = require('../models/poll-model');

module.exports.createPoll = async (req, res, next) => {
    try {
        const createdPoll = new Poll(req.body);
        await createdPoll.save();
        // Last Here
    } catch(err) {
        next(err);
    }
}