from classes.PrtsScrapper import PrtsScrapper
from classes.PrtsScrapperCharacter import PrtsScrapperCharacter
import json


if __name__ == "__main__":
    scrapper = PrtsScrapper()
    num_operators = scrapper.num_operators_available
    operator_pages = scrapper.operators_url_dict

    # TODO: add logic to compare num available operators vs operators in existing pickle file

    # Keep track of operator details in a dict
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