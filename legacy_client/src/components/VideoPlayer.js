import React from "react";
import { connect } from "react-redux";
import {
    setAutoPlay,
    setChaptersOpen,
    setVolume
} from '../redux/actions';

import { 
    AutoPlayBtn,
    VideoChapters,
    Controls, 
    Header, 
    MainControls, 
    MiniPlayerBtn, 
    RangeSlider, 
    ResolutionForm, 
    ResolutionInput, 
    ResolutionSelection, 
    ShareVideoBtn, 
    StyledLoadingVideoPlayer, 
    StyledVideoPlayer, 
    StyledVideoPlayerLoading, 
    TheaterModeBtn, 
    Thumbnail, 
    ToggleFullScreen, 
    TogglePlayPause, 
    ToggleVolume,
    ToggleVideoChapters,
    ChapterItem
} from "./styles/VideoPlayer.styled";

import Standard_Definition from '../assets/icons/standard_definition';
import High_Definition from '../assets/icons/high_definition';

class VideoPlayer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeThumbnail: null,
            activeVideoIndex: null,
            isActive: false,
            isPlaying: false,
            idleTimer: null,
            isIdle: false,
            isMuted: true,
            isReadyToPlay: false,
            videoElapsedTime: 0,
            resolutionMenuOpen: false,
            miniPlayerMode: false,
            fullscreenMode: false,
            videoPlayer: React.createRef(),
            progressBar: React.createRef(),
            volumeSlider: React.createRef(),
            chapterContainer: React.createRef(),
            media: React.createRef()
        }
    }

    componentDidMount() {
        this.setActiveVideoIndex();
        window.addEventListener('resize', this.setActiveThumbnail);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.setActiveThumbnail);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

        if(prevState.activeVideoIndex !== this.state.activeVideoIndex) {
            this.handleActiveVideoIndexChange(prevState.videoElapsedTime, prevState.isPlaying);
        }
        if (this.state.isReadyToPlay && !this.state.isActive && this.props.autoPlay) {
            this.startVideo();
        }
        // if (prevState.isReadyToPlay !== this.state.isReadyToPlay && (!this.state.isActive && this.props.autoPlay)) {
        //     this.startVideo();
        // }
    }

    setActiveVideoIndex = () => {
        const { videoQualities } = this.props;
        const { downlink, effectiveType } = navigator.connection;
        const availableQuality = videoQualities.reduce((accumulator, { height }) => {
            switch (height) {
                case 234:
                    accumulator.push('very-low');
                    break;
                case 360:
                    accumulator.push('low');
                    break;
                case 540:
                    accumulator.push('medium');
                    break;
                case 720:
                    accumulator.push('high');
                    break;
                case 1080:
                    accumulator.push('very-high');
                default:
                    break;
            }
            return accumulator;
        }, []);

        var activeVideoIndex;
        if (effectiveType === '4g' && downlink >= 8 && availableQuality.includes('very-high')) {
            activeVideoIndex = availableQuality.indexOf('very-high');
        } else if (effectiveType === '4g' && availableQuality.includes('high')) {
            activeVideoIndex = availableQuality.indexOf('high');
        } else if (downlink >= 6 && availableQuality.includes('medium')) {
            activeVideoIndex = availableQuality.indexOf('medium');
        } else if (downlink >= 4 && availableQuality.includes('low')) {
            activeVideoIndex = availableQuality.indexOf('low');
        } else {
            activeVideoIndex = availableQuality.indexOf('very-low');
        }

        this.setState({ activeVideoIndex });
    }

    setActiveThumbnail = () => {
        const { videoThumbnails } = this.props;
        const { videoPlayer } = this.state;
        var pixelCount = videoPlayer.current.clientHeight * videoPlayer.current.clientWidth;
        var activeThumbnail = videoThumbnails[0];
        for(var i = 0; i < videoThumbnails.length; i++) {
            if(videoThumbnails[i].height + videoThumbnails[i].width > pixelCount)
                break;
            activeThumbnail = videoThumbnails[i];
        }
        this.setState({ activeThumbnail });
    }

    startVideo = () => {
        const { media, videoPlayer, isReadyToPlay } = this.state;
        if (!isReadyToPlay) {
            return;
        }

        var playMedia = media.current.play();
        if(playMedia !== undefined) {
            playMedia.then(_ => {
                videoPlayer.current.addEventListener('mousemove', this.handleIdle);
                this.setState({ isActive: true });
            })
            .catch(err => {
                console.error('Error While Starting Video: ', err);
            })
        }
    }

    playPauseMedia = () => {
        const { media } = this.state;

        if(media.current.paused) {
            var playMedia = media.current.play();
            if(playMedia !== undefined) {
                playMedia
                .catch(err => {
                    console.error('Error While Playing Video: ', err);
                })
            }
        }else{
            media.current.pause()
        }
    }

    toggleVolume = () => {
        this.setState(prevState => ({ isMuted: !prevState.isMuted }));
    }

    setVolume = (event) => {
        const { media } = this.state;
        media.current.volume = event.currentTarget.value;
    }

    handleVolumeChange = (event) => {
        const { volume, muted } = event.currentTarget;

        this.props.updateVolume(volume);
        this.setState({ isMuted: muted });
    }

    updateElapsedTime = (event) => {
        const videoElapsedTime = event.currentTarget.currentTime;
        this.setState({ videoElapsedTime });
    }

    setVideoProgress = (event) => {
        const { media } = this.state;
        media.current.currentTime = event.currentTarget.value;
    }

    setResolution = (event) => {
        var activeVideoIndex = event.target.value;
        this.setState({ activeVideoIndex, resolutionMenuOpen: false, isReadyToPlay: false });
    }

    handleActiveVideoIndexChange = (prevElapsedTime, prevIsPlaying) => {
        const { media } = this.state;
        media.current.load();
        media.current.currentTime = prevElapsedTime;
        if(prevIsPlaying)
            media.current.play();
    }

    handleLoadedVideo = () => {
        this.setActiveThumbnail();
        const { videoChapters, chapterCaptures, updateChapterCaptures } = this.props;
        const { media, videoElapsedTime, isActive, autoPlay } = this.state;
        media.current.volume = this.props.volume;

        if (updateChapterCaptures && videoChapters?.length && chapterCaptures.length !== videoChapters.length) {
            media.current.addEventListener('seeked', this.captureChapterFrames);
            media.current.currentTime = videoChapters[0].time;
        } else {
            this.setState({ isReadyToPlay: true });
        }
    }

    copyToClipBoard = () => {

    }

    toggleFullScreen = () => {
        const { videoPlayer } = this.state;
        if(document.fullscreenElement) {
            document.exitFullscreen()
            .then(() => this.setState({ fullscreenMode:false }))
            .catch((err) => console.error('Error While Exiting Full Screen: ', err));
        }else{
            videoPlayer.current.requestFullscreen()
            .then(() => this.setState({ fullscreenMode: true }))
            .catch((err) => console.error('Error While Entering Full Screen: ', err));
        }
    }

    handleIdle = () => {    // buggy
        // var { idleTimer, isIdle } = this.state;

        // clearTimeout(idleTimer);
        // isIdle = false;
        // idleTimer = setTimeout(() => {
        //     this.setState({ isIdle: true });
        // }, 5000);
        // this.setState({ idleTimer, isIdle });
    }

    // Modify#2
    captureChapterFrames = () => {
        // take into account invalid times
        const { media } = this.state;
        const { videoChapters, chapterCaptures, updateChapterCaptures } = this.props;

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        var currentCapture = chapterCaptures.length;

        canvas.width = media.current.videoWidth;
        canvas.height = media.current.videoHeight;
        context.drawImage(media.current, 0, 0, canvas.width, canvas.height);
        console.log(chapterCaptures)
        updateChapterCaptures([...chapterCaptures, <ChapterItem
            key={currentCapture}
            value={videoChapters[currentCapture].time}
            posterSrc={canvas.toDataURL()}
            chapterTitle={videoChapters[currentCapture].description}
            onClick={this.setVideoProgress}
        />])

        if (++currentCapture < videoChapters.length) {
            media.current.currentTime = videoChapters[currentCapture].time;
        } else {
            media.current.removeEventListener('seeked', this.captureChapterFrames);
            media.current.currentTime = 0;
            this.setState({ isReadyToPlay: true });
        }
    }
    
    HH_MM_SS = seconds => {
        return (seconds < 3600 ? 
            new Date(seconds * 1000).toISOString().substring(14, 19) :
            new Date(seconds * 1000).toISOString().substring(11, 16)
        );
    }

    render() {
        const {
            autoPlay,
            updateAutoPlay,
            chaptersOpen,
            updateChaptersOpen,
            volume,
            videoQualities,
            videoThumbnails,
            videoTitle,
            videoUrl,
            videoDuration,
            chapterCaptures,
            theaterMode,
            updateTheaterMode,
            toggleableTheaterMode,
            toggleableVideoChapters
        } = this.props;
        const { 
            activeThumbnail, 
            activeVideoIndex, 
            media, 
            videoPlayer, 
            volumeSlider,
            chapterContainer,
            isActive, 
            isPlaying,
            isMuted,
            miniPlayerMode, 
            videoElapsedTime, 
            isIdle, 
            resolutionMenuOpen,
            isReadyToPlay,
            fullscreenMode
        } = this.state;
        const { 
            startVideo, 
            playPauseMedia, 
            setVolume, 
            updateElapsedTime, 
            setVideoProgress, 
            copyToClipBoard, 
            handleLoadedVideo, 
            handleVolumeChange, 
            setResolution,
            toggleFullScreen,
            toggleVolume,
            HH_MM_SS
        } = this;

        if(activeVideoIndex === null) {
            return <StyledLoadingVideoPlayer/>
        }

        return(<StyledVideoPlayer 
            ref={videoPlayer} 
            idle={isIdle}   
            isReadyToPlay={isReadyToPlay}
            miniPlayerMode={miniPlayerMode}
        >
            <Header isActive={isActive} >
                <a href={videoUrl}>{videoTitle}</a>
                <ShareVideoBtn onClick={copyToClipBoard} />
            </Header>
            <Thumbnail 
                thumbnail={activeThumbnail}
                duration={HH_MM_SS(videoDuration)}
                onClick={startVideo}
                isActive={isActive}
            />
            {!isReadyToPlay && <StyledVideoPlayerLoading/>}
            <video 
                ref={media} 
                onClick={playPauseMedia}
                onTimeUpdate={updateElapsedTime} 
                onVolumeChange={handleVolumeChange}
                muted={isMuted}
                onLoadedData={handleLoadedVideo}
                crossOrigin="anonymous"
                onPlay={() => this.setState({ isPlaying: true })}
                onPause={() => this.setState({ isPlaying: false })}
            >
                <source
                    src={videoQualities[activeVideoIndex].url}
                    type={`video/${videoQualities[activeVideoIndex].url.split('.').pop()}`}
                />
            </video>
            <Controls isActive={isActive}>
                <AutoPlayBtn 
                    isPlaying={isPlaying} 
                    isActive={isActive} 
                    autoPlay={autoPlay} 
                    onClick={() => updateAutoPlay(!autoPlay)}
                />
                { chapterCaptures.length !== 0 && <VideoChapters
                    ref={chapterContainer}
                    isOpen={chaptersOpen}    
                >{chapterCaptures}</VideoChapters> }
                <RangeSlider
                    min='0'
                    max={videoDuration}
                    step={videoDuration / 1000}
                    value={videoElapsedTime}
                    onInput={setVideoProgress}
                    onMouseDown={() => media.current.pause()}
                    onMouseUp={() => media.current.play()}
                    className='progressBar'
                />
                <MainControls>
                    <div className="leftControls">
                        <TogglePlayPause isPlaying={isPlaying} toggle={playPauseMedia}/>
                        <div className="volumeControl">
                            <ToggleVolume volume={isMuted ? '0' : volume} toggle={toggleVolume} />
                            <RangeSlider
                                min='0'
                                max='1'
                                step='0.01'
                                value={!isMuted ? volume : '0'}
                                onInput={setVolume}
                                ref={volumeSlider}
                            />
                        </div>
                        <h1>{`${HH_MM_SS(videoElapsedTime)} / ${HH_MM_SS(videoDuration)}`}</h1>
                    </div>
                    <div className="rightControls">
                        { toggleableVideoChapters && chapterCaptures.length !== 0 && <ToggleVideoChapters
                            open={chaptersOpen}
                            onClick={() => updateChaptersOpen(!chaptersOpen)}
                        /> }
                        <ResolutionSelection open={resolutionMenuOpen}>
                            <button
                                title={'Video Quality'}
                                onClick={() => this.setState(prevState => ({ resolutionMenuOpen: !prevState.resolutionMenuOpen }))}
                            >{videoQualities[activeVideoIndex].height > 540 ? <High_Definition/> : <Standard_Definition/>}</button>
                            <ResolutionForm onChange={setResolution}>
                                {videoQualities.map((item, index) => (<ResolutionInput 
                                    itemProps={item} key={index} value={index} checked={activeVideoIndex === index} 
                                />))}
                            </ResolutionForm>
                        </ResolutionSelection>
                        <MiniPlayerBtn onClick={() => this.setState(prevState => ({ miniPlayerMode : !prevState.miniPlayerMode }))} />
                        { toggleableTheaterMode && <TheaterModeBtn activeMode={theaterMode} onClick={updateTheaterMode} /> }
                        <ToggleFullScreen activeMode={fullscreenMode} onClick={toggleFullScreen} />
                    </div>
                </MainControls>
            </Controls>
        </StyledVideoPlayer>);
    }
}

const mapStateToProps = (state) => {
    return {
        autoPlay: state.userReducer.autoPlay,
        volume: state.userReducer.volume,
        chaptersOpen: state.userReducer.chaptersOpen
    }
}

const mapDispatchToProps = (dispatch, getProps) => {
    return {
        updateAutoPlay: (value) => dispatch(setAutoPlay(value)),
        updateVolume: (value) => dispatch(setVolume(value)),
        updateChaptersOpen: (value) => dispatch(setChaptersOpen(value))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(VideoPlayer);