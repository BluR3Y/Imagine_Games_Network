import React from "react";

import {
    StyledSearchBar,
    StyledAutoCompleteGame,
    StyledAutoCompleteMovie,
    StyledLoadingAutoCompleteItem
} from './styles/SearchBar.styled';

import Magnifying_Glass from "../assets/icons/magnifying_glass";
import Controller from '../assets/icons/controller';
import Film from '../assets/icons/film';

class AutoCompleteGame extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gamePlatforms: null,
            imageLoaded: (this.props.itemProps.background_image ? false : true),
        }
    }

    componentDidMount() {
        this.getPlatforms(this.props.itemProps.parent_platforms);
    }

    componentDidUpdate(prevProps) {
        if(prevProps.itemProps !== this.props.itemProps) {
            this.getPlatforms(this.props.itemProps.parent_platforms);
        }
    }

    async getPlatforms(platforms = []) {
        var otherPlatforms = 0;
        var platformImports = await Promise.allSettled(platforms.map(async (platform) => {
            try {
                var platformImport = await import(`../assets/icons/platforms/${platform.platform.slug}`);
                var platformItem = await React.lazy( async () => platformImport);
                return platformItem;
            }catch(err) {
                return Promise.reject();
            }
        }))
        var filteredPlatforms = platformImports.filter(platform => {
            if(platform.status === 'rejected')
                otherPlatforms += 1;
            return platform.status === 'fulfilled';
        })
        var gamePlatforms = filteredPlatforms.map(platform => platform.value);
        if(otherPlatforms > 0)
            gamePlatforms.push(() => React.createElement('h1', null, `+ ${otherPlatforms}`));
        this.setState({ gamePlatforms });
    }

    render() {
        const { gamePlatforms, imageLoaded } = this.state;
        return(
            <>
            <StyledAutoCompleteGame
                onClick={this.props.onClick}
                isLoaded={gamePlatforms !== null && imageLoaded}
            >
                <div className="AutoComplete-Img">
                    {this.props.itemProps.background_image ? 
                        <img 
                            src={this.props.itemProps.background_image} 
                            onLoad={() => this.setState({ imageLoaded: true })}
                        /> 
                        : 
                        <Controller />
                    }
                </div>
                <div className="AutoComplete-Info">
                    <div>
                        {gamePlatforms && gamePlatforms.map((Item, index) => (<Item key={index}/>))}
                    </div>
                    <h1>{this.props.itemProps.name}</h1>
                </div>
            </StyledAutoCompleteGame>
            {(!imageLoaded || gamePlatforms === null) && (<StyledLoadingAutoCompleteItem/>)}
            </>
        );
    }
}

class AutoCompleteMovie extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            imageLoaded: (this.props.itemProps.poster_path ? true : true)
        }
    }

    render() {
        const { imageLoaded } = this.state;
        return(<>
        <StyledAutoCompleteMovie
            onClick={this.props.onClick}
            isLoaded={imageLoaded}
        >
            <div className="AutoComplete-Img">
                {this.props.itemProps.poster_path ? 
                    <img
                        src={'https://image.tmdb.org/t/p/w500' + this.props.itemProps.poster_path}
                        onLoad={() => this.setState({ imageLoaded: true })}
                    />
                    :
                    <Film/>
                }
            </div>
            <div className="AutoComplete-Info">
                <h1>{this.props.itemProps.title}</h1>
                <h2>{this.props.itemProps.release_date}</h2>
            </div>
        </StyledAutoCompleteMovie>
        {!imageLoaded && (<StyledLoadingAutoCompleteItem/>)}
        </>);
    }
}

export default class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchQuery: '',
            searchBarRef: React.createRef(),
            openSearchBar: false,
            searchInputFocused: false,
            autoCompleteItems: null,
            typingTimeout: 0,
        }
    }

    componentDidMount() {
        const { searchBarRef } = this.state;
        const searchInput = searchBarRef.current.querySelector('input');
        searchBarRef.current.addEventListener('submit', this.props.onSubmit);
        searchInput.addEventListener('input', this.updateQuery);
    }

    componentWillUnmount() {
        const { searchBarRef } = this.state;
        const searchInput = searchBarRef.current.querySelector('input');
        searchBarRef.current.removeEventListener('submit', this.props.onSubmit);
        searchInput.removeEventListener('input', this.updateQuery);
    }

    toggleSearchFocus = (event) => {
        if(event.type === 'blur') {
            const searchForm = this.state.searchBarRef.current;
            requestAnimationFrame(() => {
                const newTarget = document.activeElement;
                if(searchForm.contains(newTarget)) 
                    newTarget.click();
                this.setState(prevState => ({ searchInputFocused: !prevState.searchInputFocused }));
            })
        }else{
            if(this.state.autoCompleteItems === null)
                this.props.searchAutoComplete(this.state.searchQuery);
            this.setState(prevState => ({ searchInputFocused: !prevState.searchInputFocused }));
        }
    }

    selectAutoComplete = (event) => {
        var searchStr = event.currentTarget.querySelector('h1').innerText;
        var searchBarRef = this.state.searchBarRef.current;
        var inputEl = searchBarRef.querySelector('input');
        inputEl.value = searchStr;
        searchBarRef.dispatchEvent(new Event('submit'));
    }

    updateQuery = (event) => {
        if(this.state.typingTimeout) {
            clearTimeout(this.state.typingTimeout);
        }

        this.setState({
            searchQuery: event.target.value,
            typingTimeout: setTimeout(function () {
                this.props.searchAutoComplete(this.state.searchQuery);
            }.bind(this), 150)
        })
    }

    render() {
        const { searchBarRef, openSearchBar, autoCompleteItems, searchInputFocused } = this.state;
        return(<StyledSearchBar
            ref={searchBarRef} 
            open={openSearchBar} 
            searchInputFocused={searchInputFocused}
            emptyAutoComplete={(() => {
                if(autoCompleteItems === null)
                    return true;
                return (Math.max(autoCompleteItems.gameItems.length, autoCompleteItems.movieItems.length) === 0)
            })()}
        >
            <div className="searchForm">
                <button type='button' onClick={() => this.setState(prevState => ({ openSearchBar: !prevState.openSearchBar }))}>
                    <Magnifying_Glass/>
                </button>
                <input 
                    type='text' 
                    placeholder="The Last of Us 2 Review" 
                    tabIndex='-1' 
                    onFocus={this.toggleSearchFocus}
                    onBlur={this.toggleSearchFocus}
                />
            </div>
            <div className="searchAutoComplete">
                {autoCompleteItems &&
                 autoCompleteItems.gameItems.map(item => (
                    <AutoCompleteGame
                        key={item.id}
                        itemProps={item}
                        onClick={this.selectAutoComplete}
                    />
                ))}
                {autoCompleteItems &&
                 autoCompleteItems.movieItems.map(item => (
                    <AutoCompleteMovie
                        key={item.id}
                        itemProps={item}
                        onClick={this.selectAutoComplete}
                    />
                 ))
                }
            </div>
        </StyledSearchBar>);
    }
}
