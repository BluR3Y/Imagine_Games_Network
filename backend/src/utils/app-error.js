class AppError extends Error {
    constructor(statusCode, errorCode, message, errors) {
        super(message);
        this.statusCode = statusCode;
        this.errorCode = errorCode;
        this.errors = errors;
        Error.captureStackTrace(this, this.constructor);
    }

    errorResponse(res) {
        const { statusCode, errorCode, message, errors } = this;
        return res.status(statusCode).send({
            code: errorCode,
            message: message,
            ...(this.errors ? { errors: errors } : {})
        });
    }
}
module.exports = AppError;