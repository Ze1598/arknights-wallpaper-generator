from PIL import Image, ImageDraw
import requests
from io import BytesIO
import os
import utils

DIMENSIONS = (640, 1280)
ART_ALPHA = 0.8
SHADOW_OFFSET = 15


def main(
    img_name: str, 
    foreground_art: str, 
    background_art: str,
    wallpaper_bg: str,
    operator_color: str
) -> None:
    """Given the necessary information, create a wallpaper for the operator using PIL.
    """
    # Create a new RGBA image
    wip_img = Image.new("RGBA", DIMENSIONS)

    # The operator may not have one of the arts, or the user chose to not use them
    ignore_bg_image = (background_art == "")
    ignore_fg_image = (foreground_art == "")
    # Is either of the options not being used?
    using_single_art = any((ignore_bg_image, ignore_fg_image))

    # Load the base image background
    if wallpaper_bg == "":
        bg_path = os.path.join("static", "resources", "bg.png")
    else:
        bg_path = wallpaper_bg
    bg = Image.open(bg_path, mode="r").convert("RGBA")

    # Load background art if there is one
    if ignore_bg_image != True:
        res = requests.get(background_art)
        bg_art, bg_art_coords = utils.prepare_loaded_bg_art(res, DIMENSIONS, ART_ALPHA)

    # Load foreground art if there is one
    if ignore_fg_image != True:
        # Load foreground art
        res = requests.get(foreground_art)
        # If we are using only foreground art, then center it
        if using_single_art == True:
            fg_art, fg_art_coords = utils.prepare_loaded_art(res, DIMENSIONS, "single")
        # Otherwise use the bottom alignment
        else:
            fg_art, fg_art_coords = utils.prepare_loaded_art(res, DIMENSIONS, "normal")

        # Create the foreground art shadow
        shadow = Image.new("RGBA", fg_art.size, color=operator_color)
        # Calculate the drawing coordinates for the foreground art shadow
        shadow_coords = [coord+SHADOW_OFFSET for coord in fg_art_coords]

    # Add the background
    wip_img.paste(bg)
    # Add the colored footer polygon
    utils.create_and_paste_footer(wip_img, operator_color)
    # Add the background art if there is one
    if ignore_bg_image != True:
        if using_single_art == True:
            # Add the background art shadow
            wip_img.paste(shadow, shadow_coords, mask=bg_art)
        wip_img.paste(bg_art, bg_art_coords, mask=bg_art)
    # Add the foreground art if there is one
    if ignore_fg_image != True:
        # Add the foreground art shadow
        wip_img.paste(shadow, shadow_coords, mask=fg_art)
        # Add the foreground art
        wip_img.paste(fg_art, fg_art_coords, mask=fg_art)
    # Save the resulting wallpaper
    wip_img.save(img_name)


if __name__ == "__main__":
    main(
        "Ch'en.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_0.png",
        "https://gamepress.gg/arknights/sites/arknights/files/2019-10/char_010_chen_1_2.png",
        "#616CAE"
    )
