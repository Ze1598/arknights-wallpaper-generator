import streamlit as st
import pandas as pd
import json
import os
import wallpaper_gen
import utils

st.markdown("""
# Arknights Phone Wallpaper Generator

Create phone wallpapers for your favourite Arknights operators!

If you're interested in the code, you can find it on my GitHub repository [here](https://github.com/Ze1598/arknights-wallpaper-generator).

For feedback, feel free to reach out to me on Twitter [@ze1598](https://twitter.com/ze1598).
""")


@st.cache
def load_main_csv(reset_cache=False):
    """Load the main CSV of operator names, promotion images' URLs and theme colors.
    This function exists so the data can be cached.
    """
    csv_path = os.path.join("static", "data", "operators_info.csv")
    data = pd.read_csv(csv_path, na_values=[""])
    return data

@st.cache
def load_skins_json(reset_cache=False):
    """Load the JSON with URLs to the skins' art.
    This function exists so the data can be cached.
    """
    json_path = os.path.join("static", "data", "skins_info.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

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

# Dropdown to choose the operator
operator_chosen = st.selectbox(
    "Choose your operator", 
    filtered_data["name"].to_numpy()
)

# Get the data for the chosen operator
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
op_skin_names, op_skin_urls = utils.get_skins_names_urls(skins_data, operator_name)

# Dropdown for choosing between the E1/base art and a skin
skin_options = ["Base art"] + op_skin_names
skin_dropdown = st.selectbox(
    "Do you want to use a skin for your operator? Please note that, by default, it is used as the background art",
    skin_options
)

# Checkbox for swapping fore and background art (defaults to\
# not swapping)
swap_bg_fg = st.checkbox("Swap foreground and background art? Only available for 4-star and above operators, or operators with skins", value=False)

# Set up what fore and background art to use
img_info = {
    "e0_art": e0_art,
    "e2_art": e2_art,
    "skin_names": op_skin_names,
    "skin_urls": op_skin_urls,
    "skin_chosen": skin_dropdown,
    "swap_art": swap_bg_fg,
    "is_low_rank": is_low_rank,
}
foreground_art, background_art = utils.set_fore_background_art(img_info)

# If the checkbox is ticked, then the wallpaper will not have the background art
remove_background = st.checkbox("Remove background art?", value=False)
background_art = "" if remove_background == True else background_art

# Let the user change the operator theme color
custom_op_color = st.beta_color_picker("Feel free to change the operator theme color", op_default_color)

# Create the wallpaper name string
wallpaper_name = operator_name + ".png"
# Generator the wallpaper
wallpaper_gen.main(
    wallpaper_name,
    foreground_art,
    background_art,
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
