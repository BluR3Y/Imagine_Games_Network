
-- Content
CREATE TABLE content_types (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO content_types (`name`) VALUES
    ('video'),
    ('article'),
    ('audio')
;

-- Entertainment
CREATE TABLE entertainment_categories (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO entertainment_categories (`name`) VALUES
    ('video_game'),
    ('movie'),
    ('show'),
    ('comic'),
    ('tech')
;

SELECT id INTO @video_game_category_id FROM entertainment_categories WHERE name = 'video_game';
SELECT id INTO @movie_category_id FROM entertainment_categories WHERE name = 'movie';
SELECT id INTO @show_category_id FROM entertainment_categories WHERE name = 'show';
SELECT id INTO @comic_category_id FROM entertainment_categories WHERE name = 'comic';
SELECT id INTO @tech_category_id FROM entertainment_categories WHERE name = 'tech';

CREATE TABLE entertainment_genres (
    `id` INT(6) NOT NULL AUTO_INCREMENT,
    `category_id` INT(6) NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`category_id`) REFERENCES entertainment_categories (`id`)
);
INSERT INTO entertainment_genres (`category_id`, `name`) VALUES
    (@video_game_category_id, 'action'),
    (@video_game_category_id, 'rpg'),
    (@video_game_category_id, 'simulation'),
    (@video_game_category_id, 'puzzle'),
    (@video_game_category_id, 'adventure'),
    (@video_game_category_id, 'sports'),
    (@video_game_category_id, 'shooter'),
    (@video_game_category_id, 'racing'),
    (@video_game_category_id, 'pinball'),
    (@video_game_category_id, 'strategy'),
    (@video_game_category_id, 'platformer'),
    (@video_game_category_id, 'board_game'),
    (@video_game_category_id, 'educational'),
    (@video_game_category_id, 'compilation'),
    (@video_game_category_id, 'mmo'),
    (@video_game_category_id, 'fighting'),
    (@video_game_category_id, 'card'),
    (@video_game_category_id, 'hidden_object'),
    (@video_game_category_id, 'casino'),
    (@video_game_category_id, 'viral_pet'),
    (@video_game_category_id, 'party'),
    (@video_game_category_id, 'productivity'),
    (@video_game_category_id, 'music'),
    (@video_game_category_id, 'arcade'),
    (@video_game_category_id, 'horror'),
    (@video_game_category_id, 'survival'),
    (@video_game_category_id, 'battle_royale'),
    (@video_game_category_id, 'other'),

    (@movie_category_id, 'comedy'),
    (@movie_category_id, 'romance'),
    (@movie_category_id, 'adventure'),
    (@movie_category_id, 'documentary'),
    (@movie_category_id, 'action'),
    (@movie_category_id, 'horror'),
    (@movie_category_id, 'drama'),
    (@movie_category_id, 'sports'),
    (@movie_category_id, 'musical'),
    (@movie_category_id, 'animation'),
    (@movie_category_id, 'family'),
    (@movie_category_id, 'thriller'),
    (@movie_category_id, 'science_fiction'),
    (@movie_category_id, 'crime'),
    (@movie_category_id, 'war'),
    (@movie_category_id, 'mystery'),
    (@movie_category_id, 'film_noir'),
    (@movie_category_id, 'fantasy'),
    (@movie_category_id, 'short_form'),
    (@movie_category_id, 'anime'),
    (@movie_category_id, 'other'),

    (@show_category_id, 'game_show'),
    (@show_category_id, 'reality'),
    (@show_category_id, 'anime'),
    (@show_category_id, 'crime'),
    (@show_category_id, 'comedy'),
    (@show_category_id, 'action'),
    (@show_category_id, 'adventure'),
    (@show_category_id, 'drama'),
    (@show_category_id, 'science_fiction'),
    (@show_category_id, 'animation'),
    (@show_category_id, 'sports'),
    (@show_category_id, 'news'),
    (@show_category_id, 'food'),
    (@show_category_id, 'horror'),
    (@show_category_id, 'documentary'),
    (@show_category_id, 'soap_opera'),
    (@show_category_id, 'fantasy'),
    (@show_category_id, 'other'),

    (@comic_category_id, 'science_fiction'),
    (@comic_category_id, 'action'),
    (@comic_category_id, 'manga'),
    (@comic_category_id, 'fantasy'),
    (@comic_category_id, 'adult'),
    (@comic_category_id, 'horror'),
    (@comic_category_id, 'graphic_novel'),
    (@comic_category_id, 'personal_comic'),
    (@comic_category_id, 'comedy'),
    (@comic_category_id, 'adventure'),
    (@comic_category_id, 'superhero'),
    (@comic_category_id, 'other'),

    (@tech_category_id, 'ear_buds'),
    (@tech_category_id, 'headset'),
    (@tech_category_id, 'controller'),
    (@tech_category_id, 'keyboard'),
    (@tech_category_id, 'laptop'),
    (@tech_category_id, 'mini_pc'),
    (@tech_category_id, 'display'),
    (@tech_category_id, 'mouse'),
    (@tech_category_id, 'streaming_device'),
    (@tech_category_id, 'cellphone'),
    (@tech_category_id, 'tablet'),
    (@tech_category_id, 'graphics_card'),
    (@tech_category_id, 'console'),
    (@tech_category_id, 'video_projector'),
    (@tech_category_id, 'microphone'),
    (@tech_category_id, 'watch'),
    (@tech_category_id, 'augmented_reality_device'),
    (@tech_category_id, 'arcade'),
    (@tech_category_id, 'mouse_pad'),
    (@tech_category_id, 'smartphone'),
    (@tech_category_id, 'gaming_laptop'),
    (@tech_category_id, 'gaming_headset'),
    (@tech_category_id, 'gaming_keyboard'),
    (@tech_category_id, 'gaming_pc'),
    (@tech_category_id, 'gaming_display'),
    (@tech_category_id, 'gaming_mouse'),
    (@tech_category_id, 'gaming_mousepad'),
    (@tech_category_id, 'gaming_chair'),
    (@tech_category_id, 'gaming_chair'),
    (@tech_category_id, 'other')
;