-- Object Name Entry
CREATE TYPE name_entry AS (
    main VARCHAR(128),
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
    how_long_to_beat JSON,
    type VARCHAR(16),
    cover UUID,
    gallery_id UUID,
    names name_entry,
    descriptions description_entry,
    -- Missing franchises, genres, etc

    FOREIGN KEY (cover) REFERENCES images(id),
    FOREIGN KEY (gallery_id) REFERENCES albums(id)
);
-- franchises, genres, features, producers, publishers will be Type_Attribute entries

-- Object Age Rating
CREATE TABLE age_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    type VARCHAR(16),
    name VARCHAR(64),
    slug VARCHAR(64)
);
-- rating descriptors/interactive elements need to include Age_Rating id as foreign key
-- rating descriptors/interactive elements will be Typed_Attribute entries

-- Region Object
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    name VARCHAR(64),
    region VARCHAR(32),
    age_rating_id UUID,

    FOREIGN KEY (age_rating_id) REFERENCES age_ratings (id)
);

-- Region Release
CREATE TABLE releases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    date TIMESTAMP,
    estimated_date TIMESTAMP,
    time_frame_year TIMESTAMP
);
-- Platform attributes will be Typed_Attribute entries

-- Wiki Object
CREATE TABLE wiki_objects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    name VARCHAR(128)
);

-- Wiki Navigation
CREATE TABLE wiki_navigations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wiki_object_id UUID NOT NULL,
    label VARCHAR(64),
    url VARCHAR(128),

    FOREIGN KEY (wiki_object_id) REFERENCES wiki_objects (id)
);

-- Map Object
CREATE TABLE map_objects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    wiki_object_id UUID NOT NULL,

    FOREIGN KEY (wiki_object_id) REFERENCES wiki_objects (id)
);

-- Map Item
CREATE TABLE maps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    map_object_id UUID NOT NULL,
    name VARCHAR(256),
    slug VARCHAR(256),
    cover UUID,
    width INT,
    height INT,
    map_type VARCHAR(128),
    initial_zoom INT,
    min_zoom INT,
    max_zoom INT,
    initial_latitude DECIMAL(10, 2), -- 10 total digits, 2 decimal places
    initial_longitude DECIMAL(10, 2),
    marker_count INT,
    map_genie_game_id INT,
    tile_sets VARCHAR(64)[],
    background_color VARCHAR(64),

    FOREIGN KEY (map_object_id) REFERENCES map_objects (id),
    FOREIGN KEY (cover) REFERENCES images (id)
);