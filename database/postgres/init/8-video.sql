-- Video Metadata
CREATE TABLE video_metadatas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_enabled BOOLEAN,
    description_html TEXT,
    downloadable BOOLEAN,
    duration NUMERIC(10, 2),
    m3u_url VARCHAR(512)
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
    video_id UUID NOT NULL,
    legacy_url VARCHAR(1024),
    key VARCHAR(1024),
    width INT,
    height INT,
    fps INT,

    FOREIGN KEY (video_id) REFERENCES videos (id)
);

-- Video Caption
CREATE TABLE video_captions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metadata_id UUID NOT NULL,

    language VARCHAR(128),
    text TEXT,

    FOREIGN KEY (metadata_id) REFERENCES video_metadatas (id)
);