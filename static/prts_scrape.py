from classes.PrtsScrapper import PrtsScrapper
from classes.PrtsScrapperCharacter import PrtsScrapperCharacter
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from random import randint
import os

if __name__ == "__main__":
    # Base path to write to
    out_path = os.path.join(os.getcwd(), "static", "data")

    # Initialize class to scrape list of existing operators
    scrapper = PrtsScrapper()
    num_operators = scrapper.num_operators_available
    operator_pages = scrapper.operators_url_dict

    
    with open(os.path.join(out_path, "operators_list.json"), "w") as f:
        json.dump(operator_pages, f, indent=4, ensure_ascii=False)


    # Keep track of operator details in a list of dictionaries
    operators_list = list()

    counter = 1

    for name in operator_pages:
        name_cn = operator_pages[name]["name_cn"]
        url = operator_pages[name]["url"]
        print(f"{counter} / {num_operators}: {name}, {datetime.now()}")

        try:
            # if nameoperators_dict[translated_name] == "Castle-3":
            # if name == "Vina Victoria":
            # if name in ("Vina Victoria", "Degenbrecher", "SilverAsh", "Castle-3"):
            # if name in ("Degenbrecher", "SilverAsh"):
            operator = PrtsScrapperCharacter(name, name_cn, url)
            # print(operator.skins)
            # print(operator.page_url)
            # print()
            
            # Use translated name to account for russian characters
            translated_name = operator.name_translated

            # Entry for this operator
            operators_list.append(operator.operator_details)

        # Use the except to retry scrape
        except:
            time.sleep(60)
            print(f"RETRY {counter} / {num_operators}: {name}, {datetime.now()}")

            # Then retry to scrape operator
            operator = PrtsScrapperCharacter(name, name_cn, url)
            translated_name = operator.name_translated
            operators_list.append(operator.operator_details)
            

        counter += 1

        time.sleep(randint(3, 10))


    with open(os.path.join(out_path, "dataset.json"), "w") as f:
        json.dump(operators_list, f, indent=4, ensure_ascii=False)