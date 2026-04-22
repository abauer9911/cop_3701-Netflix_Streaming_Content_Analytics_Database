import csv
import random
from datetime import date

INPUT_FILE = "netflix_titles.csv"

CONTENT_FILE = "content.csv"
GENRE_FILE = "genre.csv"
COUNTRY_FILE = "country.csv"
CONTENT_GENRE_FILE = "contentgenre.csv"
CONTENT_COUNTRY_FILE = "contentcountry.csv"
CONTENT_METRICS_FILE = "contentmetrics.csv"
EPISODE_FILE = "episode.csv"


def clean_text(value):
    """Return stripped text or empty string if None."""
    if value is None:
        return ""
    return value.strip()


def parse_duration(duration_text, content_type):
    """
    Split Kaggle duration field into:
    - duration_minutes for movies
    - seasons for TV shows
    """
    duration_text = clean_text(duration_text)

    if duration_text == "":
        return "", ""

    parts = duration_text.split()

    if len(parts) == 0:
        return "", ""

    number_part = parts[0]

    if not number_part.isdigit():
        return "", ""

    number = int(number_part)

    if content_type == "Movie":
        return number, ""
    elif content_type == "TV Show":
        return "", number
    else:
        return "", ""


def get_region(country_name):
    """
    Assign a simple region for each country.
    This can be expanded as needed.
    """
    region_map = {
        "United States": "North America",
        "Canada": "North America",
        "Mexico": "North America",
        "Brazil": "South America",
        "Argentina": "South America",
        "Chile": "South America",
        "Colombia": "South America",
        "Peru": "South America",
        "United Kingdom": "Europe",
        "France": "Europe",
        "Germany": "Europe",
        "Spain": "Europe",
        "Italy": "Europe",
        "Ireland": "Europe",
        "Netherlands": "Europe",
        "Belgium": "Europe",
        "Sweden": "Europe",
        "Norway": "Europe",
        "Denmark": "Europe",
        "Finland": "Europe",
        "Poland": "Europe",
        "Portugal": "Europe",
        "Russia": "Europe",
        "Turkey": "Asia",
        "India": "Asia",
        "China": "Asia",
        "Japan": "Asia",
        "South Korea": "Asia",
        "Pakistan": "Asia",
        "Indonesia": "Asia",
        "Thailand": "Asia",
        "Philippines": "Asia",
        "Singapore": "Asia",
        "Malaysia": "Asia",
        "Taiwan": "Asia",
        "Hong Kong": "Asia",
        "Israel": "Asia",
        "United Arab Emirates": "Asia",
        "Saudi Arabia": "Asia",
        "Egypt": "Africa",
        "South Africa": "Africa",
        "Nigeria": "Africa",
        "Kenya": "Africa",
        "Ghana": "Africa",
        "Morocco": "Africa",
        "Australia": "Oceania",
        "New Zealand": "Oceania"
    }

    return region_map.get(country_name, "Other")


def safe_show_id_to_int(show_id_text):
    """
    Convert show_id like s1, s25, s8807 into integer content_id values.
    """
    show_id_text = clean_text(show_id_text)
    digits = ""

    for char in show_id_text:
        if char.isdigit():
            digits += char

    if digits == "":
        return None

    return int(digits)


def main():
    # Store normalized lookup data
    genre_to_id = {}
    country_to_id = {}

    genre_rows = []
    country_rows = []
    content_rows = []
    content_genre_rows = []
    content_country_rows = []
    content_metrics_rows = []
    episode_rows = []

    next_genre_id = 1
    next_country_id = 1

    # Use a fixed seed so generated values are consistent on every run
    random.seed(3701)

    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            show_id = clean_text(row.get("show_id"))
            content_id = safe_show_id_to_int(show_id)

            if content_id is None:
                continue

            content_type = clean_text(row.get("type"))
            title = clean_text(row.get("title"))
            release_year = clean_text(row.get("release_year"))
            date_added = clean_text(row.get("date_added"))
            rating = clean_text(row.get("rating"))
            duration = clean_text(row.get("duration"))
            description = clean_text(row.get("description"))

            duration_minutes, seasons = parse_duration(duration, content_type)

            # Build Content row
            content_rows.append([
                content_id,
                title,
                content_type,
                release_year,
                date_added,
                rating,
                duration_minutes,
                seasons,
                description
            ])

            # Build Genre + ContentGenre
            listed_in = clean_text(row.get("listed_in"))
            if listed_in != "":
                genre_list = [g.strip() for g in listed_in.split(",") if g.strip() != ""]

                for i, genre_name in enumerate(genre_list):
                    if genre_name not in genre_to_id:
                        genre_to_id[genre_name] = next_genre_id
                        genre_rows.append([next_genre_id, genre_name])
                        next_genre_id += 1

                    genre_id = genre_to_id[genre_name]
                    is_primary_genre = "TRUE" if i == 0 else "FALSE"

                    content_genre_rows.append([
                        content_id,
                        genre_id,
                        is_primary_genre
                    ])

            # Build Country + ContentCountry
            country_field = clean_text(row.get("country"))
            if country_field != "":
                country_list = [c.strip() for c in country_field.split(",") if c.strip() != ""]

                for country_name in country_list:
                    if country_name not in country_to_id:
                        region = get_region(country_name)
                        country_to_id[country_name] = next_country_id
                        country_rows.append([next_country_id, country_name, region])
                        next_country_id += 1

                    country_id = country_to_id[country_name]

                    content_country_rows.append([
                        content_id,
                        country_id
                    ])

            # Build ContentMetrics (fabricated but consistent)
            popularity_score = round(random.uniform(60.0, 99.9), 1)
            rank_score = round(random.uniform(60.0, 99.9), 1)
            last_ranked_on = str(date.today())

            content_metrics_rows.append([
                content_id,
                popularity_score,
                rank_score,
                last_ranked_on
            ])

            # Build Episode rows for TV Shows only (fabricated)
            if content_type == "TV Show" and seasons != "":
                season_count = int(seasons)

                # Keep generated episode data small and manageable
                seasons_to_generate = min(season_count, 2)

                for season_number in range(1, seasons_to_generate + 1):
                    for episode_number in range(1, 3):
                        episode_title = f"Episode {episode_number}"
                        runtime_minutes = 45 + episode_number

                        episode_rows.append([
                            content_id,
                            season_number,
                            episode_number,
                            episode_title,
                            runtime_minutes
                        ])

    # Write content.csv
    with open(CONTENT_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "content_id",
            "title",
            "type",
            "release_year",
            "date_added",
            "rating",
            "duration_minutes",
            "seasons",
            "description"
        ])
        writer.writerows(content_rows)

    # Write genre.csv
    with open(GENRE_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "genre_id",
            "genre_name"
        ])
        writer.writerows(genre_rows)

    # Write country.csv
    with open(COUNTRY_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "country_id",
            "country_name",
            "region"
        ])
        writer.writerows(country_rows)

    # Write contentgenre.csv
    with open(CONTENT_GENRE_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "content_id",
            "genre_id",
            "is_primary_genre"
        ])
        writer.writerows(content_genre_rows)

    # Write contentcountry.csv
    with open(CONTENT_COUNTRY_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "content_id",
            "country_id"
        ])
        writer.writerows(content_country_rows)

    # Write contentmetrics.csv
    with open(CONTENT_METRICS_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "content_id",
            "popularity_score",
            "rank_score",
            "last_ranked_on"
        ])
        writer.writerows(content_metrics_rows)

    # Write episode.csv
    with open(EPISODE_FILE, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([
            "content_id",
            "season_number",
            "episode_number",
            "episode_title",
            "runtime_minutes"
        ])
        writer.writerows(episode_rows)

    print("CSV files created successfully:")
    print(f"- {CONTENT_FILE}")
    print(f"- {GENRE_FILE}")
    print(f"- {COUNTRY_FILE}")
    print(f"- {CONTENT_GENRE_FILE}")
    print(f"- {CONTENT_COUNTRY_FILE}")
    print(f"- {CONTENT_METRICS_FILE}")
    print(f"- {EPISODE_FILE}")


if __name__ == "__main__":
    main()
