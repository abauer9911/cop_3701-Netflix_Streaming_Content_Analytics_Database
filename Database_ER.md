# Netflix Streaming Content Analytics Database  
## Entity-Relationship (ER) Model

## Overview

This ER model represents the structural design of the Netflix Streaming Content Analytics database. The purpose of this database is to organize and analyze global Netflix content data, including content metadata, genre classifications, country availability, episode structure for TV shows, and ranking metrics used for analytics.

The design emphasizes normalization, analytical flexibility, and support for future features such as materialized views, country-based partitioning, and stored procedures for ranking.

---

## ER Diagram

<img width="602" height="497" alt="image" src="https://github.com/user-attachments/assets/c92b3d70-2d7b-4cf1-b3fe-7c8e425acc10" />

---

## Entity Classification

### Strong Entities
- **Content**
- **Genre**
- **Country**
- **ContentMetrics**

These entities contain their own primary keys and exist independently within the database.

### Weak Entity
- **Episode**

The Episode entity is dependent on Content. An episode cannot exist without an associated content record (specifically a TV Show). Its full identifying key consists of:

- `content_id`
- `season_number`
- `episode_number`

Because it depends on Content for identification, it is modeled as a weak entity.

### Associative (Bridge) Entities
- **ContentGenre**
- **ContentCountry**

These entities resolve many-to-many relationships and contain foreign keys referencing their related entities.

---

## Relationship Types

This ER model includes all required relationship types.

### One-to-One (1:1)
- **Content <-> ContentMetrics**

Each content item may have one corresponding analytics record in ContentMetrics.  
ContentMetrics cannot exist without a related Content record.

---

### One-to-Many (1:M)
- **Content -> Episode**

One content record (TV Show) can have multiple episodes.  
Each episode belongs to exactly one content record.

---

### Many-to-Many (M:N)

- **Content <-> Genre** (via ContentGenre)
- **Content <-> Country** (via ContentCountry)

A content item can belong to multiple genres and be associated with multiple countries.  
Likewise, each genre and country can relate to multiple content items.

These relationships are resolved using associative entities.

---

## Foreign Keys

The following foreign key relationships are implemented:

- `ContentGenre.content_id` → `Content.content_id`
- `ContentGenre.genre_id` → `Genre.genre_id`
- `ContentCountry.content_id` → `Content.content_id`
- `ContentCountry.country_id` → `Country.country_id`
- `ContentMetrics.content_id` → `Content.content_id`
- `Episode.content_id` → `Content.content_id`

---

## Attribute Requirements Coverage

This ER model includes all required attribute types:

- **Identifier Attributes (Primary Keys):**
  - `content_id`
  - `genre_id`
  - `country_id`

- **Single-Value Attributes:**
  - `release_year`
  - `genre_name`
  - `country_name`

- **Mandatory Attributes (NOT NULL):**
  - `Content.title`
  - `Content.type`
  - `Content.release_year`
  - `Genre.genre_name`
  - `Country.country_name`

- **Optional Attributes:**
  - `date_added`
  - `rating`
  - `description`
  - `episode_title`
  - `popularity_score`
  - `rank_score`

---

## User Groups

The database is designed to support multiple user groups:

### Data Analysts
Run queries to evaluate genre trends, release patterns, and regional distribution of content.

### Content Strategy Team
Analyze country-based availability and genre popularity to inform licensing and production decisions.

### Database Administrators
Maintain partitions, indexes, materialized views, and stored procedures used for ranking and analytics.

### Executive Reporting Users
Access summarized ranking and popularity data generated from stored procedures and analytical views.

---

## Design Considerations

- Multi-valued attributes in the original dataset (genres and countries) were normalized into separate entities and resolved using associative tables.
- A weak entity (Episode) was introduced to support hierarchical modeling of TV content.
- A one-to-one relationship (Content ↔ ContentMetrics) supports future ranking and stored procedure implementation.
- The schema supports country-based partitioning and materialized views for genre popularity analysis in later project phases.

This ER model provides a structured foundation for implementing the relational schema and analytical components required in the next stages of the project.
