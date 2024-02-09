const mongoose = require('mongoose')

const articleSchema = new mongoose.Schema({
    content: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Content',
        required: true
    },
    article: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'ArticleContent',
        required: true
    },
    review: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'OfficialReview'
    }
});

module.exports = mongoose.model('Article', articleSchema);