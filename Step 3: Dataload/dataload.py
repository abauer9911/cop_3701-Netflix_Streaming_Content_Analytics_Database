import csv
import oracledb


# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
DB_USER = "YOUR_USERNAME"
DB_PASS = "YOUR_PASSWORD"
DB_DSN = "YOUR_HOST:PORT/SERVICE_NAME"

LIB_DIR = r"PATH_TO_ORACLE_INSTANT_CLIENT"

# Initialize thick mode
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# -----------------------------
# CSV FILENAMES
# -----------------------------
CONTENT_FILE = "content.csv"
GENRE_FILE = "genre.csv"
COUNTRY_FILE = "country.csv"
CONTENT_GENRE_FILE = "contentgenre.csv"
CONTENT_COUNTRY_FILE = "contentcountry.csv"
CONTENT_METRICS_FILE = "contentmetrics.csv"
EPISODE_FILE = "episode.csv"

# Batch size for faster loading
BATCH_SIZE = 500


def to_none(value):
    """
    Convert empty strings or 'NULL' strings into Python None.
    """
    if value is None:
        return None

    value = value.strip()

    if value == "" or value.upper() == "NULL":
        return None

    return value


def execute_batch(cursor, sql, rows, table_name):
    """
    Execute inserts in batches for better performance.
    """
    total = len(rows)
    if total == 0:
        print(f"No rows to load for {table_name}.")
        return

    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        cursor.executemany(sql, batch)
        print(f"{table_name}: loaded {min(i + BATCH_SIZE, total)} of {total} rows...")


def load_content(cursor):
    print("Loading Content...")

    rows = []

    with open(CONTENT_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["content_id"]),
                to_none(row["title"]),
                to_none(row["type"]),
                int(row["release_year"]) if to_none(row["release_year"]) is not None else None,
                to_none(row["date_added"]),
                to_none(row["rating"]),
                int(row["duration_minutes"]) if to_none(row["duration_minutes"]) is not None else None,
                int(row["seasons"]) if to_none(row["seasons"]) is not None else None,
                to_none(row["description"])
            ])

    sql = """
        INSERT INTO Content
        (content_id, title, type, release_year, date_added, rating,
         duration_minutes, seasons, description)
        VALUES
        (:1, :2, :3, :4, :5, :6, :7, :8, :9)
    """

    execute_batch(cursor, sql, rows, "Content")


def load_genre(cursor):
    print("Loading Genre...")

    rows = []

    with open(GENRE_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["genre_id"]),
                to_none(row["genre_name"])
            ])

    sql = """
        INSERT INTO Genre
        (genre_id, genre_name)
        VALUES
        (:1, :2)
    """

    execute_batch(cursor, sql, rows, "Genre")


def load_country(cursor):
    print("Loading Country...")

    rows = []

    with open(COUNTRY_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["country_id"]),
                to_none(row["country_name"]),
                to_none(row["region"])
            ])

    sql = """
        INSERT INTO Country
        (country_id, country_name, region)
        VALUES
        (:1, :2, :3)
    """

    execute_batch(cursor, sql, rows, "Country")


def load_contentmetrics(cursor):
    print("Loading ContentMetrics...")

    rows = []

    with open(CONTENT_METRICS_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["content_id"]),
                float(row["popularity_score"]) if to_none(row["popularity_score"]) is not None else None,
                float(row["rank_score"]) if to_none(row["rank_score"]) is not None else None,
                to_none(row["last_ranked_on"])
            ])

    sql = """
        INSERT INTO ContentMetrics
        (content_id, popularity_score, rank_score, last_ranked_on)
        VALUES
        (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
    """

    execute_batch(cursor, sql, rows, "ContentMetrics")


def load_episode(cursor):
    print("Loading Episode...")

    rows = []

    with open(EPISODE_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["content_id"]),
                int(row["season_number"]),
                int(row["episode_number"]),
                to_none(row["episode_title"]),
                int(row["runtime_minutes"]) if to_none(row["runtime_minutes"]) is not None else None
            ])

    sql = """
        INSERT INTO Episode
        (content_id, season_number, episode_number, episode_title, runtime_minutes)
        VALUES
        (:1, :2, :3, :4, :5)
    """

    execute_batch(cursor, sql, rows, "Episode")


def load_contentgenre(cursor):
    print("Loading ContentGenre...")

    rows = []

    with open(CONTENT_GENRE_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["content_id"]),
                int(row["genre_id"]),
                to_none(row["is_primary_genre"])
            ])

    sql = """
        INSERT INTO ContentGenre
        (content_id, genre_id, is_primary_genre)
        VALUES
        (:1, :2, :3)
    """

    execute_batch(cursor, sql, rows, "ContentGenre")


def load_contentcountry(cursor):
    print("Loading ContentCountry...")

    rows = []

    with open(CONTENT_COUNTRY_FILE, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append([
                int(row["content_id"]),
                int(row["country_id"])
            ])

    sql = """
        INSERT INTO ContentCountry
        (content_id, country_id)
        VALUES
        (:1, :2)
    """

    execute_batch(cursor, sql, rows, "ContentCountry")


def main():
    conn = None
    cursor = None

    try:
        print("Connecting to Oracle...")
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN
        )

        cursor = conn.cursor()
        print("Connected successfully.")

        # Parent tables first
        load_content(cursor)
        conn.commit()
        print("Content committed.")

        load_genre(cursor)
        conn.commit()
        print("Genre committed.")

        load_country(cursor)
        conn.commit()
        print("Country committed.")

        # Then dependent tables
        load_contentmetrics(cursor)
        conn.commit()
        print("ContentMetrics committed.")

        load_episode(cursor)
        conn.commit()
        print("Episode committed.")

        load_contentgenre(cursor)
        conn.commit()
        print("ContentGenre committed.")

        load_contentcountry(cursor)
        conn.commit()
        print("ContentCountry committed.")

        print("All data loaded successfully.")

    except Exception as e:
        print("Error while loading data:")
        print(e)

        try:
            if conn is not None:
                conn.rollback()
        except Exception:
            print("Rollback could not be completed because the connection was already closed.")

    finally:
        try:
            if cursor is not None:
                cursor.close()
        except Exception:
            pass

        try:
            if conn is not None:
                conn.close()
        except Exception:
            pass

        print("Oracle connection closed.")


if __name__ == "__main__":
    main()
