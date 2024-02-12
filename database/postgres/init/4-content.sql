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
    legacy_id UUID,
    name VARCHAR(32)
);

-- Content
CREATE TABLE contents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    url VARCHAR(64),
    slug VARCHAR(64),
    type VARCHAR(16),
    vertical VARCHAR(16),
    cover UUID,
    title TEXT,
    subtitle TEXT,
    feed_title TEXT,
    feed_cover UUID,
    primary_object UUID NOT NULL,
    excerpt TEXT,
    description TEXT,
    state VARCHAR(16),
    publish_date TIMESTAMP,
    modify_date TIMESTAMP,
    events VARCHAR(32)[],
    brand UUID,
    category_id UUID,

    FOREIGN KEY (cover) REFERENCES images (id),
    FOREIGN KEY (feed_cover) REFERENCES images (id),
    FOREIGN KEY (primary_object) REFERENCES objects (id),
    FOREIGN KEY (brand) REFERENCES brands (id),
    FOREIGN KEY (category_id) REFERENCES content_categories (id)
);

CREATE TABLE object_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    object_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (object_id) REFERENCES objects (id)
);

CREATE TABLE contributor_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    contributor_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (contributor_id) REFERENCES users (id)
);

-- Attribute Item
CREATE TABLE attributes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(64),
    short_name VARCHAR(32),
    slug VARCHAR(32)
);

-- Typed Attribute
CREATE TABLE typed_attributes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(16) NOT NULL,
    attribute_id UUID NOT NULL,
    
    FOREIGN KEY (attribute_id) REFERENCES attributes (id)
);

CREATE TABLE attribute_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    attribute_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (attribute_id) REFERENCES typed_attributes (id)
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
    legacy_id UUID,
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

-- User Review Tag
CREATE TABLE user_review_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    name VARCHAR(128),
    is_positive BOOLEAN
);