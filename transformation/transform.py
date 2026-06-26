import sqlite3
import pandas as pd


DB_PATH = "data/government_debt.db"


def read_debt_data():
    """Lukee velkadatan SQLite-tietokannasta pandas DataFrameen."""
    connection = sqlite3.connect(DB_PATH)

    query = """
    SELECT year, sector, debt_million_eur
    FROM government_debt
    ORDER BY year
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df

def transform_debt_data(df):
    """Lisää analyysiä varten lasketut sarakkeet."""
    df = df.copy()

    # Muutetaan velka miljoonista euroista miljardeiksi euroiksi
    df["debt_billion_eur"] = df["debt_million_eur"] / 1000

    # Lasketaan vuosittainen euromääräinen kasvu
    df["annual_growth_eur"] = df["debt_million_eur"].diff()

    # Lasketaan vuosittainen prosentuaalinen kasvu
    df["annual_growth_percent"] = df["debt_million_eur"].pct_change() * 100
    
    df["debt_billion_eur"] = df["debt_billion_eur"].round(3)
    df["annual_growth_eur"] = df["annual_growth_eur"].round(0)
    df["annual_growth_percent"] = df["annual_growth_percent"].round(2)

    return df

def save_transformed_data(df):
    """Tallentaa muunnetun aineiston CSV-tiedostoon."""
    output_path = "data/transformed_debt_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Muunnettu data tallennettu tiedostoon: {output_path}")


if __name__ == "__main__":
    df = read_debt_data()
    transformed_df = transform_debt_data(df)

    save_transformed_data(transformed_df)

    print(transformed_df)