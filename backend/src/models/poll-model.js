const mongoose = require('mongoose');

const pollSchema = new mongoose.Schema({
    question: {
        type: String,
        required: true,
        immutable: true
    },
    options: {
        type: [String]
    },
    tags: {
        type: [String],
        default: []
    },
    date_created: {
        type: Date,
        default: () => Date.now(),
        immutable: true
    }
}, { collection: 'polls' });

pollSchema.path('options').validate(function(options) {
    if (options.length < 2 || options.length > 10) {
        return this.invalidate('options', 'A poll must contain between 2 and 10 options', options, 'INVALID_ARGUMENT');
    }

    const optionSet = new Set(options);
    if (optionSet.size !== options.length) {
        return this.invalidate('options', 'Each option in a poll must be unique', options, 'INVALID_ARGUMENT');
    }
    
    return true;
});

pollSchema.path('tags').validate(function(tags) {
    if (tags.length) {
        const tagSet = new Set(tags);
        if (tagSet.size !== tags.length) {
            return this.invalidate('tags', 'Each tag in a poll must be unique', tags, 'INVALID_ARGUMENT');
        }
    }
    return true;
});

module.exports = mongoose.model('Poll', pollSchema);