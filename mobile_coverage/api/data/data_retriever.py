import os

import requests
import pandas as pd

URL = 'https://data.geopf.fr/geocodage/search'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MobileCoverage:
    def __init__(self, query: str):
        self.query = query
    
    def get_city(self) -> str:
        params = {
            'q': self.query,
            'limit': 1,
            'autocomplete': 1,
            'index': 'address',
            'returntruegeometry': False
        }
        result = requests.get(URL, params=params)
        result_json = result.json()
        city = result_json['features'][0]['properties']['city'].lower()
        return city

    def get_coverage_df(self):
        csv_path = os.path.join(BASE_DIR, "city_mobile_coverage.csv")
        df = pd.read_csv(csv_path, sep=';')
        return df

    def retrieve_coverage(self):
        city = self.get_city()
        df = self.get_coverage_df()
        df = df.loc[df.city == city]

        """
        return as 
        {
            "orange": {"2G": true, "3G": true, "4G": false}, 
            "SFR": {"2G": true, "3G": true, "4G": true}
        }
        """

        print(df.head)
        operators = df.groupby(by=['operator'], as_index=True)
        print(operators)
        return operators.to_dict(orient='index')

