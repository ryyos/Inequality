import requests

from pyquery import PyQuery
from time import time, sleep
from datetime import datetime
from icecream import ic
from tqdm import tqdm

from urllib import request
from src.utils.fileIO import File
from src.utils.corrector import vname


class Inequality:
    def __init__(self) -> None:
        self.__file = File()

        self.URL = 'https://wid.world/data/'
        self.API = 'https://wid.world/wp-content/generated-files/widsummaryfile/WID_SummaryTable.json?order=asc&offset=0&limit=10'
        self.DATASET = "https://wid.world/bulk_download/wid_all_data.zip"
        self.DOMAIN = 'wid.world'
        ...

    def __curl(self, path: str, url: str):
        try:
            if url: request.urlretrieve(url, path)
        except Exception:
            ic('eror')
        ...

    def main(self):
        response = requests.get(self.API)
        raw_json: dict = response.json()

        main_response = requests.get(self.URL)
        html = PyQuery(main_response.text)
        
        PATH = 'data/zip/all_dataset.zip'

        # self.__curl(path=PATH, url=self.DATASET)

        results = {
            "domain": self.DOMAIN,
            "url": self.URL,
            "tags": [self.DOMAIN],
            "crawling_time": str(datetime.now()),
            "crawling_time_epoch": int(time()),
            "title": html.find('a.header_logo').text(),
            "category":"",
            "path_data_raw": PATH,
            "tables": []
        }

        for index, one in tqdm(enumerate(raw_json),
                               ascii=True,
                               smoothing=0.1, 
                               total=len(raw_json)
                               ):
            table = {
                key.lower(): list(one.values())[value] for value, key in enumerate(one.keys())
            }

            if index == 0 or results["category"] == one["Country"]:
                results["category"] = one["Country"]
                results["tables"].append(table)

                if table["source"]: source = PyQuery(table["source"])
                table["source"] = [PyQuery(source).text() for source in source.find('a')]

            else:
                self.__file.write_json(f'data/json/{vname(results["category"])}.json', content=results)

                results["category"] = one["Country"]
                results["tables"].clear()
                results["tables"].append(table)

                if table["source"]: source = PyQuery(table["source"])
                table["source"] = [PyQuery(source).text() for source in source.find('a')]

        ...


