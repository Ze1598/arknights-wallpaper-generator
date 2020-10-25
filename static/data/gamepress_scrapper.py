from bs4 import BeautifulSoup
import requests
import pickle
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

# Scrape the operator's names and page URLs
req = requests.get("https://gamepress.gg/arknights/tools/interactive-operator-list")
soup = BeautifulSoup(req.content, "lxml")

op_list = soup.find_all("td", class_="operator-cell")
op_dict = {}
for op in op_list:
	name = op.find("div", class_="operator-title").a.text
	page = "https://gamepress.gg" + op.find("div", class_="operator-title").a["href"]
	op_dict[name] = page

with open("operator_pages.pickle", "wb") as f:
	pickle.dump(op_dict, f)
	logging.info("Created pickle file with operator pages.")
# -----------------------------------------------------------------------------

# Scrape the operator's gallery URLs and star rankings
with open("operator_pages.pickle", "rb") as f:
	operator_pages = pickle.load(f)

# operator_pages ={
# 	"Ch'en": "https://gamepress.gg/arknights/operator/chen",
# 	"Aak": "https://gamepress.gg/arknights/operator/aak",
# 	"Blaze": "https://gamepress.gg/arknights/operator/blaze"
# }
operators_info = list()
for operator in operator_pages:
	logging.info(f"Scraping {operator}")
	name = operator
	page = operator_pages[operator]
	req = requests.get(page)
	soup = BeautifulSoup(req.content, "lxml")

	# e1_img = soup.find("div", id="image-tab-1")

	# e1_img = soup.find("div", class_="operator-image")\
		# .find("a")["href"]

	images = soup.find_all("div", class_="operator-image")

	prom_levels = soup.find("ul", class_="operator-image-tabs")\
		.find_all("li")

	e1_img = images[0].a["href"]

	# If the list of promotion levels has less than 3 options, then the\
	# operator doesn't have an E2 promotion
	if len(prom_levels) < 3:
		has_e2 = 0
		e2_img = ""
	else:
		has_e2 = 1
		# url_up_to_prom_level = e1_img.split(".png")[0]
		# e2_img = url_up_to_prom_level[:-1] + "2.png"
		e2_img = images[2].a["href"]

	num_stars = len(soup.find("div", class_="rarity-cell").find_all("img"))

	operator_info = [name, num_stars, e1_img, e2_img, has_e2]
	operators_info.append(operator_info)

info_df = pd.DataFrame(operators_info)
info_df.columns = ["name", "num_stars", "e1_img", "e2_img", "has_e2"]
info_df.to_csv("operators_info.csv", index=False)