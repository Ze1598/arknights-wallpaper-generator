import hashlib
from urllib.parse import quote
from typing import Union
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import pickle
import json
import datetime
import pandas as pd
from typing import Dict
from colorthief import ColorThief
import logging
logging.basicConfig(level=logging.INFO)

class PrtsScrapper:
    def __init__(self):
        self.prts_base_url = "https://prts.wiki/w/"
        # Get list of operators' header html
        self.operators_base_html_list = self.get_operators_base_html()
        self.num_operators_available = len(self.operators_base_html_list)
        # Map operator names to their page url
        self.operators_url_dict = self.get_operator_pages()
        # Generate local pickle whenever the class is instantiated
        # self.write_pickle()

    def get_operators_base_html(self):
        """
        Get a list with the base div header for each operator.
        """
        relative_url = "%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"
        req = requests.get(
            f"{self.prts_base_url}{relative_url}"    
        )
        soup = BeautifulSoup(req.content, "lxml")

        # Each operator has its td element with this class
        op_list = list(soup.find("div", id="filter-data").children)

        return op_list
    
    def get_operator_pages(self):
        """
        Get dictionary mapping operators to their page URL.
        """

        operators_dict = dict()

        for operator_html in self.operators_base_html_list:
            op_name = operator_html["data-en"]
            op_name_cn = operator_html["data-zh"]
            # Map EN name to their url and CN name
            operators_dict[op_name] = {
                "url": f"{self.prts_base_url}{op_name_cn}",
                "name_cn": operator_html["data-zh"]
            }

        # Manually add entries for Amiya alters because only is included in the source
        # The single entry retrived is under Amiya so these will correct that information
        operators_dict["Amiya"] = {
                    "url": "https://prts.wiki/w/阿米娅",
                    "name_cn": "阿米娅"
        }
        operators_dict["Amiya (Guard)"] = {
                    "url": "https://prts.wiki/w/阿米娅(近卫)",
                    "name_cn": "阿米娅(近卫)"
        }
        operators_dict["Amiya (Medic)"] = {
                    "url": "https://prts.wiki/w/阿米娅(医疗)",
                    "name_cn": "阿米娅(医疗)"
        }

        return operators_dict
    
    def write_pickle(self):
        with open("operator_pages.pickle", "wb") as f:
            pickle.dump(self.operators_url_dict, f)


if __name__ == "__main__":
    scrapper = PrtsScrapper()
    num_operators = scrapper.num_operators_available
    operator_pages = scrapper.operators_url_dict