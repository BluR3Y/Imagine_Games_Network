CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Gallery
CREATE TABLE galleries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
);

-- Image
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    legacy_url VARCHAR(128),
    url VARCHAR(256),
    link VARCHAR(128),
    caption TEXT,
    embargo_date TIMESTAMP
);

-- Image_Connections: Used with Content
CREATE TABLE image_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID NOT NULL,
    gallery_id UUID NOT NULL,

    FOREIGN KEY (image_id) REFERENCES images(id),
    FOREIGN KEY (gallery_id) REFERENCES galleries(id)
);

-- Attribute Item
CREATE TABLE attributes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id INT,
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