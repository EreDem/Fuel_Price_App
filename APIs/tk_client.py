import json
import os
import requests
import dotenv
from pathlib import Path

dotenv.load_dotenv()  # load environment variables from .env file
tk_api_key = os.getenv("api_key")

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR.parent / "my-app" / "resources" / "stations.json"

with open(file_path, "r", encoding="utf-8") as f:
    stations = json.load(f)

def get_info_from_station(city):
    print("requesting from tk...")
    # get all stations in city
    stations_in_city = [s for s in stations if s.get("city") and s["city"].strip().lower() == city.strip().lower()]
    # get all ids of stations in city
    station_ids = [s["id"] for s in stations_in_city]

    #tk price request format: https://creativecommons.tankerkoenig.de/json/prices.php?ids=ID1,ID2,...,ID10&apikey=APIKEY
    # split station ids into chunks of 10
    station_id_chunks = [station_ids[i:i + 10] for i in range(0, len(station_ids), 10)]
    station_info = []
    for chunk in station_id_chunks:
        ids_str = ",".join(chunk)
        url = f"https://creativecommons.tankerkoenig.de/json/prices.php?ids={ids_str}&apikey={tk_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for station_id, info in data.get("prices", {}).items():
                station_info.append({
                    "id": station_id,
                    "brand": next((s["brand"] for s in stations_in_city if s["id"] == station_id), "Unknown"),
                    "e5": info.get("e5"),
                    "e10": info.get("e10"),
                    "diesel": info.get("diesel"),
                    "status": info.get("status", "unknown"),
                    "street": next((s["street"] for s in stations_in_city if s["id"] == station_id), "Unknown"),
                    "house_number": next((s["house_number"] for s in stations_in_city if s["id"] == station_id), "Unknown"),
                })
        else:
            print(f"Error fetching data from TK API: {response.status_code}")
    print(station_info)
    return station_info
