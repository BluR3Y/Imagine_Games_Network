import styled from "styled-components";


export const StyledSearchBar = styled.form`
    height: 30px;
    width: 30px;
    position: relative;
    flex: ${props => props.open ? '1 1 0' : '0 0 0'};
    transition: flex 0.4s linear;

    .searchForm {
        height: inherit;
        display: flex;
        flex-direction: row;
        overflow: hidden;
        border-radius: ${props => !props.emptyAutoComplete && props.searchInputFocused ? '8px 8px 0 0 ' : '20px'};
        background-color: ${props => props.open ? props.theme.tertiary : 'transparent'};
        transition: background-color 0.4s ease;

        button {
            flex: 0 0 30px;
            height: 30px;
            border: none;
            border-radius: ${props => !props.emptyAutoComplete && props.searchInputFocused ? '8px' : '50%'};
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: transparent;
            cursor: pointer;

            svg {
                width: 20px;
                fill: ${props => props.theme.quaternary};
            }
        }
        button:hover {
            background-color: ${props => props.theme.primary};
        }

        input {
            flex: 1;
            border: none;
            font-size: 16px;
            padding: 0 5px;
            background: transparent;
        }
    }
    .searchAutoComplete {
        display: ${props => props.searchInputFocused ? 'block' : 'none'};
        position: absolute;
        top: 100%;
        width: 100%;
        border-radius: 0 0 8px 8px;
        overflow: hidden;
        background-color: ${props => props.theme.tertiary};
    }
`;

export const StyledAutoCompleteGame = styled.div.attrs(() => ({
    tabIndex: 0,
}))`
    display: ${props => props.isLoaded ? 'flex' : 'none'};
    flex-direction: row;
    align-items: center;
    cursor: pointer;
    height: 50px;

    &:hover {
        background-color: ${props => props.theme.primary};
    }

    .AutoComplete-Img {
        flex: 0 0 40px;
        height: 40px;
        border-radius: 8px;
        margin: 0 10px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;

        img { 
            flex: 1 0 auto;
            height: inherit;
            object-fit: fill;
        }
        svg {
            width: 15px;
        }
    }
    .AutoComplete-Info {
        height: 40px;
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        padding-right: 5px;


        div {
            display: flex;
            flex-direction: row;
            align-items: center;

            svg {
                height: 16px;
                width: auto;
                fill: #fff;
                margin-right: 5px;
            }

            h1 {
                font-size: 18px;
                font-weight: 400;
                letter-spacing: -2px;
            }
        }
        h1 {
            width: inherit;
            font-size: 16px;
            font-weight: 500;
            line-height: 18px;
            cursor: pointer;
            white-space: nowrap;
            margin: auto 0;
        }
    }
`;

export const StyledAutoCompleteMovie = styled(StyledAutoCompleteGame)`
    display: ${props => props.isLoaded ? 'flex' : 'none'};
    height: 60px;

    & .AutoComplete-Img {
        height: 50px;
        border-radius: 4px;
    }
    & .AutoComplete-Info {
        flex: 1;
        height: inherit;
        padding: 5px 0;
        justify-content: space-around !important;

        h1 {
            font-size: 16px;
        }
        h2 {
            font-size: 14px;
            font-weight: 500;
        }
    }
`;

export const StyledLoadingAutoCompleteItem = styled.div.attrs(props => ({
    children: (<>
        <div/>
        <div>
            <div/>
            <div/>
        </div>
    </>)
}))`
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 50px;
    background-color: #383434;

    & > div:nth-child(1) {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        margin: 0 10px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(-45deg, #9c9996, #9cabab, #919191, #747372);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    & > div:nth-child(2) {
        flex: 1;
        height: inherit;
        display: flex;
        flex-direction: column;
        justify-content: center;
        
        div {
            border-radius: 8px;
            background: linear-gradient(-45deg, #9c9996, #9cabab, #919191, #747372);
            background-size: 400% 400%;
            animation: gradient 8s ease infinite;
        }

        div:nth-child(1) {
            height: 12px;
            width: 40%;
            margin-bottom: 7px;
        }
        div:nth-child(2) {
            height: 18px;
            width: 90%;
        }
    }

    @keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
	50% {
		background-position: 100% 50%;
	}
	100% {
		background-position: 0% 50%;
	}
}
`;