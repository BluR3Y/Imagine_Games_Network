import React from "react";

import { 
    Nav_Container, 
    Date_Logo, 
    StyledLogo, 
    ContentSelection, 
    SelectionList,
    SelectionList_More,
    Profile,
    ThemeSelection,
    StyledLoadingAdditionalContent,
} from "./styles/Navigation.styled";

import Caret_Down from '../assets/icons/caret_down';

import ProfileImg from '../assets/images/profileImg.jfif';
import SearchBar from "./SearchBar";

export default class Navigation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hiddenContentItems: [],
            additionalSelectionItems: null,
            selectionListRef: React.createRef(),
            searchBarRef: React.createRef(),
            currentDate: null,
        }
    }

    componentDidMount() {
        this.getDate();
        this.getTrendingGames();

        window.addEventListener('load', this.resizeNavigationContent);
        window.addEventListener('resize', this.resizeNavigationContent);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.resizeNavigationContent);
        window.removeEventListener('load', this.resizeNavigationContent);
    }

    getDate = () => {
        var date = new Date();
        var weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        var currWeekday = weekDays[date.getDay()];
        var currDate = months[date.getMonth()] + ' ' + date.getDate();
        this.setState({ currentDate: [currWeekday, currDate] });
    }

    submitSearch = (event) => {
        event.preventDefault();
        var searchInput = event.currentTarget.querySelector('input');
        window.open(`https://www.google.com/search?q=${encodeURIComponent(searchInput.value)} site:ign.com`, '_blank');
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
    }

    searchAutoComplete = async (searchQuery) => {
        const { searchBarRef } = this.state;
        var gamesURL = 'https://api.rawg.io/api/games?';
        var searchParams = {
            key: process.env.REACT_APP_RAWG_API_KEY,
            search: searchQuery,
            page_size: 5,
            search_precise: true,
            search_exact: true,
            // ordering: '-released'
        }
        for (const property in searchParams) {
            gamesURL += `${property}=${searchParams[property]}&`;
        }
        var gameItems = await fetch(gamesURL)
        .then(async res => res.json())
        .then(data => data.results);

        var movieItems = await (async () => {
            if(gameItems.length === 5)
                return [];

            var moviesURL = 'https://api.themoviedb.org/3/search/movie?';
            searchParams = {
                api_key: process.env.REACT_APP_MOVIE_DB_API_KEY,
                query: searchQuery,
            }
            for (const property in searchParams) {
                moviesURL += `${property}=${searchParams[property]}&`;
            }

            var movies = await fetch(moviesURL)
            .then(async res => res.json())
            .then(data => data.results);

            return movies.splice(0, 5);
        })()

        var autoCompleteItems = {
            gameItems: gameItems,
            movieItems: movieItems,
        };
        searchBarRef.current.setState({ autoCompleteItems });
    }

    resizeNavigationContent = () => {
        const { selectionListRef } = this.state;
        const selectionList = selectionListRef.current;
        const listDimensions = selectionList.getBoundingClientRect();
        const listItems = Object.values(selectionList.children);
        const hiddenItems = listItems.filter(item => {
            const itemDimensions = item.getBoundingClientRect();
            return itemDimensions.y > listDimensions.y;
        })

        const hiddenContentItems = hiddenItems.map(item => {
            var linkItem = item.querySelector('a');
            return({ title: linkItem.innerHTML, link: linkItem.href });
        })
        this.setState({ hiddenContentItems })
    }

    getTrendingGames = async () => {
        var gamesURL = 'https://rawg.io/api/games/lists/greatest?';
        var searchParams = {
            key: process.env.REACT_APP_RAWG_API_KEY,
            discover: true,
            ordering: '-added',
            page_size: 10,
        }
        for (const property in searchParams) {
            gamesURL += `${property}=${searchParams[property]}&`;
        }
        var gameItems = await fetch(gamesURL)
        .then(async res => res.json())
        .then(data => data.results)
        this.setState({ additionalSelectionItems: gameItems });
    }

    render() {
        const { currentDate, selectionListRef, hiddenContentItems, searchBarRef, additionalSelectionItems } = this.state;
        const { submitSearch, searchAutoComplete } = this;
        return(<Nav_Container>
            <div className="navMain">
                <Date_Logo>
                    <StyledLogo/>
                    {currentDate && (
                        <h1>
                            <span>{currentDate[0]}</span>
                            <span>{currentDate[1]}</span>
                        </h1>
                    )}
                </Date_Logo>
                <ContentSelection>
                    <SelectionList ref={selectionListRef}>
                        <div><a href='https://www.ign.com/news' target='_blank'>News</a></div>
                        <div><a href='https://www.ign.com/videos' target='_blank'>Videos</a></div>
                        <div><a href='https://www.ign.com/reviews' target='_blank'>Reviews</a></div>
                        <div><a href='https://www.ign.com/watch' target='_blank'>Shows</a></div>
                        <div><a href='https://www.ign.com/wikis' target='_blank'>Wikis</a></div>
                    </SelectionList>
                    <SelectionList_More>
                        <h1>More</h1>
                        <Caret_Down/>
                        <div>
                            {hiddenContentItems.map((item, index) => (
                                <a href={item.link} key={index} tabIndex='-1'>{item.title}</a>
                            ))}
                            <a href="https://www.ign.com/wikis/ign-community-central/How_to_Follow_IGN" tabIndex='-1'>IGN on social</a>
                            <a href="https://corp.ign.com/" tabIndex='-1'>About Us</a>
                            <a href="https://www.ziffdavis.com/accessibility" tabIndex='-1'>Accessibility</a>
                            <a href="https://corp.ign.com/privacy" tabIndex='-1'>Privacy Policy</a>
                            <a href="https://corp.ign.com/user-agreement" tabIndex='-1'>Terms of Use</a>
                            <a href="https://corp.ign.com/standards-and-practices" tabIndex='-1'>Editorial Standards</a>
                            <a href="https://corp.ign.com/ccpa" tabIndex='-1'>Do Not Sell My Personal Information</a>
                            <a href="https://corp.ign.com/sitemap" tabIndex='-1'>Site Map</a>
                            <a href="https://www.ignboards.com/" tabIndex='-1'>Boards</a>
                            <a href="https://corp.ign.com/support" tabIndex='-1'>Contact Support</a>
                        </div>
                    </SelectionList_More>
                    <SearchBar
                        ref={searchBarRef}
                        onSubmit={submitSearch}
                        searchAutoComplete={searchAutoComplete}
                    />
                    <ThemeSelection onClick={this.props.toggleTheme}/>
                    <Profile>
                        <img src={ProfileImg}/>
                        <h1>12</h1>
                    </Profile>
                </ContentSelection>
            </div>
            <div className="navSub">
                {additionalSelectionItems ? (additionalSelectionItems.map(item => (
                    <a href={`https://www.google.com/search?q=${encodeURIComponent(item.name)} site:ign.com`} target='_target' key={item.id}>{item.name}</a>
                ))) : [...Array(8)].map((item,index) => <StyledLoadingAdditionalContent key={index} />)}
            </div>
        </Nav_Container>);
    }
}