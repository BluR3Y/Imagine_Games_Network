import {
    SET_AUTO_PLAY,
    SET_CHAPTERS_OPEN,
    SET_VOLUME,
    SET_ACTIVE_VIDEO_INDEX
} from './actions';

const initialState = {
    autoPlay: false,
    chaptersOpen: true,
    volume: 1,
    activeVideoIndex: 2
};

function userReducer(state = initialState, action) {
    switch(action.type) {
        case SET_AUTO_PLAY:
            return {...state, autoPlay: action.payload};
        case SET_VOLUME:
            return {...state, volume: action.payload};
        case SET_CHAPTERS_OPEN:
            return {...state, chaptersOpen: action.payload};
        case SET_ACTIVE_VIDEO_INDEX:
            return {...state, activeVideoIndex: action.payload};
        default:
            return state;
    }
};

export default userReducer;