-- How Long To Beat
CREATE TABLE how_long_to_beat (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    legacy_ign_object_id UUID,
    steam_id INT,
    itch_id VARCHAR(8),
    platforms TEXT,
    list JSON,
    review JSON,
    time JSON
);

-- Object Name Entry
CREATE TYPE name_entry AS (
    long VARCHAR(128),
    alt VARCHAR(128)[],
    short VARCHAR(128)
);

-- Object Description Entry
CREATE TYPE description_entry AS (
    long TEXT,
    short TEXT
);

-- Object
CREATE TABLE objects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    url VARCHAR(64),
    slug VARCHAR(64),
    wiki_slug VARCHAR(64),
    how_long_to_beat_id UUID,
    type VARCHAR(16),
    cover_id UUID,
    gallery_id UUID,
    names name_entry,
    descriptions description_entry,
    -- Missing franchises, genres, etc

    FOREIGN KEY (how_long_to_beat_id) REFERENCES how_long_to_beat(id),
    FOREIGN KEY (cover_id) REFERENCES images(id),
    FOREIGN KEY (gallery_id) REFERENCES galleries(id)
);
-- franchises, genres, features, producers, publishers will be Type_Attribute entries

-- Object Attributes Connection
CREATE TABLE object_attribute_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    object_id UUID NOT NULL,
    attribute_id UUID NOT NULL,

    FOREIGN KEY (object_id) REFERENCES objects(id),
    FOREIGN KEY (attribute_id) REFERENCES typed_attributes(id)
);

-- Object Age Rating
CREATE TABLE age_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    type VARCHAR(16),
    name VARCHAR(64),
    slug VARCHAR(64)
);

-- Region Object
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
    object_id UUID NOT NULL,
    name VARCHAR(64),
    region VARCHAR(32),
    age_rating_id UUID,

    FOREIGN KEY (object_id) REFERENCES objects (id),
    FOREIGN KEY (age_rating_id) REFERENCES age_ratings (id)
);

-- Age Rating Descriptors
CREATE TABLE age_rating_descriptors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID NOT NULL,
    attribute_id UUID NOT NULL,

    FOREIGN KEY (region_id) REFERENCES regions (id),
    FOREIGN KEY (attribute_id) REFERENCES attributes (id)
);

-- Age Rating Interactive Elements
CREATE TABLE age_rating_interactive_elements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID NOT NULL,
    attribute_id UUID NOT NULL,

    FOREIGN KEY (region_id) REFERENCES regions (id),
    FOREIGN KEY (attribute_id) REFERENCES attributes (id)
);

-- Region Release
CREATE TABLE releases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    date TIMESTAMP,
    estimated_date BOOLEAN,
    time_frame_year VARCHAR(32)
);
-- Platform attributes will be Typed_Attribute entries

-- Release Platform Attributes
CREATE TABLE release_platform_attributes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    release_id UUID NOT NULL,
    attribute_id UUID NOT NULL,
    FOREIGN KEY (release_id) REFERENCES releases (id),
    FOREIGN KEY (attribute_id) REFERENCES attributes (id)
);