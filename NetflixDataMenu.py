import oracledb
import pandas as pd
import random
from datetime import datetime, timedelta
import csv

# --- CONFIGURATION ---
LIB_DIR = r"C:\oraclexe\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "USERNAME"
DB_PASS = "PASSWORD"
DB_DSN = "DSN"

# Initialize Oracle Client
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# Connect to database
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()

print("Connected to Oracle Database")

print("Welcome user!")
def main_menu(cursor):
    while True:
        print("\n--- Netflix Content Explorer ---")
        print("1. Search content by region")
        print("2. Filter by popularity threshold")
        print("3. Filter by content type")
        print("4. Filter by genre")
        print("5. Sort by release year or date added")
        print("6. Exit")

        choice = input("Please select your query: ")

        if choice == "1":
            search_by_region(cursor)
        elif choice == "2":
            popularity_threshold(cursor)
        elif choice == "3":
            filter_by_type(cursor)
        elif choice == "4":
            filter_by_genre(cursor)
        elif choice == "5":
            sort_by_date(cursor)
        elif choice == "6":
            break
        else:
            print("Invalid choice")







# Requirement 1

def search_by_region(cursor):
    region = input("Enter region name: ")

    sql = """
        SELECT c.content_id, c.title, cm.popularity_score, co.country_name, co.region
        FROM Content c
        JOIN ContentMetrics cm ON c.content_id = cm.content_id
        JOIN ContentCountry cc ON c.content_id = cc.content_id
        JOIN Country co ON cc.country_id = co.country_id
        WHERE co.region = :region_input
        ORDER BY cm.popularity_score DESC
    """

    cursor.execute(sql, {"region_input": region})
    rows = cursor.fetchall()

    if not rows:
        print("No content found for that region.")
        return

    else:
      print("\nCONTENT ID | TITLE | POPULARITY | COUNTRY | REGION")
      for r in rows:
          print(f"{r[0]} | {r[1]} | Popularity: {r[2]} | {r[3]} ({r[4]})")



#Requirement 2


def popularity_threshold(cursor):
    min_pop = float(input("Enter minimum popularity score: "))

    sql = """
        SELECT c.content_id, c.title, cm.popularity_score
        FROM Content c
        JOIN ContentMetrics cm ON c.content_id = cm.content_id
        WHERE cm.popularity_score >= :min_pop
        ORDER BY cm.popularity_score DESC
    """

    cursor.execute(sql, {"min_pop": min_pop})
    rows = cursor.fetchall()

    if not rows:
        print("No content meets that popularity threshold.")
        return

    else:
       print("\nCONTENT ID | TITLE | POPULARITY")
       for r in rows:
          print(f"{r[0]} | {r[1]} | Popularity: {r[2]}")





#Requirement 3

def filter_by_type(cursor):
    ctype = input("Enter type (Movie or TV Show): ")
    if(ctype == "movie"):
      ctype = "Movie"
    if(ctype == "tv show"):
       ctype == "TV Show"

    sql = """
        SELECT content_id, title, type, release_year
        FROM Content
        WHERE type = :ctype
        ORDER BY release_year DESC
    """

    cursor.execute(sql, {"ctype": ctype})
    rows = cursor.fetchall()

    if not rows:
        print("No content found for that type.")
        return

    else:
       print("\nCONTENT ID | TITLE | TYPE | RATING")
       for r in rows:
           print(f"{r[0]} | {r[1]} | {r[2]} | Release Year: {r[3]}")





#Requirement 4

def filter_by_genre(cursor):
    genre = input("Enter genre: ")

    sql = """
        SELECT c.content_id, c.title, cm.popularity_score, ge.genre_name
        FROM Content c
        JOIN ContentMetrics cm ON c.content_id = cm.content_id
        JOIN ContentGenre cg ON c.content_id = cg.content_id
        JOIN Genre ge ON cg.genre_id = ge.genre_id
        WHERE ge.genre_name = :genre_input
        ORDER BY cm.popularity_score DESC
    """

    cursor.execute(sql, {"genre_input": genre})
    rows = cursor.fetchall()

    if not rows:
        print("No content found for that genre.")
        return

    else:
       print("\nCONTENT ID | TITLE | POPULARITY | GENRE")
       for r in rows:
           print(f"{r[0]} | {r[1]} | Popularity: {r[2]} | Genre: {r[3]}")







#Requirement 5
def sort_by_date(cursor):
    print("1. Sort by release year")
    print("2. Sort by date added")
    choice = input("Choose an option: ")

    if choice == "1":
        sql = """
            SELECT content_id, title, release_year
            FROM Content
            ORDER BY release_year DESC
        """
    else:
        sql = """
            SELECT content_id, title, date_added
            FROM Content
            ORDER BY TO_DATE(date_added, 'Month DD, YYYY') DESC
        """

    cursor.execute(sql)
    rows = cursor.fetchall()
    print("\nCONTENT ID | TITLE | YEAR/DATE")
    for r in rows:
        print(" | ".join(str(x) for x in r))





main_menu(cursor)
print("Goodbye!")










cursor.close()
conn.close()

print("Oracle connection closed.")