USE imdb_clone;

CREATE TABLE
    IF NOT EXISTS movies (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        year YEAR,
        certificate VARCHAR(10),
        runtime_min SMALLINT,
        imdb_rating DECIMAL(3, 1),
        overview TEXT,
        metascore SMALLINT,
        votes INT,
        gross_usd BIGINT,
        poster_link VARCHAR(512),
        UNIQUE KEY uniq_title_year (title, year),
        INDEX idx_title (title)
    );

CREATE TABLE
    IF NOT EXISTS people (
        person_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS genres (
        genre_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS movie_cast (
        movie_id INT,
        person_id INT,
        cast_order TINYINT,
        PRIMARY KEY (movie_id, person_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people (person_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_directors (
        movie_id INT,
        person_id INT,
        PRIMARY KEY (movie_id, person_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (person_id) REFERENCES people (person_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_genres (
        movie_id INT,
        genre_id INT,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS reviews (
        review_id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT NOT NULL,
        rating TINYINT CHECK (rating BETWEEN 1 AND 10),
        comment_txt TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        reviewer_ip VARCHAR(45),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE
    );