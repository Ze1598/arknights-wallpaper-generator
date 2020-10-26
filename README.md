# arknights-wallpaper-generator

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights mobile wallpapers on the fly.
The art was scraped from [Gamepress](https://gamepress.gg/arknights/tools/interactive-operator-list) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The default colors for each operator was done manually by me.

Simply choose your favorite operator and the wallpaper will be generated in the moment. You can filter operators by rank (number of stars), and even choose a theme color if you don't like the default one!

Limitations:
* 1-star operators' art is bigger than the others (I consider this a easter egg since they are already big in-game)
* 3-star operators and below don't have background art, since they don't have E2 art
* Skins' art is not available in the app
