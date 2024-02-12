const mongoose = require('mongoose')

const contentSchema = new mongoose.Schema({
    legacy_id: {
        type: Number
    },
    url: {
        type: String
    },
    slug: {
        
    }
});