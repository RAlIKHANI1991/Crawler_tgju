import time
import random
import requests

from utils.config import DEFAULT_HEADERS


class TGJUClient:

    def __init__(self, identifier):

        self.identifier = identifier

        self.base_url = (
            f"https://api.tgju.org/v1/"
            f"market/indicator/summary-table-data/"
            f"{identifier}"
        )

        self.session = requests.Session()

        headers = DEFAULT_HEADERS.copy()

        headers["Referer"] = (
            f"https://www.tgju.org/"
            f"profile/{identifier}/history"
        )

        self.session.headers.update(headers)

    def get_total(self,params):

        p = params.copy()

        p["draw"] = 1
        p["start"] = 0
        r = self.session.get(self.base_url,params=p,timeout=25)
        r.raise_for_status()
        data = r.json()

        return (data["recordsTotal"],data.get("length", 30))

    def fetch_page(self,params,draw,start,length,retries=3):
        p = params.copy()

        p["draw"] = draw
        p["start"] = start
        p["length"] = length

        for attempt in range(retries):

            try:
                r = self.session.get(self.base_url,params=p,timeout=25)
                r.raise_for_status()

                return r.json()["data"]

            except Exception:
                time.sleep(random.uniform(2, 5))

        raise RuntimeError("all retries failed")