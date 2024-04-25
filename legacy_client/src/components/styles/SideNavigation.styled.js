import styled, { css } from "styled-components";
import {breakPoints} from './breakPoints';

import { Date_Logo, StyledLogo } from './Navigation.styled';

import Menu_Bars from '../../assets/icons/menu_bars';
import Caret_Down from "../../assets/icons/caret_down";

import ProfileImg from '../../assets/images/profileImg.jpeg';

export const StyledSideNavigation = styled.div`
    position: fixed; // swapped with 'fixed' bc hid behind Playlist Content
    width: 100vw;
    height: 100vh;
    left: 0;
    top: 0;
    pointer-events: none;
    -webkit-tap-highlight-color: transparent;
    z-index: 3;
    
    .navMain {
        height: inherit;
        width: calc(100% - 60px);
        position: absolute;
        z-index: 1;
        left: ${props => props.open ? '0' : 'calc(-100% + 60px)'};
        pointer-events: all;
        transition: left 0.2s ease;
        background-color: ${props => props.theme.secondary};

        @media (min-width: 350px) {
            width: 65vw;
            left: ${props => props.open ? '0' : '-65vw'};
        }
    }

    .collapseBtn {
        display: ${props => props.open ? 'block' : 'none'};
        width: inherit;
        height: inherit;
        backdrop-filter: blur(4px);
        background-color: rgba(0,0,0,0.5);
        pointer-events: all;
    }

    @media ${breakPoints.laptop} {
        display: none;
    }
`;

export const StyledHamburgerButton = styled.button.attrs(() => ({
    children: (<Menu_Bars/>)
}))`
    position: absolute;
    right: -46px;
    top: 5px;
    pointer-events: all;

    svg {
        width: 35px;
        fill: ${props => props.theme.quaternary};
    }
`;

export const ContentPage = styled.div`
    position: absolute;
    top: 0;
    left: 100%;
    height: inherit;
    width: inherit;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: left 0.4s ease;
    padding: 0 30px;
    user-select: none;

    .pageTitle {
        font-weight: 700;
        font-size: 40px;
        line-height: 40px;
        color: ${props => props.theme.quaternary};
        text-align: left;
        width: inherit;
        margin: 30px 0 10px 0;
        border-bottom: 3px solid ${props => props.theme.tertiary};
    }
`;

export const ContentList = styled.div`
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    font-size: 22px;
`;

export const NavContent = styled.div`
    width: 100%;
    height: inherit;
    position: relative;
    overflow: hidden;
    
    .mainPage {
        left: -100%;

        ${Date_Logo} {
            align-self: flex-start;
            margin: 15px 0 0 0;
            height: 40px;

            @media (max-width: 560px ){
                svg {
                    display: none;
                }
            }
        }

        @media (min-height: 550px) {
            ${ContentList} {
                margin-top: 60px;
            }
        }
    }

    .${props => props.openPage} {
        left: 0;
    }

    ${ContentPage}:not(:first-child) > ${ContentList} > a {
        border-left: 3px solid ${props => props.theme.primary};
        padding-left: 3px;
        background-color: rgba(0,0,0,0.2);
    }
`;

export const StyledProfile = styled.div`
    /* width: 220px; */
    width: 100%;
    height: auto;
    border-radius: 18px;
    margin: 20px 0 10px 0;
    backdrop-filter: brightness(70%);
    display: flex;
    flex-direction: column;
    align-items: center;

    h1 {
        display: -webkit-box;
        font-size: 25px;
        font-weight: 500;
        white-space: pre-wrap;
        line-height: 28px;
        text-align: center;
        color: ${props => props.theme.primary};
        margin: 10px 10px;
        -webkit-line-clamp: 2;
        overflow: hidden;
        text-overflow: ellipsis;
        -webkit-box-orient: vertical;
    }
`;

export const StyledProfileImg = styled.a.attrs(() => ({
    children: (<>
        <img src={ProfileImg} />
        <span>12</span>
    </>),
    href: 'https://ign.com/register'
}))`
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 10px 0 0 0;
    display: flex;
    justify-content: center;
    position: relative;
    -webkit-tap-highlight-color: transparent;

    img {
        width: inherit;
        height: inherit;
        object-fit: cover;
        border-radius: inherit;
    }

    span {
        position: absolute;
        left: 5px;
        top: 5px;
        background-color: ${props => props.theme.primary};
        width: 30px;
        height: 30px;
        border-radius: 50%;
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Lato;
        font-size: 16px;
        padding-bottom: 4px;
    }
`;

export const ThemeToggle = styled.div`
    width: 100%;
    backdrop-filter: brightness(70%);
    border-radius: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    flex: 0 0 50px;

    div {
        width: 50%;
        height: 90%;
        border-radius: 8px;
        position: absolute;
        left: ${props => props.theme.type === 'classic' ? '3px' : 'calc(50% - 3px)'};
        top: 50%;
        transform: translate(0,-50%);
        background-color: ${props => props.theme.secondary};
        transition: left 0.3s ease;
    }

    button {
        height: 30px;
        margin: auto;
        z-index: 1;
        -webkit-tap-highlight-color: transparent;

        svg {
            height: inherit;
            fill: ${props=>props.theme.quaternary};
        }
    }

    ${props => props.theme.type === 'classic' && css`
        .classicBtn {
            pointer-events: none;
        }
    `}
    ${props => props.theme.type === 'dark' && css`
        .darkBtn {
            pointer-events: none;
        }
    `}
`;

export const ContentLink = styled.a.attrs((props) => ({
    target: '_blank',
    children: (props.href ? props.children : ([...props.children,<Caret_Down key={props.children.length + 1}/>]))
}))`
    width: inherit;
    min-height: 36px;
    display: flex;
    flex-direction: row;
    margin-bottom: 12px;
    align-items: center;
    text-decoration: none;
    user-select: none;
    cursor: pointer;
    font-size: 22px;
    
    h1 {
        font-size: 1em;
        line-height: 1.1em;
        font-weight: 500;
        color: ${props => props.theme.quaternary};
        text-align: left;
        width: 100%;
    }

    svg:not(:last-child) {
        max-width: 30px;
        max-height: inherit;
        margin-right: 10px;
        fill: ${props => props.theme.primary};
        color: ${props => props.theme.primary};
    }
    svg:last-child {
        transform: rotate(-90deg);
        height: 1em;
        fill: ${props => props.theme.quaternary};
    }
`;

export const ReturnMainPage = styled.button.attrs(() => ({
    children: (<>
        <Caret_Down/>
        <h1>Return</h1>    
    </>)
}))`
    font-size: 22px;
    margin: 15px 0;
    display: flex;
    flex-direction: row;
    align-items: center;
    align-self: flex-start;
    

    h1 {
        font-size: 1em;
        font-weight: 500;
        margin-left: 10px;
        color: ${props => props.theme.quaternary};
    }
    
    svg {
        width: 0.9em;
        transform: rotate(90deg);
        fill: ${props => props.theme.quaternary};
    }
`;