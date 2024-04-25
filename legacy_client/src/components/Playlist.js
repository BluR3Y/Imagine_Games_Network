import React from "react";
import $ from "jquery";
import { faker } from '@faker-js/faker';
import { connect } from "react-redux";

import VideoPlayer from "./VideoPlayer";
// import VideoQueue from "./VideoQueue";
// import ArticleList from './ArticleList';

import { setActiveVideoIndex } from '../redux/actions';

import { CommentCount, StyledPlaylist, VideoTags } from './styles/Playlist.styled';
import { deviceSizes } from './styles/breakPoints';

import Videos from '../data/videos.json';
import Articles from '../data/articles.json';
import CommentSection from "./CommentSection";
import VideoQueue from "./VideoQueue";

class Playlist extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            articles: null,
            videos: null,
            activeVideoTimeStamps: [],
            formattedVideoDescription: null,
            activeVideoComments: null,
            componentError: false,
            theaterMode: false,
            toggleableTheaterMode: null,
            chapterCaptures: [],
            toggleableVideoChapters: null,
            extendedContentList: false,
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(prevProps.activeVideoIndex !== this.props.activeVideoIndex) {
            this.findTimeStamps();
            this.setVideoComments();
        }
        if(prevState.activeVideoTimeStamps !== this.state.activeVideoTimeStamps){}
            // this.captureFrames();
    }

    componentDidMount() {
        Promise.all([
            this.fetchVideos()
            .then(videos => this.setState({
                videos: videos.map(item => this.generateMissingVideoData(item))
            })),
            this.fetchArticles()
            .then(articles => this.setState({
                articles: articles.map(item => ({
                    ...item,
                    commentCount: Math.floor(Math.random() * 200)
                }))
            }))
        ])
        .catch(err => {
            console.error('Error occured while fetching content: ', err);
            this.setState({ componentError: err });
        });
        window.addEventListener('load', this.resolutionBasedAdjustments);
        window.addEventListener('resize', this.resolutionBasedAdjustments);
    }

    fetchVideos = async (startIndex = 0, count = 5) => {
        return Videos;
    }

    fetchArticles = async (startIndex = 0, count = 10) => {
        return Articles;
    }

    resolutionBasedAdjustments = () => {
        const currentWidth = window.innerWidth;

        this.setState({
            toggleableVideoChapters: currentWidth >= 560,
            toggleableTheaterMode: currentWidth >= deviceSizes.minDesktop
        })
    }

    // IGN deciding to remove their public api which required that I use 'unique' methods to tretrieve their content
    generateMissingVideoData = (videoInfo) => ({
        ...videoInfo,
        commentCount: Math.floor(Math.random() * 200),
        metadata: {
            ...videoInfo.metadata,
            description: faker.lorem.paragraph(10),
            publishDate: faker.date.anytime(),
            author: faker.person.fullName()
        },
        tags: (() => {
            const tags = [];
            for (var i = 0; i < 15; i++)
                tags.push(faker.lorem.word());
            return tags;
        })(),
        chapters: (() => {
            const chapters = [];
            const avgLength = videoInfo.metadata.duration / Math.floor(Math.random() * 10);
            var prevTime = 0;
            while (prevTime < videoInfo.metadata.duration) {
                const newTime = Math.floor(Math.random() * avgLength) + prevTime;
                if (newTime >= videoInfo.metadata.duration) {
                    break;
                }

                chapters.push({
                    time: newTime,
                    description: faker.lorem.paragraph(5)
                });
                prevTime = newTime;
            }
            return chapters;
        })()
    });

    findTimeStamps = async () => {
        const { videos } = this.state;
        const { activeVideoIndex } = this.props;
        const videoInfo = videos[activeVideoIndex];
        var formattedVideoDescription = videoInfo['metadata'].description || '';
        var activeVideoTimeStamps = this.getTimeStamps(formattedVideoDescription);

        if(activeVideoTimeStamps) {
            formattedVideoDescription = formattedVideoDescription.substring(0, formattedVideoDescription.indexOf(activeVideoTimeStamps[0].timestamp)) + 
            formattedVideoDescription.substring(formattedVideoDescription.indexOf(activeVideoTimeStamps[activeVideoTimeStamps.length-1].title)+activeVideoTimeStamps[activeVideoTimeStamps.length-1].title.length);            
        }
        this.setState({ formattedVideoDescription, activeVideoTimeStamps });
    }

    getTimeStamps = (str) => {
        var timeStamps = [];
        var lastTSIndex = null;
        var lastTimeStamp = null;
        for(let i =0; i < str.length-4; i++) {
            if(!isNaN(parseFloat(str[i]))) {
                var j = i+1;
                for(; j < str.length && ((/^\d+$/).test(str[j]) || str[j] === ':'); j++);
                var subStr = str.substring(i,j);
                if(this.isTimeStamp(subStr)) {
                    if(lastTSIndex) {
                        let prevTitle = str.substring(lastTSIndex, i);
                        if(prevTitle[0] === ' ')
                            prevTitle = prevTitle.substring(1);
                        if(prevTitle[prevTitle.length-1] === ' ')
                            prevTitle = prevTitle.substring(0, prevTitle.length-1);
                        timeStamps.push({ timestamp: lastTimeStamp, title: prevTitle });
                    }

                    lastTimeStamp = subStr;
                    lastTSIndex = j;
                }

                i = j;
            }
        }
        if(lastTSIndex) {
            let prevTitle = '';
            for(let i = lastTSIndex + 1; i < str.length; i++) {
                if(
                    prevTitle.length &&
                    str[i].match(/^[A-Z]*$/) &&
                    (prevTitle[prevTitle.length-1] !== ' ' && prevTitle[prevTitle.length-1] !== '.')
                ) {
                    break;
                }
                
                prevTitle += str[i];
            }
            timeStamps.push({ timestamp: lastTimeStamp, title: prevTitle });
        }

        return timeStamps.length ? timeStamps : null;
    }

    isTimeStamp = (str) => {
        var parts = str.split(':');
        if(parts.length < 2) 
            return false;
        for(const part of parts) {
            for(const char of part) {
                if(isNaN(char))
                    return false;
            }
        }
        return true;
    }

    convertTimestamp = (timestamp) => {
        var months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
        var date = new Date(timestamp);
        return(`${months[date.getMonth()]} ${date.getDate()} ${date.getFullYear()}`);
    }
 
    setVideoComments = () => {
        const activeVideoComments = [];
        for (var i = 0; i < 15; i++)
            activeVideoComments.push(faker.lorem.paragraph());
        return activeVideoComments;
    }

    render() {
        const {
            activeVideoIndex,
            updateActiveVideoIndex
        } = this.props;
        const { 
            videos,
            articles,
            activeVideoTimeStamps,
            formattedVideoDescription,
            activeVideoComments,
            componentError,
            toggleableTheaterMode,
            theaterMode,
            chapterCaptures,
            toggleableVideoChapters
            // extendedContentList
        } = this.state;
        const {
            convertTimestamp
        } = this;

        if (videos === null || articles === null) {
            return <h1>Ipsum Lorem</h1> // creating Loading component for Playlist
        }

        return <StyledPlaylist 
            theaterMode={theaterMode}
            // extendedContentList={extendedContentList}
        >
            <VideoPlayer
                videoQualities={videos[activeVideoIndex].assets}
                videoThumbnails={videos[activeVideoIndex].thumbnails}
                videoTitle={videos[activeVideoIndex].metadata.title}
                videoUrl={videos[activeVideoIndex].metadata.url}
                videoDuration={videos[activeVideoIndex].metadata.duration}
                toggleableTheaterMode={toggleableTheaterMode}
                theaterMode={theaterMode}
                updateTheaterMode={() => this.setState(prevState => ({ theaterMode: !prevState.theaterMode }))}
                toggleableVideoChapters={toggleableVideoChapters}
                videoChapters={videos[activeVideoIndex].chapters}
                chapterCaptures={chapterCaptures}
                updateChapterCaptures={(chapterEntries) => this.setState({ chapterCaptures: chapterEntries })}
            />
            <div className="videoInfo">
                <h1>{videos[activeVideoIndex].metadata.title}</h1>
                <h2>Published: <span>{convertTimestamp(videos[activeVideoIndex].metadata.publishDate)}</span></h2>
                <CommentCount count={videos[activeVideoIndex].commentCount} />
                <p>{activeVideoTimeStamps.length ? formattedVideoDescription : videos[activeVideoIndex].metadata.description}</p>
                { videos[activeVideoIndex].tags?.length && (
                    <VideoTags>
                        { videos[activeVideoIndex].tags.map((item, index) => (<li key={index}>{item}</li>)) }
                    </VideoTags>
                ) }
                {/* Implement alternative video chapters */}
            </div>
            <VideoQueue
                videos={videos}
                activeVideoIndex={activeVideoIndex}
                updateActiveVideoIndex={updateActiveVideoIndex}
                inTheaterMode={theaterMode}
            />
            {/* <CommentSection
                inTheaterMode={theaterMode}
            >

            </CommentSection> */}
        </StyledPlaylist>
    }
}

const mapStateToProps = (state) => {
    return {
        activeVideoIndex: state.userReducer.activeVideoIndex
    }
}

const mapDispatchToProps = (dispatch, getProps) => {
    return {
        updateActiveVideoIndex: (value) => dispatch(setActiveVideoIndex(value))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Playlist);