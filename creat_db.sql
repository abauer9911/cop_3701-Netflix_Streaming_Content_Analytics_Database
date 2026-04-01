-- Drop tables first if they already exist
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Episode CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ContentMetrics CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ContentGenre CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ContentCountry CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Genre CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Country CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Content CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Create parent tables first

CREATE TABLE Content (
    content_id NUMBER PRIMARY KEY,
    title VARCHAR2(255) NOT NULL,
    type VARCHAR2(20) NOT NULL,
    release_year NUMBER(4) NOT NULL,
    date_added VARCHAR2(50),
    rating VARCHAR2(20),
    duration_minutes NUMBER,
    seasons NUMBER,
    description VARCHAR2(2000)
);

CREATE TABLE Genre (
    genre_id NUMBER PRIMARY KEY,
    genre_name VARCHAR2(100) NOT NULL UNIQUE
);

CREATE TABLE Country (
    country_id NUMBER PRIMARY KEY,
    country_name VARCHAR2(100) NOT NULL UNIQUE,
    region VARCHAR2(50)
);

-- Create associative and dependent tables

CREATE TABLE ContentGenre (
    content_id NUMBER NOT NULL,
    genre_id NUMBER NOT NULL,
    is_primary_genre VARCHAR2(5),
    CONSTRAINT pk_contentgenre PRIMARY KEY (content_id, genre_id),
    CONSTRAINT fk_contentgenre_content FOREIGN KEY (content_id)
        REFERENCES Content(content_id),
    CONSTRAINT fk_contentgenre_genre FOREIGN KEY (genre_id)
        REFERENCES Genre(genre_id),
    CONSTRAINT chk_contentgenre_primary
        CHECK (is_primary_genre IN ('TRUE', 'FALSE'))
);

CREATE TABLE ContentCountry (
    content_id NUMBER NOT NULL,
    country_id NUMBER NOT NULL,
    CONSTRAINT pk_contentcountry PRIMARY KEY (content_id, country_id),
    CONSTRAINT fk_contentcountry_content FOREIGN KEY (content_id)
        REFERENCES Content(content_id),
    CONSTRAINT fk_contentcountry_country FOREIGN KEY (country_id)
        REFERENCES Country(country_id)
);

CREATE TABLE ContentMetrics (
    content_id NUMBER PRIMARY KEY,
    popularity_score NUMBER(4,1),
    rank_score NUMBER(4,1),
    last_ranked_on DATE,
    CONSTRAINT fk_contentmetrics_content FOREIGN KEY (content_id)
        REFERENCES Content(content_id)
);

CREATE TABLE Episode (
    content_id NUMBER NOT NULL,
    season_number NUMBER NOT NULL,
    episode_number NUMBER NOT NULL,
    episode_title VARCHAR2(255),
    runtime_minutes NUMBER,
    CONSTRAINT pk_episode PRIMARY KEY (content_id, season_number, episode_number),
    CONSTRAINT fk_episode_content FOREIGN KEY (content_id)
        REFERENCES Content(content_id)
);