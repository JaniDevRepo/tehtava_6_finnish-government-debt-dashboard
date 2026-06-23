import requests
import pandas as pd


# Tilastokeskuksen StatFin PXWeb API -osoite valitulle velkataulukolle
API_URL = "https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/jali/122g.px"


def fetch_debt_data():
    """Hakee Suomen valtion velkadatan Tilastokeskuksen API:sta."""

    query = {
        "query": [
            {
                "code": "sektoriluokitus_7_20230101",
                "selection": {
                    "filter": "item",
                    "values": ["S1311"]
                }
            },
            {
                "code": "contentscode",
                "selection": {
                    "filter": "item",
                    "values": ["jali-D"]
                }
            }
        ],
        "response": {
            "format": "CSV"
        }
    }

    response = requests.post(API_URL, json=query, timeout=30)
    response.raise_for_status()

    return response.text


def save_raw_data(csv_text, file_path="data/raw_debt_data.csv"):
    """Tallentaa API:sta haetun raakadatana CSV-tiedostoon."""

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(csv_text)


if __name__ == "__main__":
    csv_data = fetch_debt_data()
    save_raw_data(csv_data)

    print("Data haettu onnistuneesti.")
    print("Raakadata tallennettu tiedostoon: data/raw_debt_data.csv")