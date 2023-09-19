import re

import aswan
import datazimmer as dz

LIMIT = 48

IDS = list(range(63)) + [
    2001,
    2005,
    2007,
    2010,
    2011,
    2014,
    2015,
    2017,
    2022,
    2024,
    2028,
    2034,
    2046,
    2050,
    2051,
    2056,
    2059,
    2061,
]

main_url = dz.SourceUrl("https://arfigyelo.gvh.hu/api/products-by-category/")


def make_url(i, offset=0):
    return aswan.add_url_params(main_url + str(i), {"limit": LIMIT, "offset": offset})


STARTER_URLS = [make_url(i) for i in IDS]


class GetProducts(aswan.RequestJsonHandler):
    process_indefinitely = False

    def parse(self, obj: dict):
        offset = int(re.compile("offset=(\d+)").findall(self._url)[0])
        if (offset + LIMIT) < obj["count"]:
            self.register_links_to_handler(
                [aswan.add_url_params(self._url, {"offset": offset + LIMIT})]
            )
        return obj


class HunGovPriceCollect(dz.DzAswan):
    name = "arfigyelo"
    cron = "0 10 * * *"

    starters = {GetProducts: STARTER_URLS}
