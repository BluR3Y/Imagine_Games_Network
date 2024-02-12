-- Album
CREATE TABLE albums (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
);

-- Image
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    url VARCHAR(128),
    caption TEXT,
    embargo_date TIMESTAMP
);

-- Image_Connections: Used with Content
CREATE TABLE image_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID NOT NULL,
    album_id UUID NOT NULL,

    FOREIGN KEY (image_id) REFERENCES images(id),
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

-- -- Poll Object
-- CREATE TABLE Poll (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     legacy_id UUID,
--     content_id UUID,
--     configuration_id UUID,
--     image UUID,
--     voters INT,

--     FOREIGN KEY (content_id) REFERENCES Content(id),
--     FOREIGN KEY (configuration_id) REFERENCES Poll_Configuration(id),
--     FOREIGN KEY (image) REFERENCES Image(id)
-- );

-- -- Poll Answer
-- CREATE TABLE Poll_Answer(
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     poll_id UUID NOT NULL,
--     legacy_id INT,
--     answer TEXT,
--     votes INT,

--     FOREIGN KEY (poll_id) REFERENCES Poll(id)
-- );

-- -- Poll Configuration
-- CREATE TABLE Poll_Configuration(
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     require_authentication BOOLEAN,
--     require_authentication_for_results BOOLEAN,
--     multi_choice BOOLEAN,
--     auto_display_results BOOLEAN
-- );