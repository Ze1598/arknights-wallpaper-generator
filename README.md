# arknights-wallpaper-generator [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)
[live app](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights mobile wallpapers on the fly.
The art was scraped from [Gamepress](https://gamepress.gg/arknights/tools/interactive-operator-list) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The default colors for each operator was done manually by me.

Simply choose your favorite operator and the wallpaper will be generated in the moment. You can filter operators by rank (number of stars), and choose a theme color if you don't like the default one and even play around with skins!