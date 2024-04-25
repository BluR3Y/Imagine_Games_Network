import styled from "styled-components";
import { deviceSizes } from "./breakPoints";

export const StyledCommentSection = styled.div`
    grid-column: 1;
    grid-row: 4;

    @media (min-width: ${deviceSizes.minDesktop}px) {
        grid-row: 3;
    }

    border: 1px solid yellow;
`;