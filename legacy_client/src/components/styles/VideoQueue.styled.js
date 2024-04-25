import styled, { css } from "styled-components";
import { deviceSizes } from "./breakPoints";

export const StyledQueueVideo = styled.div`
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: 100px auto;
    grid-gap: 10px;
    font-size: 0.8em;
    text-decoration: none;

    .previewPlayer {
        width: inherit;
        background-color: black;
        aspect-ratio: 16 / 9;
        grid-column: 1;
        grid-row: 1;
        border-radius: 6px;
        overflow: hidden;
        position: relative;

        .playerThumbnail {
            
        }
    }

    .contentInfo {
        grid-column: 2;
        grid-row: 1;
        font-size: 1em;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 5px;

        h1 {
            font-size: 0.95em;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            text-overflow: ellipsis;
            overflow: hidden;
            -webkit-box-orient: vertical;
        }
        h2 {
            font-weight: 400;
            font-size: 0.9em;

            display: -webkit-box;
            -webkit-line-clamp: 2;
            text-overflow: ellipsis;
            overflow: hidden;
            -webkit-box-orient: vertical;
        }
    }

    .additionalContentInfo {
        grid-column: 1 / -1;
        grid-row: 2;
        display: flex;
        flex-direction: row;
        font-size: 1em;
        gap: 25px;
        overflow: hidden;

        div {
            font-size: 0.8em;
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 5px;
            overflow: hidden;
            white-space: nowrap;

            svg {
                fill: ${props => props.theme.tertiary};
                height: 1.2em;
            }
            h1 {
                font-size: 0.9em;
                line-height: 1.8em;
                color: ${props => props.theme.tertiary};
            }
        }
    }

    @media (min-width: ${deviceSizes.minTablet}px) {
        grid-template-columns: 180px 1fr;
        grid-template-rows: auto auto;
        grid-row-gap: 5px;

        .previewPlayer {
            grid-column: 1;
            grid-row: 1 / -1;
        }

        .contentInfo {
            align-self: flex-end;
        }

        .additionalContentInfo {
            grid-column: 2;
            align-self: flex-start;
        }
    }
    
    @media (min-width: ${deviceSizes.minDesktop}px) {
        grid-template-columns: auto 1fr;
        grid-template-rows: 90px auto;

        .previewPlayer {
            grid-column: 1;
            grid-row: 1;
        }

        .contentInfo {
            align-self: unset;
        }

        .additionalContentInfo {
            grid-column: 1 / -1;
            align-self: unset;
        }
    }
`;

export const StyledVideoQueue = styled.div`
    display: flex;
    flex-direction: column;
    padding: 0;
    font-size: 1em;
    justify-content: center;
    gap: 10px;
    grid-column: 1;
    grid-row: 3;
    border: 1px solid red;
    position: relative;

    .contentWrapper {
        flex: 1 1 0;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        gap: 15px;

        ${StyledQueueVideo}:not(:last-child) {
            border-bottom: 1px solid ${props => props.theme.tertiary};
            padding-bottom: 15px;
        }
    }

    .extendList {
        flex: 0 0 30px;
        width: 100%;
        background-color: ${props => props.theme.primary};
        border-radius: 5px;
        color: ${props => props.theme.tertiary};
        position: absolute;
        bottom: -35px;
        left: 50%;
        transform: translate(-50%);
    }

    @media (min-width: ${deviceSizes.minDesktop}px) {
        grid-column: 2;
        ${props => props.inTheaterMode ? css`
            grid-row: 2 / -1;
        ` : css`
            ${props.extendedList ? css`
                grid-row: 1 / -1;
            ` : css`
                grid-row: 1;
            `}
        `}

        .contentWrapper {
            gap: 5px;
            ${StyledQueueVideo}:not(:last-child) {
                padding-bottom: 5px;
            }
        }
    }
`;