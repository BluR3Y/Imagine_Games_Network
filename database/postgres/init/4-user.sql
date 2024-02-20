-- User
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    avatar_id UUID,
    name VARCHAR(128),
    nickname VARCHAR(128),

    FOREIGN KEY (avatar_id) REFERENCES images (id)
);

-- Socials Type
CREATE TYPE social_media_entry AS (
    platform VARCHAR(50),
    username VARCHAR(100)
);

-- Author
CREATE TABLE authors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    user_id UUID NOT NULL,
    url VARCHAR(256),
    cover_id UUID,
    position VARCHAR(128),
    bio VARCHAR(256),
    location VARCHAR(128),
    socials social_media_entry[] DEFAULT '{}'::social_media_entry[],
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (cover_id) REFERENCES images(id)
);

CREATE TYPE privacy_type AS ENUM ('public', 'private');

CREATE TABLE user_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    privacy privacy_type NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id)
);