import { Sequelize } from 'sequelize';

const sequelize = () => {
    const {
        POSTGRES_ACCESS_USER,
        POSTGRES_ACCESS_PASSWORD,
        POSTGRES_DATABASE,
        POSTGRES_HOST,
        POSTGRES_PORT
    } = process.env;

    return new Sequelize({
        dialect: 'postgres',
        host: POSTGRES_HOST,
        port: POSTGRES_PORT,
        username: POSTGRES_ACCESS_USER,
        password: POSTGRES_ACCESS_PASSWORD,
        database: POSTGRES_DATABASE
    });
}

export default sequelize();