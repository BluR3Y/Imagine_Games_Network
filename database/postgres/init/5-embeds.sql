-- Poll Configuration
CREATE TABLE poll_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    require_authentication BOOLEAN,
    require_authentication_for_results BOOLEAN,
    multi_choice BOOLEAN,
    auto_display_results BOOLEAN
);

-- Poll Object
CREATE TABLE polls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    content_id UUID,
    configuration_id UUID,
    image UUID,
    voters INT,

    FOREIGN KEY (content_id) REFERENCES contents (id),
    FOREIGN KEY (configuration_id) REFERENCES poll_configurations (id),
    FOREIGN KEY (image) REFERENCES images (id)
);

-- Poll Answer
CREATE TABLE poll_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    poll_id UUID NOT NULL,
    legacy_id INT,
    answer TEXT,
    votes INT,

    FOREIGN KEY (poll_id) REFERENCES polls (id)
);