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

-- Catalog
CREATE TABLE catalogs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,

    FOREIGN KEY (content_id) REFERENCES contents(id)
);

-- Commerce Deal
CREATE TABLE commerce_deals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    legacy_id UUID,
    url VARCHAR(128),
    title TEXT,
    description TEXT,
    brand VARCHAR(32),
    model VARCHAR(64),
    vendor VARCHAR(64),
    price NUMERIC(10, 2),
    msrp NUMERIC(10, 2),
    discount NUMERIC(10, 2),
    coupon_code VARCHAR(16),
    sponsor_disclosure VARCHAR(128),
    is_large BOOLEAN,
    region_code VARCHAR(4),
    up_votes INT,
    cover_id UUID,

    FOREIGN KEY (cover_id) REFERENCES images(id)
);

-- Deal Connection
CREATE TABLE deal_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deal_id UUID NOT NULL,
    catalog_id UUID NOT NULL,

    FOREIGN KEY (deal_id) REFERENCES commerce_deals(id),
    FOREIGN KEY (catalog_id) REFERENCES catalogs(id)
);