import React, { Fragment } from "react";

import GlobalStyles from './styles/GlobalStyles';
import Navigation from "./Navigation";
import { ThemeProvider } from "styled-components";
import SideNavigation from "./SideNavigation";
import Playlist from "./Playlist";

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            siteThemes: {
                classic: {
                    type: 'classic',
                    primary: '#bf1313',
                    secondary: '#ffffff',
                    tertiary: '#bbc4c4',
                    quaternary: '#41495a',
                    text: '#181c25',
                    background: '#f6f8f7'
                },
                dark: {
                    type: 'dark',
                    primary: '#bf1313',
                    secondary: '#41495a',
                    tertiary: '#bbc4c4',
                    quaternary: '#ffffff',
                    text: '#f6f8f7',
                    background: '#202634'
                }
            },
            activeTheme: 'dark',
            isMobile: false,
        }
    }

    componentDidMount() {
        this.updateDevice();
        window.addEventListener('resize', this.updateDevice);
    }
    componentWillUnmount() {
        window.removeEventListener('resize', this.updateDevice);
    }

    toggleTheme = () => {
        this.setState({ activeTheme: (this.state.activeTheme == 'classic' ? 'dark' : 'classic') });
    }

    updateDevice = () => {
        this.setState({ isMobile: window.innerWidth < 769 });
    }

    render() {
        const { siteThemes, activeTheme, isMobile } = this.state;
        const { toggleTheme } = this;

        return(<ThemeProvider theme={siteThemes[activeTheme]}>
            <GlobalStyles/>
            <Navigation toggleTheme={toggleTheme} />
            {isMobile && (<SideNavigation toggleTheme={toggleTheme} />)}
            <Playlist/>
        </ThemeProvider>);
    }
}