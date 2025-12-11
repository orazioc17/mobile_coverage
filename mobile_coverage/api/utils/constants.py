import os

GEO_URL = "https://data.geopf.fr/geocodage/search"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COVERAGE_CSV_PATH = os.path.join(BASE_DIR, "api", "data", "city_mobile_coverage.csv")

OPERATEURS = {"20801": "Orange", "20810": "SFR", "20815": "Free", "20820": "Bouygue"}

LIST_OPERATEURS = list(OPERATEURS.values())
