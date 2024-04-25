import styled, { css } from "styled-components";
import { deviceSizes } from "./breakPoints";

export const StyledArticleContentItem = styled.a.attrs((props) => ({
    href: 'https://ign.com' + props.contentUrl
}))`
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: 100px auto;
    grid-gap: 10px;
    font-size: 0.8em;
    text-decoration: none;

    .posterContainer {
        background-color: #000;
        grid-column: 1;
        grid-row: 1;
        aspect-ratio: 16 / 9;
        border-radius: 6px;
        overflow: hidden;

        img {
            height: 100%;
            width: 100%;
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
        grid-template-columns: 220px 1fr;
        grid-template-rows: auto auto;
        grid-row-gap: 5px;

        .posterContainer {
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
`;

export const StyledContentSelection = styled.div`
    display: flex;
    flex-direction: column;
    padding: 0;
    font-size: 1em;
    justify-content: center;
    gap: 10px;
    grid-column: 1;
    grid-row: 3;

    .typeSelection {
        flex: 0 0 40px;
        width: 300px;
        align-self: flex-start;
        display: flex;
        flex-direction: row;
        border-radius: 25px;
        font-size: 0.85em;
        gap: 4px;
    }

    .contentWrapper {
        flex: 1 1 0;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        gap: 1px;

        ${StyledArticleContentItem} {
            padding: 15px 0;
        }
        ${StyledArticleContentItem}:not(:last-child) {
            border-bottom: 1px solid ${props => props.theme.tertiary};
        }
    }

    .extendList {
        flex: 0 0 30px;
        background-color: ${props => props.theme.primary};
        border-radius: 5px;
        color: ${props => props.theme.tertiary};
    }

    @media (min-width: ${deviceSizes.minDesktop}px) {
        grid-column: 2;
        ${props => props.inTheaterMode ? css`
            grid-row: 2 / -1;
        ` : css`
            ${props.extendedContentList ? css`
                grid-row: 1 / -1;
            ` : css`
                grid-row: 1;
            `}
        `}

    }
`;

export const ContentSelectionBtn = styled.button`
    font-size: 1em;
    flex: 1 1 auto;
    text-transform: capitalize;
    color:  ${props => props.selected ? props.theme.secondary : props.theme.quaternary};
    background-color: ${props => props.selected ? props.theme.quaternary : props.theme.secondary};

    &:first-child {
        border-top-left-radius: inherit;
        border-bottom-left-radius: inherit;
    }
    &:last-child {
        border-top-right-radius: inherit;
        border-bottom-right-radius: inherit;
    }
    &:hover {
        background-color: ${props => props.theme.tertiary};
    }
`;

export const StyledVideoContentItem = styled(StyledArticleContentItem)`
    
`;

// export const StyledContentItem = styled.div`
//     height: 110px;
//     display: flex;
//     flex-direction: row;
//     background-color: ${props => props.theme.background};    
//     border: 1px solid black;
// `;