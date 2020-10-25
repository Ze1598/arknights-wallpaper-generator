from PIL import Image, ImageDraw
import requests
from io import BytesIO
import utils

DIMENSIONS = (640, 1280)
E2_ALPHA = 0.8
SHADOW_OFFSET = 15

def main(e1_img_url, e2_img_url, operator_color):
	# Create a new RGBA image
	wip_img = Image.new("RGBA", DIMENSIONS)
	draw = ImageDraw.Draw(wip_img)

	has_e2_img = str(e2_img_url) != "nan"

	# Load the background
	bg = Image.open("static\\resources\\bg.png", mode="r").convert("RGBA")
	# Load E2 image
	"""
	e2_img = Image.open("exusiai_e2.png", mode="r").convert("RGBA")
	e2_img = Image.open("siege_e2.png", mode="r").convert("RGBA")
	e2_img = Image.open("rosa_e2.png", mode="r").convert("RGBA")
	"""
	if has_e2_img == True:
		res = requests.get(e2_img_url)
		e2_img = Image.open(BytesIO(res.content), mode="r").convert("RGBA")
		# Change the image's opacity
		e2_img = utils.change_alpha(e2_img, E2_ALPHA)
		# Resize the image
		e2_img = utils.resize_img(e2_img, 1.05)
		# Center the E2 image horizontally
		e2_coords = utils.calculate_e2_coordinates(e2_img, DIMENSIONS)

	# Load E1 image
	"""
	e1_img = Image.open("exusiai.png", mode="r").resize((1024, 1024)).convert("RGBA")
	e1_img = Image.open("siege.png", mode="r").resize((1024, 1024)).convert("RGBA")
	e1_img = Image.open("rosa.png", mode="r").resize((1024, 1024)).convert("RGBA")
	"""
	res = requests.get(e1_img_url)
	e1_img = Image.open(BytesIO(res.content), mode="r").resize((1024, 1024)).convert("RGBA")
	# Calculate the drawing coordinates for the E1 image
	e1_coords = utils.calculate_e1_coordinates(e1_img, DIMENSIONS)
	shadow_coords = [coord+SHADOW_OFFSET for coord in e1_coords]

	# Add the background
	wip_img.paste(bg)
	# Add the colored footer polygon
	utils.create_and_paste_footer(wip_img, operator_color)
	if has_e2_img == True:
		wip_img.paste(e2_img, e2_coords, mask=e2_img)
	# Add the E1 image shadow
	shadow = Image.new("RGBA", e1_img.size, color=operator_color)
	wip_img.paste(shadow, shadow_coords, mask=e1_img)
	# Add the E1 image
	wip_img.paste(e1_img, e1_coords, mask=e1_img)
	# Save the resulting wallpaper
	wip_img.save("wallpaper.png")

if __name__ == "__main__":
	main(
		"https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_0.png",
		"https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_2.png",
		"#616CAE"
	)