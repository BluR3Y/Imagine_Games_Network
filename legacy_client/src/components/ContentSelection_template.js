import React from "react";
import { ContentSelectionBtn, StyledArticleContentItem, StyledContentSelection, StyledVideoContentItem } from "./styles/ContentSelection.styled";

import Controller from '../assets/icons/controller';
import OpenBook from '../assets/icons/book_open';
import Comment from '../assets/icons/comment';
import Film from '../assets/icons/film';
import TV from '../assets/icons/television';
import MicroChip from '../assets/icons/microchip';
import User from '../assets/icons/user';

// class VideoContent extends React.Component {
//     render() {
//         return <h1></h1>
//     }
// }

// class ContentItem extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = {

//         }
//     }
    
//     render() {
//         const {
//             contentInfo,
//             contentType
//         } = this.props;
//         return <StyledContentItem>
//             { contentType === 'video' ? <VideoContent/> : <div>

//             </div> }
//         </StyledContentItem>
//     }
// }

class VideoContentItem extends React.Component {
    render() {
        return <StyledVideoContentItem>

        </StyledVideoContentItem>
    }
}

class ArticleContentItem extends React.Component {
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

    render() {
        const { contentInfo } = this.props;
        const { getEntertainmentTypeIcon } = this;
        return <StyledArticleContentItem
            contentUrl={contentInfo.content.url}
        >
            <div className="posterContainer">
                <img src={contentInfo.content.feedImage.url} />
            </div>
            <div className="contentInfo">
                <h1>{contentInfo.content.title}</h1>
                <h2>{contentInfo.content.subtitle}</h2>
            </div>
            <div className="additionalContentInfo">
                <div>
                    {getEntertainmentTypeIcon(contentInfo.content.primaryObject.type)}
                    <h1>{contentInfo.content.primaryObject.type}</h1>
                </div>
                <div>
                    <User/>
                    <h1>{contentInfo.content.contributors[0].name}</h1>
                </div>
                <div>
                    <Comment/>
                    <h1>{contentInfo.commentCount}</h1>
                </div>
            </div>
        </StyledArticleContentItem>
    }
}

export default class ContentSelection extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeType: 'articles',
            contentTypes: ['latest', 'videos', 'articles'],
            extendedContentList: false
        }
    }

    setContentType = (event) => {
        this.setState({ activeType: event.currentTarget.value });
    }
    
    testContentItems = () => {
        const items = [];
        for(let i = 0; i < 5; i++) {
            items.push(this.props.articles[i]);
        }
        return items.map((item, index) => <ArticleContentItem key={index} contentInfo={item} />);
    }

    render() {
        const {
            inTheaterMode,
            videos,
            articles
        } = this.props;
        const {
            activeType,
            contentTypes,
            extendedContentList
        } = this.state;
        const {
            setContentType
        } = this;
        return <StyledContentSelection
                inTheaterMode={inTheaterMode}
                extendedContentList={extendedContentList}
            >
            <div className="typeSelection">{contentTypes.map((item, index) => 
                <ContentSelectionBtn
                    value={item} 
                    key={index}
                    selected={item === activeType}
                    onClick={setContentType}
                >{item}</ContentSelectionBtn>)}
            </div>
            <div className="contentWrapper">{this.testContentItems()}</div>
            <button className="extendList" onClick={() => this.setState(prevState => ({ extendedContentList: !prevState.extendedContentList }))}>{extendedContentList ? 'Show Less' : 'Load More'}</button>
        </StyledContentSelection>
    }
}