import React from "react";
import { StyledVideoQueue, StyledQueueVideo } from './styles/VideoQueue.styled';

import Controller from '../assets/icons/controller';
import OpenBook from '../assets/icons/book_open';
import Comment from '../assets/icons/comment';
import Film from '../assets/icons/film';
import TV from '../assets/icons/television';
import MicroChip from '../assets/icons/microchip';
import User from '../assets/icons/user';

class QueueVideo extends React.Component {
    getEntertainmentTypeIcon = (type) => {
        var Icon;
        switch (type) {
            case 'Game':
                Icon = Controller;
                break;
            case 'Tech':
                Icon = MicroChip;
                break;
            case 'Movie':
                Icon = Film;
                break;
            case 'Show':
                Icon = TV;
                break;
            case 'Comic':
                Icon = OpenBook;
                break;
            default:
                break;
        }
        return <Icon/>
    }

    convertTimestamp = (timestamp) => {
        var months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        var date = new Date(timestamp);
        return(`${months[date.getMonth()]} ${date.getDate()} ${date.getFullYear()}`);
    }

    render() {
        const { contentInfo } = this.props;
        const { getEntertainmentTypeIcon, convertTimestamp } = this;

        return <StyledQueueVideo>
            <div className="previewPlayer">
            
            </div>
            <div className="contentInfo">
                <h1>{contentInfo.metadata.title}</h1>
                <h2>{convertTimestamp(contentInfo.metadata.publishDate)}</h2>
            </div>
            <div className="additionalContentInfo">
                <div>
                    {getEntertainmentTypeIcon(contentInfo.objectRelations[0].objectType)}
                    <h1>{contentInfo.objectRelations[0].objectType}</h1>
                </div>
                <div>
                    <User/>
                    <h1>{contentInfo.metadata.author}</h1>
                </div>
                <div>
                    <Comment/>
                    <h1>{contentInfo.commentCount}</h1>
                </div>
            </div>
        </StyledQueueVideo>
    }
}

export default class VideoQueue extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            extendedList: false
        }
    }

    testContentItems = () => {
        const items = [];
        for(let i = 0; i < 3; i++) {
            items.push(this.props.videos[i]);
        }
        return items.map((item, index) => <QueueVideo key={index} contentInfo={item} />);
    }


    render() {
        const {
            videos,
            inTheaterMode
        } = this.props;
        const {
            extendedList
        } = this.state;
        return <StyledVideoQueue
            inTheaterMode={inTheaterMode}
            extendedList={extendedList}
        >
            <div className="contentWrapper">{this.testContentItems()}</div>
            <button className="extendList" onClick={() => this.setState(prevState => ({ extendedList: !prevState.extendedList }))}>{extendedList ? 'Show Less' : 'Load More'}</button>
        </StyledVideoQueue>
    }
}