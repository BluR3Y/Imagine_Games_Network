-- Article Content
CREATE TABLE article_contents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    hero_video_content_id UUID,
    hero_video_content_slug VARCHAR(64),
    processed_html TEXT
);

-- Article
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    content_id UUID NOT NULL,
    article_content_id UUID NOT NULL,
    -- embeds Missing
    review_id UUID,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (article_content_id) REFERENCES article_contents (id),
    FOREIGN KEY (review_id) REFERENCES official_reviews (id)
);