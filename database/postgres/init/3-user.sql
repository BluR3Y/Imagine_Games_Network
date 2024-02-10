-- Socials Type
CREATE TYPE social_media_entry AS (
    name VARCHAR(50),
    handler VARCHAR(100)
);

-- Contributor
CREATE TABLE contributors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    legacy_author_id INT,
    url VARCHAR(256),
    cover UUID,
    position VARCHAR(128),
    bio VARCHAR(256),
    location VARCHAR(128),
    socials social_media_entry[] DEFAULT '{}'::social_media_entry[],
    
    FOREIGN KEY (cover) REFERENCES images(id)
);

-- User Configuration : Missing
-- User Configuration
CREATE TABLE user_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
);

-- User
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    contributor_id UUID,
    avatar UUID,
    name VARCHAR(128),
    nickname VARCHAR(128),
    privacy_configuration UUID,

    FOREIGN KEY (contributor_id) REFERENCES contributors (id),
    FOREIGN KEY (avatar) REFERENCES images (id),
    FOREIGN KEY (privacy_configuration) REFERENCES user_configurations (id)
);