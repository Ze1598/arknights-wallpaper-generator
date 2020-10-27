from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os
import utils

DIMENSIONS = (640, 1280)
E2_ALPHA = 0.8
SHADOW_OFFSET = 15


def main(img_name: str, foreground_art: str, background_art: str, operator_color: str) -> None:
    """Given the necessary information, create a wallpaper for the operator using PIL.
    """
    # Create a new RGBA image
    wip_img = Image.new("RGBA", DIMENSIONS)
    draw = ImageDraw.Draw(wip_img)

    # Verify that the operator has E2 art (rather, there's an URL for it)
    # has_e2_img = str(background_art) != "nan"
    ignore_bg_image = background_art == ""

    # Load the background
    bg_path = os.path.join("static", "resources", "bg.png")
    bg = Image.open(bg_path, mode="r").convert("RGBA")

    # Load E2 image if there is one
    if ignore_bg_image != True:
        res = requests.get(background_art)
        e2_img = Image.open(BytesIO(res.content), mode="r").convert("RGBA")
        # Change the image's opacity
        e2_img = utils.change_alpha(e2_img, E2_ALPHA)
        # Resize the image
        e2_img = utils.resize_img(e2_img, 1.05)
        # Center the E2 image horizontally
        e2_coords = utils.calculate_e2_coordinates(e2_img, DIMENSIONS)

    # Load E0 image
    res = requests.get(foreground_art)
    e0_img = Image.open(BytesIO(res.content), mode="r").resize(
        (1024, 1024)).convert("RGBA")
    # Calculate the drawing coordinates for the E0 image
    e0_coords = utils.calculate_e0_coordinates(e0_img, DIMENSIONS)
    
    # Create the E0 image shadow
    shadow = Image.new("RGBA", e0_img.size, color=operator_color)
    # Calculate the drawing coordinates for the E0 image shadow
    shadow_coords = [coord+SHADOW_OFFSET for coord in e0_coords]

    # Add the background
    wip_img.paste(bg)
    # Add the colored footer polygon
    utils.create_and_paste_footer(wip_img, operator_color)
    # Add the E2 image if there is one
    if ignore_bg_image != True:
        wip_img.paste(e2_img, e2_coords, mask=e2_img)
    # Add the E0 image shadow
    wip_img.paste(shadow, shadow_coords, mask=e0_img)
    # Add the E0 image
    wip_img.paste(e0_img, e0_coords, mask=e0_img)
    # Save the resulting wallpaper
    wip_img.save(img_name)


if __name__ == "__main__":
    main(
        "Ch'en.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_0.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_2.png",
        "#616CAE"
    )
