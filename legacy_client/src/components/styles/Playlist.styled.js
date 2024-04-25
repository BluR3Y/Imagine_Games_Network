import styled, { css } from "styled-components";

import {deviceSizes} from './breakPoints';
import { TheaterModeBtn, StyledVideoPlayer } from "./VideoPlayer.styled";
import Comment from '../../assets/icons/comment';

export const StyledPlaylist = styled.div`
    flex: 1 1 auto;
    position: relative;
    display: grid;
    padding: 20px;
    margin: auto;
    grid-template-columns: auto;
    grid-template-rows: repeat(4, auto);
    grid-row-gap: 4px;
    grid-column-gap: 0px;

    h1,
    h2,
    p,
    li {
        color: ${props => props.theme.text};
    }
    
    ${StyledVideoPlayer} {
        grid-column: 1;
        grid-row: 1;
    }
    .videoInfo {
        font-size: 18px;
        grid-column: 1;
        grid-row: 2;
        padding: 20px 0;
        h1 {
            font-size: 1.6em;
            line-height: 1em;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 1.2em;
            font-weight: 500;
            margin-bottom: 20px;
            display: inline-block;
        }
        p {
            font-size: 1em;
            line-height: 1.4em;
            margin-bottom: 15px;
        }
    }
    
    @media (min-width: ${deviceSizes.minDesktop}px) {
        grid-template-columns: 660px 1fr;
        grid-template-rows: repeat(3, auto);
        grid-column-gap: 25px;

        ${props => props.theaterMode && css`
            padding: 0;
            ${StyledVideoPlayer} {
                max-height: 72vh;
                grid-column: 1 / -1;
                grid-row: 1;
                margin: 0;
                border-radius: 0;
            }

            .videoInfo {
                gird-column: 1;
                grid-row: 2;
                margin-left: 30px;
            }
        `}
    }

    @media (min-width: ${deviceSizes.xlScreens}px) {
        grid-template-columns: 1fr 450px;
        ${props => !props.theaterMode && css `
            padding: 20px 100px;
        `}
    }

    /* Needs Modification */
`;

export const CommentCount = styled.div.attrs((props) => ({
    children: (<>
        <Comment/>
        <h1>{props.count}</h1>
    </>)
}))`
    height: 26px;
    display: flex;
    flex-direction: row;
    float: right;
    align-items: center;
    user-select: none;

    svg {
        height: inherit;
        fill: ${props => props.theme.text};
        margin-right: 7px;
    }
    h1 {
        font-size: 1.1em !important;
        font-weight: lighter !important;
        margin-top: 15px;
    }
`;

export const VideoTags = styled.ul`
    list-style-type: none;
    display: flex;
    flex-direction: row;
    width: inherit;
    flex-wrap: wrap;
    justify-content: flex-start;
    user-select: none;

    li {
        background-color: ${props => props.theme.type === 'classic' ? props.theme.tertiary : props.theme.secondary};
        display: block;
        width: fit-content;
        border-radius: 14px;
        padding: 0 10px;
        text-transform: uppercase;
        font-size: 0.9em;
        margin: 5px 10px 5px 0;
    }
`;