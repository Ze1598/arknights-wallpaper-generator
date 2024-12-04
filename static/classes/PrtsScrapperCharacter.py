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
import re
from requests_html import HTMLSession
# Local imports
from classes.PrtsScrapper import PrtsScrapper
from classes.WebScraper import WebScraper


class PrtsScrapperCharacter:
    def __init__(self, operator_name, operator_name_cn, operator_url):
        self.name = operator_name
        self.name_cn = operator_name_cn
        self.page_url = operator_url
        self.operator_details = self.load_operator_details()

    def load_operator_details(self):
        """
        Navigate to an operator page, extract their details and return as a dict
        """
        operator_details_dict = {
            "original_name": self.name,
            "url": self.page_url
        }
        # name
        # class
        # stars
        # hp
        # atk
        # def
        # res
        # redeploy
        # block
        # deploy_cost
        # atk_interval
        # limited

        # Scrape all required details
        with WebScraper() as scraper:
            scraper.navigate(self.page_url)
            # Click english language button (reloads page)

            # Get the english-translated character name
            char_name = scraper.page.locator("#firstHeading")
            self.operator_name_translated = char_name.text_content()
            operator_details_dict["name_translated"] = self.operator_name_translated

            char_info = scraper.page.locator(".charinfo-container")
            # # Debug only
            # char_info_html = char_info.evaluate("el => el.outerHTML")
            # print(char_info_html)

            # Find the img element with a src attribute for the rarity image url
            rarity_url = char_info.locator("div.charstar").locator("img").get_attribute("src")
            # And extract the rarity via regex matching on the file name
            rarity_pattern = r'star_(\d+)\.png$'
            # Group 1 being the numeric value in the file name
            rarity_value = re.search(rarity_pattern, rarity_url).group(1)
            operator_details_dict["rarity"] = rarity_value

            # Calculate elite 1 and 2 artwork url
            elite_info = char_info.locator(".stage-btn-wrapper").evaluate("div => div.childNodes")
            elite_stages = len(elite_info)
            elite1_filename = f"立绘_{self.name_cn}_1.png"
            elite1_url = f"https://media.prts.wiki/{self.get_path(elite1_filename)}"
            if elite_stages > 1:
                elite2_filename = f"立绘_{self.name_cn}_2.png"
                elite2_url = f"https://media.prts.wiki/{self.get_path(elite2_filename)}"
            else:
                elite2_url = ""
            operator_details_dict["Elite 1"] = elite1_url
            operator_details_dict["Elite 2"] = elite2_url

            # Calculate skins url
            skin_info = char_info.locator(".charlogo-skin").evaluate("div => div.childNodes")
            skins_dict = dict()
            for skin in range(len(skin_info)):
                skin_name = f"skin{skin + 1}"
                skin_filename = f"立绘_{self.name_cn}_{skin_name}.png"
                skin_url = f"https://media.prts.wiki/{self.get_path(skin_filename)}"
                skins_dict[f"Skin {skin + 1}"] = skin_url
            operator_details_dict["skins"] = skins_dict
            
        # Add up remaining operator details as class attributs
        self.elite1 = operator_details_dict["Elite 1"]
        self.elite2 = operator_details_dict["Elite 2"]
        self.rarity = operator_details_dict["rarity"]
        self.skins = operator_details_dict["skins"]

        return operator_details_dict
            

            
    def get_path(self, filename: Union[str, bytes]) -> str:
        """
        Generate a file path using MD5 hash-based directory structure.
        
        Args:
            filename: The filename to process (string or bytes)
            
        Returns:
            str: Path in format "x/xx/encoded_filename" where x are MD5 hash chars
            
        Raises:
            TypeError: If filename is not string or bytes
            ValueError: If filename is empty
        """
        if not filename:
            raise ValueError("Filename cannot be empty")
            
        # Convert to bytes if string
        if isinstance(filename, str):
            filename_bytes = filename.encode('utf-8')
        elif isinstance(filename, bytes):
            filename_bytes = filename
        else:
            raise TypeError(f"Filename must be string or bytes, not {type(filename)}")
            
        # Generate MD5 hash
        md5 = hashlib.md5(filename_bytes).hexdigest()
        
        # Handle bytes vs string for the URL encoding
        if isinstance(filename, bytes):
            filename = filename.decode('utf-8')
            
        # Construct and return path
        return f"{md5[0]}/{md5[:2]}/{quote(filename)}"
    

if __name__ == "__main__":
    # char_name = "立绘_" + "维娜·维多利亚" + "_1.png"
    # image_path = f"https://media.prts.wiki/{get_path(char_name)}"
    # print(image_path)

    scrapper = PrtsScrapper()
    num_operators = scrapper.num_operators_available
    operator_pages = scrapper.operators_url_dict

    operators_dict = dict()

    for name in operator_pages:
        name_cn = operator_pages[name]["name_cn"]
        url = operator_pages[name]["url"]

        # if name == "Castle-3":
        # if name == "Vina Victoria":
        # if name in ("Vina Victoria", "Degenbrecher", "SilverAsh", "Castle-3"):
        # if name in ("Degenbrecher", "SilverAsh"):
        operator = PrtsScrapperCharacter(name, name_cn, url)
        print(operator.name, operator.rarity)
        # print(operator.skins)
        # print(operator.page_url)
        # print()

        # Entry for this operator
        operators_dict[name] = operator.operator_details

    with open('operators.json', 'w') as f:
        json.dump(operators_dict, f, indent=4)