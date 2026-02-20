# Netflix Streaming Content Analytics Database

## Project Overview
The goal of this project is to design and implement a relational database that analyzes Netflix’s global streaming content catalog. The database will focus on content availability across countries, genre distribution, content ratings, and release patterns over time. By structuring and querying this data effectively, the project aims to support analytical insights such as genre popularity, regional content trends, and ranked content performance.

This project is developed for the Database 1 course and emphasizes practical database concepts including normalization, indexing, partitioning, materialized views, and stored procedures.

---

## Application Domain
**Streaming Media Analytics / Entertainment Data Management**

The application domain centers on streaming platforms, specifically Netflix, and how large-scale content metadata can be stored and analyzed using database systems. This domain is highly relevant due to the global scale of streaming services and the need for efficient data organization to support analytics, reporting, and decision-making.

---

## High-Level Goals
The primary goals of this project include:

- Design a normalized relational database schema to store Netflix content metadata.
- Analyze global content availability by country and region.
- Examine genre distribution and popularity trends.
- Analyze content ratings and release year patterns.
- Implement database-level analytics using advanced SQL features.

---

## Key Features and Requirements
The database will include the following required components:

- **Materialized Views**
  - A materialized view to analyze genre popularity based on content count.
  - Additional views to support analytical queries efficiently.

- **Country-Based Partitioning**
  - Tables will be partitioned by country (or region) to improve query performance and scalability when analyzing geographic content distribution.

- **Stored Procedures**
  - Stored procedures will be implemented to rank content based on defined metrics such as release year, rating, or genre frequency.

---

## Intended Users
The database is intended for:

- Data analysts exploring streaming content trends.
- Researchers studying media distribution and global content availability.
- Database students learning practical SQL and database design concepts.
- Developers interested in analytics-focused database implementations.

---

## Data Source
The dataset used for this project is publicly available on Kaggle:

- **Dataset Name:** Netflix Movies and TV Shows  
- **Source:** Kaggle  
- **URL:** https://www.kaggle.com/datasets/shivamb/netflix-shows  

The dataset contains metadata for Netflix titles, including:
- Title name
- Type (Movie or TV Show)
- Director and cast
- Country of availability
- Release year
- Rating
- Duration
- Listed genres

This dataset is well-suited for relational modeling and analytical querying due to its structured format and global scope.

---

## Project Scope (Tentative)
The scope of this project includes:

- Importing and cleaning the Netflix dataset for database use.
- Designing and implementing a relational schema.
- Writing SQL queries to analyze trends and patterns.
- Creating materialized views and stored procedures as required.
- Demonstrating the database functionality through sample queries.

---

## Tools and Technologies
- Relational Database Management System (RDBMS) (e.g., PostgreSQL or MySQL)
- SQL for schema design, queries, views, and stored procedures
- GitHub for version control and project documentation


