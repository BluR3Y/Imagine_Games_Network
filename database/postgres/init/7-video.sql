-- Video Metadata
CREATE TABLE video_metadatas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ad_breaks BOOLEAN,
    chat_enabled BOOLEAN,
    description_html TEXT,
    downloadable BOOLEAN,
    duration INT,
    m3u_url VARCHAR(256)
);

-- Video
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    content_id UUID NOT NULL,
    metadata_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (metadata_id) REFERENCES video_metadatas (id)
);

-- Video Asset
CREATE TABLE video_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metadata_id UUID NOT NULL,
    url VARCHAR(256),
    width INT,
    height INT,
    fps INT,

    FOREIGN KEY (metadata_id) REFERENCES video_metadatas (id)
);

-- Video Caption
CREATE TABLE video_captions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metadata_id UUID NOT NULL,

    language VARCHAR(128),
    text TEXT,

    FOREIGN KEY (metadata_id) REFERENCES video_metadatas (id)
);