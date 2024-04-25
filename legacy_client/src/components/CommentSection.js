import React from "react";
import { StyledCommentSection } from "./styles/CommentSection.styled";

export default class CommentSection extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        }
    }

    render() {
        return <StyledCommentSection>
            Comment Section
        </StyledCommentSection>
    }
}