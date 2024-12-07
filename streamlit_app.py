from PIL import Image
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


def load_main_csv():
    """Load the main CSV of operator names, promotion images' URLs and theme colors.
    This function exists so the data can be cached.
    """
    csv_path = os.path.join("static", "data", "operators_info.csv")
    data = pd.read_csv(csv_path, na_values=[""])
    return data


def load_skins_json():
    """Load the JSON with URLs to the skins' art.
    This function exists so the data can be cached.
    """
    json_path = os.path.join("static", "data", "skins_info.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    return data


# Load dataset
json_path = os.path.join(os.getcwd(), "static", "data", "dataset.json")
dataset = pd.read_json(json_path)
dataset.sort_values(by="name_translated", inplace=True)

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
        filtered_data = dataset[dataset["rarity"] == int(star)]

operator_rank_int = int(operator_rank[0])
filtered_data = dataset.query(f"rarity == {operator_rank_int}")

# Dropdown to choose the operator
operator_chosen = st.selectbox(
    "Choose your operator",
    filtered_data["name_translated"].to_numpy()
)

# Get data for the chosen operator (as a dictionary)
chosen_op_data = dataset[dataset["name_translated"] == operator_chosen]
chosen_op_dict = chosen_op_data.to_dict("records")[0]

operator_name = chosen_op_dict["name_translated"]
operator_rank = chosen_op_dict["rarity"]
is_low_rank = operator_rank in (1, 2, 3)
e0_art = chosen_op_dict["Elite 0"]
e1_art = chosen_op_dict["Elite 1"]
e2_art = chosen_op_dict["Elite 2"]
# op_default_color = chosen_op_data["color"].iloc[0]
op_default_color = "#63B3B0"

# Default artwork for fore and background
foreground_art = e0_art
background_art = e2_art if e2_art != "" else e0_art

# Calculate available elite artwork and skins
art_choices = [artwork for artwork in ("Elite 0", "Elite 1", "Elite 2") if chosen_op_dict[artwork] != ""]
skin_names = list(chosen_op_dict["skins"].keys())
art_choices.extend(skin_names)

# Foreground art must always be selected
# fg_art_choices = art_choices[:-1]

# Choose the fore and background art individually
foreground_art = st.selectbox(
    "Which art do you want in the front?",
    art_choices
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
custom_op_color = st.color_picker("Feel free to change the operator theme color", op_default_color)

# Put together relevant operator information in a single dictionary
operator_info = {
    "Elite 0": e0_art,
    "Elite 1": e1_art,
    "Elite 2": e2_art,
    "skins": chosen_op_dict["skins"],
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
wallpaper_gen.generate(
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