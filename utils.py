import os
from PIL import Image, ImageEnhance, ImageDraw
from typing import List
import base64
import streamlit as st


def change_alpha(img: Image.Image, opacity: float) -> Image.Image:
    """Change the opacity of an image.
    # https://gist.github.com/blippy/a385dc77f9d74e4876d5
    """
    # Get the alpha channel
    alpha = img.getchannel("A")
    # Adjust the brightness of the alpha channel to the desired opacity level
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    # Instead of changing the image's alpha channel value, update it with\
    # an already transformed image channel
    img.putalpha(alpha)

    return img


def resize_img(img: Image.Image, factor: float) -> Image.Image:
    """Resize an image.
    """
    # Make sure the image is in the default dimensions and is RGBA
    img = img.resize((1024, 1024)).convert("RGBA")
    
    # Calculate new dimensions
    img_dims = img.size
    img_dims = [int(dim*factor) for dim in img_dims]
    
    # Finally resize the image, keeping it RGBA
    img = img.resize(img_dims).convert("RGBA")

    return img


def calculate_e2_coordinates(e2_img: Image.Image, img_dims: List[int]) -> List[int]:
    """Calculate the coordinates at which to draw the E2 image.
    """
    # Lis of coordinates (the Y/height coordinate won't change)
    e2_coords = [None, -100]
    # The X/width coordinate is horizontally-aligned
    e2_img_dims = e2_img.size
    e2_coords[0] = (img_dims[0] - e2_img_dims[0]) // 2

    return e2_coords


def calculate_e1_coordinates(e1_img: Image.Image, img_dims: List[int]) -> List[int]:
    """Calculate the coordinates at which to draw the E1 image.
    """
    # Both coordinates will change
    e1_coords = [None, None]
    e1_img_dims = e1_img.size
    # The X/width is horizontally-aligned
    e1_coords[0] = (img_dims[0] - e1_img_dims[0]) // 2
    # The Y/height is bottom-aligned
    e1_coords[1] = img_dims[1] - e1_img_dims[1]

    return e1_coords


def increment_footer_color(operator_color: str) -> str:
    """Increment the most saturated RGB channel of the operator color to create the footer block color.
    If more than one channels have the most saturation, then those are all updated.
    """
    # Increment by this percentage
    update_delta = 0.20
    # Get the individual RGB channels
    channels = [
        int(operator_color[1:3], 16),
        int(operator_color[3:5], 16),
        int(operator_color[5:], 16)
    ]
    # String to hold the final color
    new_color = "0x"
    # Loop through the color channels to update the most saturated one(s),\
    # adding the result to the running string
    for value in channels:
        # Only update the channel if it is (one of) the most saturated and\
        # it is not already at max saturation
        if (max(channels) == value) and (value != 255):
            updated_channel = int(value * (1+update_delta))
            # Clip the saturation to the maximum value possible
            if updated_channel > 255:
                updated_channel = 255
            # Don't add the initial "0x" characters to the string
            hex_channel = hex(updated_channel)[2:]
            new_color += hex_channel
        # Otherwise, add the color as is
        else:
            hex_conv = hex(value)[2:]
            # In case the channel add a leading 0, make sure it is kept
            if len(hex_conv) == 1:
                hex_conv = "0" + hex_conv
            new_color += hex_conv

    # If the resulting hexadecimal is still a valid hex color (i.e., a\
    # positive hex value), use it, otherwise the new color will simply be black
    if int(new_color, 16) < int("0x000", 16):
        new_color = "0xFFF"
    # Replace Python's "0x" notation with a proper pound symbol
    new_color = new_color.replace("0x", "#")
    return new_color


def create_and_paste_footer(img: Image.Image, operator_color: str) -> None:
    """Draw the footer in a new image and save it, load it, and paste it into the working image.
    The footer image is deleted at the end of the operation.
    """
    # Create a new image for the footer
    img_dims = img.size
    footer_img = Image.new("RGBA", img_dims)
    d = ImageDraw.Draw(footer_img)

    # Draw the footer polygon
    footer_coords = [(0, 1100), (640, 1000), (640, 1280), (0, 1280)]
    footer_color = increment_footer_color(operator_color)
    d.polygon(footer_coords, fill=footer_color)

    # Save the temporary footer image
    footer_img_name = "footer.png"
    footer_img.save(footer_img_name)

    # Load the footer image
    footer_img = Image.open(footer_img_name, "r").convert("RGBA")
    footer_img = change_alpha(footer_img, 0.7)
    # And paste it into the working image
    img.paste(footer_img, (0, 0), mask=footer_img)

    # Delete the footer image at the end
    os.remove(footer_img_name)


def encode_img_to_b64(img_name: str) -> bytes:
    """Given the name of a image file, load it in bytes mode, and convert it to a base 64 bytes object.
    """
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/19
    with open(img_name, "rb") as f:
        img = f.read()
        encoded_img = base64.b64encode(img).decode()

    return encoded_img
