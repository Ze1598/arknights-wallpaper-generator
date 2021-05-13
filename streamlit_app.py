from PIL import Image
import streamlit as st
from streamlit import caching
import pandas as pd
import json
import os
import wallpaper_gen
import utils
st.set_option("deprecation.showfileUploaderEncoding", False)

st.markdown("""
# Arknights Phone Wallpaper Generator

Create phone wallpapers for your favourite Arknights operators!

If you're interested in the code, you can find it on my GitHub repository [here](https://github.com/Ze1598/arknights-wallpaper-generator).

For feedback, feel free to reach out to me on Twitter [@ze1598](https://twitter.com/ze1598).
""")


@st.cache
def load_main_csv():
    """Load the main CSV of operator names, promotion images' URLs and theme colors.
    This function exists so the data can be cached.
    """
    csv_path = os.path.join("static", "data", "operators_info.csv")
    data = pd.read_csv(csv_path, na_values=[""])
    return data


@st.cache
def load_skins_json():
    """Load the JSON with URLs to the skins' art.
    This function exists so the data can be cached.
    """
    json_path = os.path.join("static", "data", "skins_info.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


# Reset all app caches
# caching.clear_cache()
# Load the necessary data and sort it by alphabetical order of names
main_data = load_main_csv()
main_data.sort_values(by="name", inplace=True)
skins_data = load_skins_json()

# Dropdown to filter by operator rank
operator_rank = st.selectbox(
    "Choose the operator rank",
    ("6-star", "5-star", "4-star", "3-star", "2-star", "1-star")
)

# Filter the data by operator rank
for star in range(1, 7):
    star = str(star)
    option = star + "-star"
    # Since the dropdown is single-choice only, this will only match a single\
    # rank at any point in time
    if operator_rank == option:
        filtered_data = main_data[main_data["num_stars"] == int(star)]

operator_rank_int = int(operator_rank[0])
filtered_data = main_data.query(f"num_stars == {operator_rank_int}")

# Dropdown to choose the operator
operator_chosen = st.selectbox(
    "Choose your operator",
    filtered_data["name"].to_numpy()
)

# Get data for the chosen operator
chosen_op_data = main_data[main_data["name"] == operator_chosen]
operator_name = chosen_op_data["name"].iloc[0]
operator_rank = chosen_op_data["num_stars"].iloc[0]
is_low_rank = operator_rank in (1, 2, 3)
e0_art = chosen_op_data["e0_img"].iloc[0]
e2_art = chosen_op_data["e2_img"].iloc[0]\
    if str(chosen_op_data["e2_img"].iloc[0]) != "nan" else ""
op_default_color = chosen_op_data["color"].iloc[0]

# By default, the foreground art is the base/E1 art
foreground_art = e0_art
# By default, the background art is the E2 art
background_art = e2_art

# Get lists of skin names and their respective art URLs
skins_available = skins_data.get(operator_name, None)
skin_names = tuple(skins_available.keys())\
    if skins_available != None else tuple()

# List of available art to choose from (promotion and skins)
art_choices = utils.create_avail_art_options(skin_names, operator_name, e2_art)
# Foreground art must always be selected
fg_art_choices = art_choices[:-1]

# Choose the fore and background art individually
foreground_art = st.selectbox(
    "Which art do you want in the front?",
    fg_art_choices
)
background_art = st.selectbox(
    "Which art do you want in the back?",
    art_choices
)

# Upload a custom background image for the wallpaper
custom_bg_img = st.file_uploader(
    "You can upload a custom background image to replace the default black one with 640x1280 dimensions (otherwise it is resized)", 
    type=["png", "jpg"]
)
# Save the uploaded image (deleted from the server at the end of the script)
if custom_bg_img != None:
    custom_bg_name = "custom_bg_img.png"
    custom_bg_path = os.path.join("static", "resources", custom_bg_name)
    pil_custom_bg_img = Image.open(custom_bg_img).resize((640, 1280)).save(custom_bg_path)

# Change the operator theme color
# Using the beta version until the generally available version is fixed in Streamlit 
#custom_op_color = st.color_picker("Feel free to change the operator theme color", op_default_color)
custom_op_color = st.beta_color_picker("Feel free to change the operator theme color", op_default_color)

# Put together relevant operator information in a single dictionary
operator_info = {
    "E0 art": e0_art,
    "E2 art": e2_art,
    "skins": skins_available,
    "bg_chosen": background_art,
    "fg_chosen": foreground_art
}

# Get the url for fore and background art
fg_art_url = utils.get_art_url(foreground_art, operator_info)
bg_art_url = utils.get_art_url(background_art, operator_info)

# Create the image name string
wallpaper_name = operator_name + ".png"
wallpaper_bg_path = custom_bg_path if custom_bg_img != None else ""

# Generate the wallpaper
wallpaper_gen.main(
    wallpaper_name,
    fg_art_url,
    bg_art_url,
    wallpaper_bg_path,
    custom_op_color
)
# Display the wallpaper
st.image(wallpaper_name, use_column_width=True)

# Encode the image to bytes so a download link can be created
encoded_img = utils.encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
# Create the download link
st.markdown(href, unsafe_allow_html=True)

# Delete the graphic from the server
os.remove(wallpaper_name)
try:
    os.remove(custom_bg_path)
except:
    pass