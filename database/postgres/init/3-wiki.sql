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
    cover_id UUID,
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
    FOREIGN KEY (cover_id) REFERENCES images (id)
);