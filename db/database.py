import sqlite3
import pandas as pd


DB_PATH = "data/government_debt.db"
CSV_PATH = "data/raw_debt_data.csv"


def create_database():
    """Luo SQLite-tietokannan ja government_debt-taulun."""

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS government_debt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            sector TEXT NOT NULL,
            debt_million_eur REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def import_csv_to_database():
    """Lukee CSV-tiedoston, siivoaa datan ja tallentaa sen SQLite-tietokantaan."""

    df = pd.read_csv(CSV_PATH)

    df = df.rename(columns={
        "Year": "year",
        "Sector": "sector",
        "EDP debt, millions of euro": "debt_million_eur"
    })

    # Poistetaan rivit, joilla velka-arvo puuttuu
    df = df[df["debt_million_eur"] != "."]

    # Poistetaan vuoden perästä mahdollinen tähtimerkki
    df["year"] = df["year"].astype(str).str.replace("*", "", regex=False).astype(int)

    df["debt_million_eur"] = df["debt_million_eur"].astype(float)

    connection = sqlite3.connect(DB_PATH)

    df.to_sql("government_debt", connection, if_exists="replace", index=False)

    connection.close()


def preview_database():
    """Tulostaa tietokannasta ensimmäiset rivit tarkistusta varten."""

    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT
            year,
            sector,
            debt_million_eur
        FROM government_debt
        ORDER BY year""",
        connection
    )

    connection.close()

    print(df)
    print()
    print(f"Ensimmäinen vuosi: {df['year'].min()}")
    print(f"Viimeinen vuosi: {df['year'].max()}")
    print(f"Yhteensä rivejä: {len(df)}")


if __name__ == "__main__":
    create_database()
    import_csv_to_database()
    preview_database()

    print("SQLite-tietokanta luotu ja data tallennettu onnistuneesti.")