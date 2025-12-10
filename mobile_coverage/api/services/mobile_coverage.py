import os
from functools import lru_cache
import requests
from requests.exceptions import RequestException

import pandas as pd

GEO_URL = 'https://data.geopf.fr/geocodage/search'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COVERAGE_CSV_PATH = os.path.join(BASE_DIR, "api", "data", "city_mobile_coverage.csv")


class MobileCoverage:
    def __init__(self, query: str):
        self.query = query

    def get_city(self) -> str:
        params = {
            "q": self.query,
            "limit": 1,
            "autocomplete": 1,
            "index": "address",
            "returntruegeometry": False,
        }

        try:
            response = requests.get(GEO_URL, params=params, timeout=5)
            response.raise_for_status()
        except RequestException as e:
            raise ValueError("External geocoding service is unavailable")

        data = response.json()

        if not data.get("features"):
            raise ValueError("No address found for the given query")
        
        props = data["features"][0].get("properties", {})

        try:
            city = props["city"].strip().lower()
            score = props.get("score", None)
        except KeyError:
            raise ValueError("Invalid response from geocoding API")

        return city, score

    @staticmethod
    @lru_cache(maxsize=1)
    def get_coverage_df():
        try:
            return pd.read_csv(COVERAGE_CSV_PATH, sep=";")
        except Exception as e:
            raise RuntimeError("Failed to load coverage data")

    def retrieve_coverage(self):
        city, score = self.get_city()

        df = self.get_coverage_df()
        df = df.query("city == @city")
        city = city.capitalize()

        if df.empty:
            return {
                "matched_city": city,
                "confidence_score": score,
                "coverage": {}
            }
        
        operators = (
            df.set_index("operator")[["2G", "3G", "4G"]]
            .astype(bool)
            .to_dict(orient="index")
        )

        return {
            "matched_city": city,
            "confidence_score": score,
            "coverage": operators
        }

