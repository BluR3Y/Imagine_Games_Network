import React from "react";
import {
    StyledSideNavigation, 
    StyledHamburgerButton, 
    StyledProfile,
    StyledProfileImg,
    ThemeToggle,
    ContentList,
    NavContent,
    ContentPage,
    ReturnMainPage, 
    ContentLink,
} from './styles/SideNavigation.styled';

import { Date_Logo, StyledLogo } from './styles/Navigation.styled';

import Sun from '../assets/icons/sun';
import Moon from '../assets/icons/moon';
import News from '../assets/icons/news';
import Videos from '../assets/icons/videos';
import Television from "../assets/icons/television";
import Compass from '../assets/icons/compass';
import Reviews from '../assets/icons/reviews';
import Circle_Ellipsis from '../assets/icons/circle_ellipsis';

export default class SideNavigation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            openSideNav: false,
            openPage: 'mainPage',
            currentDate: null,
        }
    }

    componentDidMount() {
        this.getDate();
    }

    getDate = () => {
        var date = new Date();
        var weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        var currWeekday = weekDays[date.getDay()];
        var currDate = months[date.getMonth()] + ' ' + date.getDate();
        this.setState({ currentDate: [currWeekday, currDate] });
    }

    render() {

        const { openSideNav, openPage, currentDate } = this.state;

        return(<StyledSideNavigation
            open={openSideNav}
        >
            <div className="navMain">
                <StyledHamburgerButton onClick={() => this.setState(prevState => ({ openSideNav: !prevState.openSideNav }))} />
                <NavContent openPage={openPage}>
                    <ContentPage className="mainPage" activePage={openPage}>
                        <Date_Logo>
                            <StyledLogo/>
                            {currentDate && (
                                <h1>
                                    <span>{currentDate[0]}</span>
                                    <span>{currentDate[1]}</span>
                                </h1>
                            )}
                        </Date_Logo>
                        <StyledProfile>
                            <StyledProfileImg/>
                            <h1>John Doe</h1>
                        </StyledProfile>
                        <ThemeToggle>
                            <div/>
                            <button className="classicBtn" onClick={this.props.toggleTheme}><Sun/></button>
                            <button className="darkBtn" onClick={this.props.toggleTheme}><Moon/></button>
                        </ThemeToggle>
                        <ContentList className="mainContent">
                            <ContentLink  onClick={() => this.setState({ openPage: 'newsPage' })}>
                                <News/><h1>News</h1>
                            </ContentLink>
                            <ContentLink  onClick={() => this.setState({ openPage: 'videosPage' })}>
                                <Videos/><h1>Videos</h1>
                            </ContentLink>
                            <ContentLink  onClick={() => this.setState({ openPage: 'reviewsPage' })}>
                                <Reviews style={{fill:'none'}} /><h1>Reviews</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/watch'>
                                <Television/><h1>Shows</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/wikis'>
                                <Compass/><h1>Wikis</h1>
                            </ContentLink>
                            <ContentLink  onClick={() => this.setState({ openPage: 'morePage' })}>
                                <Circle_Ellipsis/><h1>More</h1>
                            </ContentLink>
                        </ContentList>
                    </ContentPage>
                    <ContentPage className="newsPage">
                        <ReturnMainPage onClick={() => this.setState({ openPage: 'mainPage' })}/>
                        <h1 className="pageTitle">News</h1>
                        <ContentList className="newsContent">
                            <ContentLink href='https://www.ign.com/news'>
                                <h1>All News</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/playstation'>
                                <h1>PlayStation</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/xbox'>
                                <h1>Xbox</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/nintendo'>
                                <h1>Nintendo</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/pc'>
                                <h1>PC</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/mobile'>
                                <h1>Mobile</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/movies'>
                                <h1>Movies</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/tv'>
                                <h1>Television</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/comics'>
                                <h1>Comics</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/tech'>
                                <h1>Tech</h1>
                            </ContentLink>
                        </ContentList>
                    </ContentPage>
                    <ContentPage className="videosPage">
                        <ReturnMainPage onClick={() => this.setState({ openPage: 'mainPage' })}/>
                        <h1 className="pageTitle">Videos</h1>
                        <ContentList className="videosContent">
                            <ContentLink  href='https://www.ign.com/watch'>
                                <h1>Original Shows</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/watch?filter=popular'>
                                <h1>Popular</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/watch?filter=trailers'>
                                <h1>Trailers</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/watch?filter=gameplay'>
                                <h1>Gameplay</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/watch?filter=videos'>
                                <h1>All Videos</h1>
                            </ContentLink>
                        </ContentList>
                    </ContentPage>
                    <ContentPage className="reviewsPage">
                        <ReturnMainPage onClick={() => this.setState({ openPage: 'mainPage' })}/>
                        <h1 className="pageTitle">Reviews</h1>
                        <ContentList className="reviewsContent">
                            <ContentLink href='https://www.ign.com/reviews'>
                                <h1>All Reviews</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/editors-choice'>
                                <h1>Editor's Choice</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/reviews/games'>
                                <h1>Game Reviews</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/reviews/movies'>
                                <h1>Movie Reviews</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ign.com/reviews/tv'>
                                <h1>TV Show Reviews</h1>
                            </ContentLink>
                            <ContentLink  href='https://www.ign.com/reviews/tech'>
                                <h1>Tech Reviews</h1>
                            </ContentLink>
                        </ContentList>
                    </ContentPage>
                    <ContentPage className="morePage">
                        <ReturnMainPage onClick={() => this.setState({ openPage: 'mainPage' })}/>
                        <h1 className="pageTitle">More</h1>
                        <ContentList className="moreContent">
                            <ContentLink href='https://www.ign.com/wikis/ign-community-central/How_to_Follow_IGN'>
                                <h1>IGN on social</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/'>
                                <h1>About Us</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ziffdavis.com/accessibility'>
                                <h1>Accessibility</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/privacy'>
                                <h1>Privacy Policy</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/user-agreement'>
                                <h1>Terms of Use</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/standards-and-practices'>
                                <h1>Editorial Standards</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/ccpa'>
                                <h1>Do Not Sell My Personal Information</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/sitemap'>
                                <h1>Site Map</h1>
                            </ContentLink>
                            <ContentLink href='https://www.ignboards.com/'>
                                <h1>Boards</h1>
                            </ContentLink>
                            <ContentLink href='https://corp.ign.com/support'>
                                <h1>Contact Support</h1>
                            </ContentLink>
                        </ContentList>
                    </ContentPage>
                </NavContent>
            </div>
            <button className="collapseBtn" onClick={() => this.setState(prevState => ({ openSideNav: !prevState.openSideNav }))} />
        </StyledSideNavigation>);
    }
}