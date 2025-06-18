USE imdb_clone;

CREATE TABLE
    IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(128) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_username (username)
    );

CREATE TABLE
    IF NOT EXISTS movies (
        movie_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        year YEAR,
        runtime_min SMALLINT,
        certificate VARCHAR(10),
        overview TEXT,
        gross_usd BIGINT,
        poster_link VARCHAR(512),
        INDEX idx_title (title)
    );

CREATE TABLE
    IF NOT EXISTS actors (
        actor_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS directors (
        director_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS genres (
        genre_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

CREATE TABLE
    IF NOT EXISTS reviews (
        review_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        rating TINYINT CHECK (rating BETWEEN 1 AND 10),
        comment_txt TEXT,
        reviewer_ip VARCHAR(45),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_rating (
        movie_id     INT PRIMARY KEY,
        rating   DECIMAL(3,1),
        votes  INT,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_cast (
        movie_id INT,
        actor_id INT,
        cast_order TINYINT,
        PRIMARY KEY (movie_id, actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (actor_id) REFERENCES actors (actor_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_directors (
        movie_id INT,
        director_id INT,
        PRIMARY KEY (movie_id, director_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (director_id) REFERENCES directors (director_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS movie_genres (
        movie_id INT,
        genre_id INT,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id) ON DELETE CASCADE
    );

