import requests
import logging
import json
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()],
)

webmap_id = "4ab98771f61844818663c7bf92670883"

# arcGIS endpoint
url = "https://services3.arcgis.com/m6jZ1AVBKWsoVudm/ArcGIS/rest/services/12_09_2024_world/FeatureServer/0/query"


try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # arcgis requires format param
    params = {"where": "1=1", "outFields": "*", "returnGeometry": "true", "f": "pjson"}

    response = requests.get(url, headers=headers, params=params)

    logging.info(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        logging.info('data', data)

        rows = [feature["attributes"] for feature in data["features"]]
        logging.info('rows', rows)

        df = pd.DataFrame(rows)

        df.to_csv("BAP_certifications.csv", index=False)

        logging.info(f"successfully created csv with {len(rows)} entries.")
        logging.info(list(df.columns()))

except Exception as e:
    logging.error(f"Error occurred: {str(e)}")
