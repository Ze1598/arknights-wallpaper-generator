import streamlit as st
import pandas as pd
import numpy as np
import os
import wallpaper_gen
import utils

st.markdown("""
# Arknights Phone Wallpaper Generator

Create phone wallpapers for your favourite Arknights operators!

If you're interested in the code, you can find it on my GitHub repository [here]().

For feedback, feel free to reach out to me on Twitter [@ze1598]().
""")


@st.cache
def load_main_csv():
    """Load the main CSV of operator names and promotion images' URLs.
    This function exists so the data can be cached.
    """
    csv_path = os.path.join("static", "data", "operators_info.csv")
    data = pd.read_csv(csv_path, na_values=[""])
    return data


@st.cache
def load_colors_csv():
    """Load the CSV of operator names and theme colors.
    This function exists so the data can be cached.
    """
    csv_path = os.path.join("static", "data", "colors.csv")
    data = pd.read_csv(csv_path, na_values=[""])
    return data

# Load the necessary data and sort it by alphabetical order of names
main_data = load_main_csv()
colors_data = load_colors_csv()
main_data.sort_values(by="name", inplace=True)
colors_data.sort_values(by="name", inplace=True)

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
chosen_op_color = colors_data[colors_data["name"] == operator_chosen]

# Create the wallpaper name string
wallpaper_name = chosen_op_data["name"].iloc[0] + ".png"
# Generator the wallpaper
wallpaper_gen.main(
    wallpaper_name,
    chosen_op_data["e1_img"].iloc[0],
    chosen_op_data["e2_img"].iloc[0],
    chosen_op_color["color"].iloc[0]
)
# Display the wallpaper
st.image(wallpaper_name, use_column_width=True)
# Encoded the image to bytes so a download link can be created
encoded_img = utils.encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
# Create the download link
st.markdown(href, unsafe_allow_html=True)

# Delete the graphic from the server
os.remove(wallpaper_name)
