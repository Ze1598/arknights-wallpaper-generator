import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
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
	data = pd.read_csv("static\\data\\operators_info.csv", na_values=[""])
	return data
@st.cache
def load_colors_csv():
	data = pd.read_csv("static\\data\\colors.csv", na_values=[""])
	return data
main_data = load_main_csv()
main_data.sort_values(by="name", inplace=True)
colors_data = load_colors_csv()
colors_data.sort_values(by="name", inplace=True)
operator_rank = st.selectbox("Choose the operator rank", ("6-star", "5-star", "4-star", "3-star", "2-star", "1-star"))

for star in range(1, 7):
	star = str(star)
	option = star + "-star"
	if operator_rank == option:
		filtered_data = main_data[main_data["num_stars"] == int(star)]

operator_chosen = st.selectbox("Choose your operator", filtered_data["name"].to_numpy())

chosen_op_data = main_data[main_data["name"] == operator_chosen]
chosen_op_color = colors_data[colors_data["name"] == operator_chosen]

# st.write(colors_data)
st.write(chosen_op_data["e1_img"].iloc[0], chosen_op_data["e2_img"].iloc[0], chosen_op_color["color"].iloc[0])

wallpaper_gen.main(
	chosen_op_data["e1_img"].iloc[0], 
	chosen_op_data["e2_img"].iloc[0],
	chosen_op_color["color"].iloc[0]
)
wallpaper_name = "wallpaper.png"
st.image(wallpaper_name, use_column_width=True)

encoded_img = utils.encode_img_to_b64(wallpaper_name)
href = f'<a href="data:image/png;base64,{encoded_img}" download="{wallpaper_name}">Download the graphic</a>'
st.markdown(href, unsafe_allow_html=True)
# Delete the graphic from the server
os.remove(wallpaper_name)

# st.table(data)

# TODO: add 050505 to the footer color
# TODO: fix error from w/che/magallan/...