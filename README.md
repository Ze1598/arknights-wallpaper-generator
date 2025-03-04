# arknights-wallpaper-generator [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)
[live app](https://share.streamlit.io/ze1598/arknights-wallpaper-generator/main)

A web app built with [Streamlit](https://www.streamlit.io/) in Python to create Arknights mobile wallpapers on the fly.

# Details

## Update
Artwork and operator details are now sourced from the [PRTS wiki](https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88). The scraping code has also been updated to use [Playwright](https://playwright.dev/python/docs/api/class-playwright).

Choose your favorite operator and the wallpaper will be generated in the moment. You can filter operators by rank (number of stars), and choose a theme color if you don't like the default one and even play around with skins!

## Original details

The art was scraped from [Gamepress](https://gamepress.gg/arknights/tools/interactive-operator-list) and images are loaded directly from their source. This scraping is done with with the [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries.
The default colors for each operator was done manually by me.


# Extra: Docker Image

Some notes about the docker image: how to build and run

## Build the image
-t is the name of the image (the tag)
. is the path to the image, in this case i ran it at the project root

`docker build -t arknights_wallpaper_generator .`

## Run the image
-p port forwarding as exposed_port:image_internal_port
in the example, you will access the streamlit app at port 8502, but the image is using port 8501 internally
also pass it the name of the image to run

`docker run -p 8502:8501 arknights_wallpaper_generator`