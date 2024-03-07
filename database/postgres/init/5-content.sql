-- Brand
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    slug VARCHAR(32),
    name VARCHAR(64),
    logo_light VARCHAR(16),
    logo_dark VARCHAR(16)
);

-- Content Category
CREATE TABLE content_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    name VARCHAR(32)
);

-- Content
CREATE TABLE contents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    url VARCHAR(128),
    slug VARCHAR(128),
    type VARCHAR(16),
    vertical VARCHAR(16),
    header_image_id UUID,
    title TEXT,
    subtitle TEXT,
    feed_title TEXT,
    feed_image_id UUID,
    primary_object_id UUID,
    excerpt TEXT,
    description TEXT,
    state VARCHAR(16),
    publish_date TIMESTAMP,
    modify_date TIMESTAMP,
    events VARCHAR(32)[],
    brand_id UUID,
    category_id UUID,

    FOREIGN KEY (header_image_id) REFERENCES images (id),
    FOREIGN KEY (feed_image_id) REFERENCES images (id),
    FOREIGN KEY (primary_object_id) REFERENCES objects (id),
    FOREIGN KEY (brand_id) REFERENCES brands (id),
    FOREIGN KEY (category_id) REFERENCES content_categories (id)
);

CREATE TABLE object_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    object_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (object_id) REFERENCES objects (id)
);

-- Author connections to content
CREATE TABLE contributors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    user_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Attribute Connection
CREATE TABLE content_attribute_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    attribute_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (attribute_id) REFERENCES typed_attributes (id)
);

-- Slideshow
CREATE TABLE slideshows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    gallery_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents(id),
    FOREIGN KEY (gallery_id) REFERENCES galleries(id)
);

-- Official Review
CREATE TABLE official_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    score INT,
    score_text TEXT,
    editors_choice BOOLEAN,
    score_summary TEXT,
    article_url VARCHAR(256),
    video_url VARCHAR(256),
    review_date TIMESTAMP
);

-- User Review
CREATE TABLE user_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    user_id UUID NOT NULL,
    legacy_user_id UUID,
    object_id UUID NOT NULL,
    legacy_object_id UUID,
    is_liked BOOLEAN,
    score INT,
    text TEXT,
    is_spoiler BOOLEAN,
    is_private BOOLEAN,
    publish_date TIMESTAMP,
    modify_date TIMESTAMP,
    platform_id UUID,

    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (object_id) REFERENCES objects (id),
    FOREIGN KEY (platform_id) REFERENCES attributes (id)
);

-- Tag Object
-- CREATE TABLE tag_objects (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     legacy_id INT,
--     name VARCHAR(128) NOT NULL
-- );

-- Review Tag
CREATE TABLE review_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    review_id UUID NOT NULL,
    attribute_id UUID NOT NULL,
    is_positive BOOLEAN,

    FOREIGN KEY (review_id) REFERENCES user_reviews (id),
    FOREIGN KEY (attribute_id) REFERENCES attributes (id)
);