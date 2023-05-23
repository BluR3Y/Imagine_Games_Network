const Poll = require('../models/poll-model');
const AppError = require('../utils/app-error');

// Route handler for creating polls
module.exports.createPoll = async (req, res, next) => {
    try {
        const createdPoll = new Poll(req.body);
        await createdPoll.save();
        
        res.status(201).send(); // Modify response
    } catch(err) {
        next(err);
    }
}

// Route handler for modifying polls
module.exports.updatePoll = async (req, res, next) => {
    try {
        const { pollId } = req.params;
        const pollDocument = await Poll.findById(pollId);

        if (!pollDocument) {
            throw new AppError(404, 'NOT_FOUND', 'Poll does not exist');
        }
        pollDocument.set(req.body);
        await pollDocument.save();
        res.status(204).send();
    } catch(err) {
        next(err);
    }
}

// Route handler for deleting polls
module.exports.deletePoll = async (req, res, next) => {
    try {
        const { pollId } = req.params;
        const pollDocument = await Poll.findById(pollId);

        if (!pollDocument) {
            throw new AppError(404, 'NOT_FOUND', 'Poll does not exist');
        }
        await pollDocument.deleteOne();
        res.status(204).send();
    } catch(err) {
        next(err);
    }
}

// Route handler for retrieving polls
module.exports.getPoll = async (req, res, next) => {
    try {
        const { pollId } = req.params;
        const pollDocument = await Poll.findById(pollId);

        if (!pollDocument) {
            throw new AppError(404, 'NOT_FOUND', 'Poll does not exist');
        }


    } catch(err) {
        next(err);
    }
}

// Route handler for searching polls
module.exports.searchPolls = async (req, res, next) => {
    try {

    } catch(err) {
        // Last Here
    }
}