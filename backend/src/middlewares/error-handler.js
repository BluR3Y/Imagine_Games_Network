const AppError = require('../utils/app-error');
const { Error: MongooseError } = require('mongoose');

// Middleware that handles errors
module.exports = (err, req, res, next) => {
    switch(true) {
        case err instanceof AppError:
            return err.errorResponse(res);
        // A response object is created for Mongoose Validation Errors
        case err instanceof MongooseError.ValidationError:
            return (new AppError(400, 'INVALID_ARGUMENT', 'Invalid field values', Object.entries(err.errors).reduce((accumulator, [key, value]) => ({
                ...accumulator,
                [key]: {
                    message: value.message,
                    type: value.kind
                }
            }), {})).errorResponse(res));

        default:
            console.error(err);
            return (new AppError(500, 'INTERNAL', 'Internal server error').errorResponse(res));
    }
}