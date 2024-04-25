import { DataTypes } from 'sequelize';
import sequelize from '../config/database';

const Video = sequelize.define('videos', {
    id: {
        type: DataTypes.UUIDV4,
        primaryKey: true,
        autoIncrement: false
    },
});

export default Video;