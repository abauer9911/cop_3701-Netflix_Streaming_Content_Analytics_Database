# Netflix Streaming Content Analytics Database

## Project Overview
The goal of this project is to design and implement a relational database that analyzes Netflix’s global streaming content catalog. The database focuses on content availability across countries, genre distribution, content ratings, release patterns, and ranking analytics. 

The system is designed using a normalized ER model that supports analytical queries, materialized views, country-based partitioning, and stored procedures for ranking and trend evaluation.

This project is developed for the Database 1 course and emphasizes core database design principles including normalization, entity classification (strong, weak, associative), relationship modeling, indexing, and analytics-oriented schema design.

---

## Application Domain
**Streaming Media Analytics / Entertainment Data Management**

The application domain centers on streaming platforms, specifically Netflix, and how large-scale content metadata can be structured for analytical purposes. Streaming platforms operate globally and manage multi-valued attributes such as genres and country availability, making normalization and relationship modeling essential.

---

## Database Design Summary

The ER model includes:

### Strong Entities
- **Content** – Stores core metadata for movies and TV shows.
- **Genre** – Stores normalized genre classifications.
- **Country** – Stores normalized country information.
- **ContentMetrics** – Stores ranking and analytics metrics associated with content.

### Weak Entity
- **Episode** – Dependent on Content and identified using a composite key (`content_id`, `season_number`, `episode_number`). This supports hierarchical modeling of TV shows.

### Associative (Bridge) Entities
- **ContentGenre** – Resolves the many-to-many relationship between Content and Genre.
- **ContentCountry** – Resolves the many-to-many relationship between Content and Country.

### Relationship Types Modeled
- **One-to-One (1:1):** Content ↔ ContentMetrics  
- **One-to-Many (1:M):** Content → Episode  
- **Many-to-Many (M:N):**  
  - Content ↔ Genre (via ContentGenre)  
  - Content ↔ Country (via ContentCountry)

This design ensures full compliance with relational modeling requirements and supports scalable analytics.

---

## High-Level Goals
The primary goals of this project include:

- Designing a normalized relational schema for Netflix content metadata.
- Supporting global content analysis by country and region.
- Evaluating genre distribution and popularity.
- Analyzing release year trends and rating patterns.
- Implementing ranking and analytical functionality using SQL features such as materialized views and stored procedures.

---

## Key Features and Requirements

### Normalization of Multi-Valued Attributes
The original dataset includes comma-separated genres and countries. These were normalized into separate entities and resolved using associative tables to ensure proper relational design.

### Materialized Views
- A materialized view will analyze genre popularity based on content counts.
- Additional views may support ranking summaries and trend reporting.

### Country-Based Partitioning
ContentCountry and related tables are structured to support partitioning strategies by country or region to improve performance and scalability.

### Stored Procedures
Stored procedures will be implemented to:
- Rank content based on defined metrics.
- Update popularity scores.
- Generate summary analytics.

---

## Intended Users

The database supports multiple user groups:

- **Data Analysts** – Perform analytical queries on genre trends, regional distribution, and release patterns.
- **Content Strategy Teams** – Evaluate content gaps and genre popularity across regions.
- **Database Administrators** – Maintain schema structure, partitions, and stored procedures.
- **Executive Reporting Users** – Consume summarized ranking and popularity data.

---

## Data Source

The dataset used for this project is publicly available on Kaggle:

- **Dataset Name:** Netflix Movies and TV Shows  
- **Source:** Kaggle  
- **URL:** https://www.kaggle.com/datasets/shivamb/netflix-shows  

The dataset contains metadata including:
- Title
- Content type (Movie or TV Show)
- Country
- Release year
- Rating
- Duration
- Genre classifications
- Date added to Netflix

Multi-valued attributes from the dataset were normalized into separate entities to support proper relational modeling.

---

## Project Scope

The scope of this project includes:

- Cleaning and importing the Netflix dataset.
- Implementing the ER model as a relational schema.
- Defining primary and foreign key constraints.
- Writing analytical SQL queries.
- Creating materialized views for genre popularity.
- Implementing stored procedures for ranking and analytics.
- Demonstrating query performance using partitioned structures.

The focus is on backend database architecture and analytics functionality rather than application-layer development.

---

## Tools and Technologies

- Relational Database Management System (PostgreSQL or MySQL)
- SQL for schema design, queries, views, and stored procedures
- GitHub for version control and documentation
- dbdiagram.io for ER modeling
