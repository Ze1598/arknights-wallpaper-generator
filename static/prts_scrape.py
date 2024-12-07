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

    # List to keep track of failed scrapes
    failed_list = list()

    counter = 1

    for name in operator_pages:
        name_cn = operator_pages[name]["name_cn"]
        url = operator_pages[name]["url"]
        print(f"{counter} / {num_operators}: {name}, {datetime.now()}")

        try:
            # Scrape operator
            operator = PrtsScrapperCharacter(name, name_cn, url)
            # Use translated name to account for russian characters
            translated_name = operator.name_translated
            # Entry for this operator
            operators_list.append(operator.operator_details)

        # Use the except to record failed scrape
        except:
            print(f"FAILED {name}, {datetime.now()}")
            failed_list.append(name)
            time.sleep(60)

        counter += 1

        time.sleep(randint(3, 10))

    # Loop while there are no failed operators
    print()
    while len(failed_list) > 0:
        print(f"{len(failed_list)} fails remain, {datetime.now()}")
        # Always take the first operator from the list
        name = failed_list[0]
        name_cn = operator_pages[name]["name_cn"]
        url = operator_pages[name]["url"]

        try:
            print(f"REPEAT {name} from {len(failed_list)} fails, {datetime.now()}")
            operator = PrtsScrapperCharacter(name, name_cn, url)
            translated_name = operator.name_translated
            operators_list.append(operator.operator_details)
        except:
            print(f"REPEAT FAIL {name}, {datetime.now()}")
            continue
        
        # If scrape successful, then delete it from the list
        del failed_list[0]

        time.sleep(60)



    with open(os.path.join(out_path, "dataset.json"), "w") as f:
        json.dump(operators_list, f, indent=4, ensure_ascii=False)