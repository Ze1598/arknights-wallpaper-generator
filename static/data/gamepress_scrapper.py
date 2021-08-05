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


def get_num_operators() -> int:
    """Get the number of operators available on Gamepress.
    """
    req = requests.get(
        "https://gamepress.gg/arknights/tools/interactive-operator-list")
    soup = BeautifulSoup(req.content, "lxml")

    # Each operator has its td element with this class
    op_list = soup.find_all("td", class_="operator-cell")
    # Get the number of operators available
    num_operators = len(op_list)

    return num_operators


def scrape_pages() -> None:
    """Given the page with the list of operators, scrape their names and individual pages' URL.
    This data is exported in a pickle file.
    """
    # Scrape the operator's names and page URLs
    req = requests.get(
        "https://gamepress.gg/arknights/tools/interactive-operator-list")
    soup = BeautifulSoup(req.content, "lxml")

    # Get all the table cells (<td>) with information about the operators
    op_list = soup.find_all("td", class_="operator-cell")
    op_dict = {}
    for op in op_list:
        # Get the name and their personal page from these HTML elements
        name = op.find("div", class_="operator-title").a.text
        page = "https://gamepress.gg" + \
            op.find("div", class_="operator-title").a["href"]
        # Add the new information to the dictionary
        op_dict[name] = page
        # logging.info(f"{datetime.datetime.now()}: Found {name}")
    logging.info(f"{datetime.datetime.now()}: Found {len(op_list)} operators")

    # Write this dictionary to a pickle file
    with open("operator_pages.pickle", "wb") as f:
        pickle.dump(op_dict, f)
        logging.info(f"{datetime.datetime.now()}: Created pickle file with operator pages")


def gen_operator_colour(art_url: str) -> str:
    """Generate a colour for an operator by detecting the most dominant colour on their E0 art.
    """
    # Request the image
    img_req = requests.get(art_url)
    # Read the response content
    img_bytes = BytesIO(img_req.content)
    # Create a ColorThief object for the image (in bytes)
    colour_thief = ColorThief(img_bytes)
    # Build a colour palette
    palette = colour_thief.get_palette(color_count=2)
    # Convert the generated colour to hex
    colour_chosen = palette[0]
    colour_chosen = f"#{colour_chosen[0]:02x}{colour_chosen[1]:02x}{colour_chosen[2]:02x}"
    # Return only the most dominant colour
    return colour_chosen


def scrape_op_art(op_pages: Dict[str, str]) -> None:
    """Given a dictionary of operators and the URLs to their pages, scrape all their promotion and skins artwork.
    """

    # List to contain lists of individual operator information
    operators_info = list()
    # List to contain dictionaries of operator skins
    skins_info = dict()

    # Loop through available operators
    for operator in op_pages:
        logging.info(f"{datetime.datetime.now()}: Scraping {operator}")
        name = operator
        page = op_pages[operator]

        # Get the operator's page
        req = requests.get(page)
        soup = BeautifulSoup(req.content, "lxml")

        # Find all the elements for operator art
        images = soup.find_all("div", class_="operator-image")

        # Find all the elements for promotion levels
        prom_levels = soup.find("ul", class_="operator-image-tabs")\
            .find_all("li")

        # Get the URL for the base/E1 art
        e0_img = images[0].a["href"]

        # If the list of promotion levels has less than 3 levels, then the\
        # operator doesn't have an E2 promotion
        if len(prom_levels) < 3:
            has_e2 = 0
            e2_img = ""
        # Otherwise get their E2 art
        else:
            has_e2 = 1
            e2_img = images[2].a["href"]

        # Find the operator's rank by counting the number of stars they have
        num_stars = len(soup.find("div", class_="rarity-cell").find_all("img"))

        # Generate the operator colour
        # Based on E2 art if they have it, otherwise E0
        operator_colour = gen_operator_colour(e2_img) if e2_img != "" else gen_operator_colour(e0_img)

        # HTML unordered list (<ul>) of skins
        skins_ul = soup.find("ul", class_="skin-image-tabs")
        # Count the number of items in the list above to know the number of skins available
        num_skins = len(skins_ul.find_all("li", class_="tab-link"))

        # If the operator has skins, scrape their URL
        if num_skins > 0:
            # Since the operator skins are the last `num_skins` <li> items of\
            # the <ul>, then create a range to get the last `num_skins` skins\
            # from the `images` <ul>
            _start = -1
            _stop = -num_skins-1
            skins_li = images[_start: _stop: -1]
            op_skins = dict()

            # If the operator is Amiya, then we need to scrape her E1\
            # art since she has different arts for each promotion. Her E1\
            # art will be stored as a skin
            if name == "Amiya":
                op_skins["E1 art"] = images[1].a["href"]

            # Now get a list of all the availble skins' art URLs as a dictionary
            for i, skin_html in enumerate(skins_li):
                op_skins[f"Skin {i+1}"] = f"https://gamepress.gg{skin_html.img['src']}"

            # Add the new info to the running list
            skins_info[name] = op_skins

            # Reset this list so skins' information does not carry over for the\
            # next operator
            skins_ul = list()
            # Ditto for this list
            op_skins = list()

        # Add this operator's info to the running list
        operator_info = [name, num_stars, e0_img, e2_img, has_e2, operator_colour]
        operators_info.append(operator_info)

    
    # Create a DF for the list of lists of operators
    info_df = pd.DataFrame(operators_info, columns=["name", "num_stars", "e0_img", "e2_img", "has_e2", "color"])
    # Load the CSV of operator colors
    # colors_csv = pd.read_csv("colors.csv")
    # Join the two DFs
    # csv_info_join = info_df.merge(colors_csv, how="inner", on="name")
    # Export the complete DF as a CSV
    # csv_info_join.to_csv("operators_info.csv", index=False)
    info_df.to_csv("operators_info.csv", index=False)

    # Export the list of skins dictionaries as a JSON
    with open("skins_info.json", "w") as f:
        json.dump(skins_info, f, indent=2)


def main() -> None:
    # Load the pickle file with the operator pages
    with open("operator_pages.pickle", "rb") as f:
        operator_pages = pickle.load(f)
    
    # Get the number of operators in the pickle and on Gamepress
    num_operators_pickle = len(operator_pages.keys())
    num_operators_gamepress = get_num_operators()

    # If the pickle has as many operators as Gamepress, use this pickle
    # and get the operators' art
    if num_operators_pickle == num_operators_gamepress:
        logging.info(f"{datetime.datetime.now()}: Pickle up to date. Scraping operator art")
        scrape_op_art(operator_pages)
    
    # Otherwise, we need to scrape all operators again, load the new pickle
    # and finally get the operators' art
    else:
        logging.info(f"{datetime.datetime.now()}: Pickle outdated. Scraping operators from scratch")
        scrape_pages()
        with open("operator_pages.pickle", "rb") as f:
            operator_pages = pickle.load(f)
        scrape_op_art(operator_pages)


if __name__ == "__main__":
    main()
    
    # Kept for tests
    # operator_pages = {
    #     "SilverAsh": "https://gamepress.gg/arknights/operator/silverash",
    #     "Amiya": "https://gamepress.gg/arknights/operator/amiya",
    #     "THRM-EX": "https://gamepress.gg/arknights/operator/thrm-ex",
    #     "Lancet-2": "https://gamepress.gg/arknights/operator/lancet-2"
    # }
    # scrape_op_art(operator_pages)