from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os
import utils

DIMENSIONS = (640, 1280)
E2_ALPHA = 0.8
SHADOW_OFFSET = 15


def main(img_name: str, e1_img_url: str, e2_img_url: str, operator_color: str) -> None:
    """Given the necessary information, create a wallpaper for the operator using PIL.
    """
    # Create a new RGBA image
    wip_img = Image.new("RGBA", DIMENSIONS)
    draw = ImageDraw.Draw(wip_img)

    # Verify that the operator has E2 art (rather, there's an URL for it)
    has_e2_img = str(e2_img_url) != "nan"

    # Load the background
    bg_path = os.path.join("static", "resources", "bg.png")
    bg = Image.open(bg_path, mode="r").convert("RGBA")

    # Load E2 image if there is one
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
    res = requests.get(e1_img_url)
    e1_img = Image.open(BytesIO(res.content), mode="r").resize(
        (1024, 1024)).convert("RGBA")
    # Calculate the drawing coordinates for the E1 image
    e1_coords = utils.calculate_e1_coordinates(e1_img, DIMENSIONS)
    
    # Create the E1 image shadow
    shadow = Image.new("RGBA", e1_img.size, color=operator_color)
    # Calculate the drawing coordinates for the E1 image shadow
    shadow_coords = [coord+SHADOW_OFFSET for coord in e1_coords]

    # Add the background
    wip_img.paste(bg)
    # Add the colored footer polygon
    utils.create_and_paste_footer(wip_img, operator_color)
    # Add the E2 image if there is one
    if has_e2_img == True:
        wip_img.paste(e2_img, e2_coords, mask=e2_img)
    # Add the E1 image shadow
    wip_img.paste(shadow, shadow_coords, mask=e1_img)
    # Add the E1 image
    wip_img.paste(e1_img, e1_coords, mask=e1_img)
    # Save the resulting wallpaper
    wip_img.save(img_name)


if __name__ == "__main__":
    main(
        "Ch'en.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_0.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_2.png",
        "#616CAE"
    )
