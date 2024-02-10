-- Companies
CREATE TABLE companies (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `parent_id` INT(6),
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
);
-- Parent Companies
INSERT INTO companies (`name`) VALUES
    ('apple'),
    ('samsung'),
    ('microsoft'),
    ('sony'),
    ('nintendo'),
    ('sega'),
    ('valve')
;

SELECT id INTO @apple_company_id FROM companies WHERE name = 'apple';
SELECT id INTO @samsung_company_id FROM companies WHERE name = 'samsung';
SELECT id INTO @microsoft_company_id FROM companies WHERE name = 'microsoft';
SELECT id INTO @sony_company_id FROM companies WHERE name = 'sony';
SELECT id INTO @nintendo_company_id FROM companies WHERE name = 'nintendo';
SELECT id INTO @sega_company_id FROM companies WHERE name = 'sega';
SELECT id INTO @valve_company_id FROM companies WHERE name = 'valve';

-- Subsidiary Companies
INSERT INTO companies (`parent_id`, `name`) VALUES
    (@sony_company_id, 'sony interactive entertainment'),
    (@microsoft_company_id, 'xbox')
;

SELECT id INTO @xbox_subsidiary_id FROM companies WHERE name = 'xbox' AND parent_id = @microsoft_company_id;
SELECT id INTO @sony_subsidiary_id FROM companies WHERE name = 'sony interactive entertainment' AND parent_id = @sony_company_id;

-- Industries
CREATE TABLE industries (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO industries (`name`) VALUES
    ('conglomerate'),
    ('consumer electronics'),
    ('software services'),
    ('online services'),
    ('information technology'),
    ('video games'),
    ('entertainment'),
    ('digital distribution')
;

SELECT id INTO @conglomerate_industry_id FROM industries WHERE name = 'conglomerate';
SELECT id INTO @consumer_electronics_industry_id FROM industries WHERE name = 'consumer electronics';
SELECT id INTO @software_services_industry_id FROM industries WHERE name = 'software services';
SELECT id INTO @online_services_industry_id FROM industries WHERE name = 'online services';
SELECT id INTO @information_technology_industry_id FROM industries WHERE name = 'information technology';
SELECT id INTO @video_games_industry_id FROM industries WHERE name = 'video games';
SELECT id INTO @entertainment_industry_id FROM industries WHERE name = 'entertainment';
SELECT id INTO @digital_distribution_industry_id FROM industries WHERE name = 'digital distribution';

-- Company Industries
CREATE TABLE company_industries (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `company_id` INT NOT NULL,
    `industry_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`company_id`) REFERENCES companies (`id`),
    FOREIGN KEY (`industry_id`) REFERENCES industries (`id`)
);
INSERT INTO company_industries (`company_id`, `industry_id`) VALUES
    (@apple_company_id, @consumer_electronics_industry_id),
    (@apple_company_id, @software_services_industry_id),
    (@apple_company_id, @online_services_industry_id),
    (@samsung_company_id, @conglomerate_industry_id),
    (@microsoft_company_id, @information_technology_industry_id),
    (@sony_company_id, @conglomerate_industry_id),
    (@nintendo_company_id, @video_games_industry_id),
    (@nintendo_company_id, @consumer_electronics_industry_id),
    (@sega_company_id, @entertainment_industry_id),
    (@valve_company_id, @video_games_industry_id),
    (@valve, @digital_distribution_industry_id)
;

-- Brands
CREATE TABLE brands (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `company_id` INT(6) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `industry` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO brands (`company_id`, `name`, `industry`) VALUES
    ('xbox'),
    ('playstation'),
    ('')
;