# arknights-wallpaper-generator [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)
[live app](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights mobile wallpapers on the fly.
The art was scraped from [Gamepress](https://gamepress.gg/arknights/tools/interactive-operator-list) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The default colors for each operator was done manually by me.

Simply choose your favorite operator and the wallpaper will be generated in the moment. You can filter operators by rank (number of stars), and choose a theme color if you don't like the default one and even play around with skins!

Limitations:
* 1-star operators' art is bigger than the others (I consider this a easter egg since they are already big in-game)
* 3-star operators and below don't have background art, since they don't have E2 art, but you can play around with skins for those that have them
* Can't choose the normal/E0 art as the background art (though you can trick the app to do this for 3-star and below operators)
