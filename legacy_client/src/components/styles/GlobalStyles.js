import { createGlobalStyle } from "styled-components"

import LatoRegular from '../../assets/fonts/Lato/Lato-Regular.ttf';
import LatoBlack from '../../assets/fonts/Lato/Lato-Black.ttf';
import LatoBold from '../../assets/fonts/Lato/Lato-Bold.ttf';

import PoppinsRegular from '../../assets/fonts/Poppins/Poppins-Regular.ttf';
import PoppinsBlack from '../../assets/fonts/Poppins/Poppins-Black.ttf';
import PoppinsBold from '../../assets/fonts/Poppins/Poppins-Bold.ttf';
import PoppinsMedium from '../../assets/fonts/Poppins/Poppins-Medium.ttf';

const GlobalStyles = createGlobalStyle`
    @font-face {
        font-family: 'Lato';
        font-weight: 900;
        src: local('Lato'), url(${LatoBlack}) format('truetype');
    }
    @font-face {
        font-family: 'Lato';
        font-weight: 400;
        src: local('Lato'), url(${LatoRegular}) format('truetype');
    }
    @font-face {
        font-family: 'Lato';
        font-weight: 700;
        src: local('Lato'), url(${LatoBold}) format('truetype');
    }

    @font-face {
        font-family: 'Poppins';
        font-weight: 900;
        src: local('Poppins'), url(${PoppinsBlack}) format('truetype');
    }
    @font-face {
        font-family: 'Poppins';
        font-weight: 400;
        src: local('Poppins'), url(${PoppinsRegular}) format('truetype');
    }
    @font-face {
        font-family: 'Poppins';
        font-weight: 700;
        src: local('Poppins'), url(${PoppinsBold}) format('truetype');
    }
    @font-face {
        font-family: 'Poppins';
        font-weight: 500;
        src: local('Poppins'), url(${PoppinsMedium}) format('truetype');
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html,
    body,
    #root {
        height: 100%;
    }

    body {
        font-family: 'Poppins', sans-serif;
        font-size: 1.15em;
        background-color: ${props => props.theme.background};
    }

    #root {
        display: flex;
        flex-direction: column;
    }

    svg {
        display: block;
    }

    input:focus,
    select:focus,
    textarea:focus,
    button:focus {
        outline: none;
    }

    button, input[type="submit"], input[type="reset"] {
        background: none;
        color: inherit;
        border: none;
        padding: 0;
        font: inherit;
        cursor: pointer;
        outline: inherit;
    }
`;

export default GlobalStyles;