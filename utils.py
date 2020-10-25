import os
from PIL import Image, ImageEnhance, ImageDraw
from typing import List
import base64
import streamlit as st

E2_COORDS = [None, -100]

# https://gist.github.com/blippy/a385dc77f9d74e4876d5


def change_alpha(img: Image.Image, opacity: float) -> Image.Image:
    """Change the opacity of an image.
    """
    # Get the alpha channel
    alpha = img.getchannel("A")
    # Adjust the brightness of the alpha channel to the desired opacity level
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    # Instead of changing the image's alpha channel directly, update it with\
    # an already transformed image channel
    img.putalpha(alpha)

    return img


def resize_img(img: Image.Image, factor: float) -> Image.Image:
    """Resize an image.
    """
    img = img.resize((1024, 1024)).convert("RGBA")
    # Calculate new dimensions
    img_dims = img.size
    img_dims = [int(dim*factor) for dim in img_dims]
    # Resize E2 image
    img = img.resize(img_dims).convert("RGBA")

    return img


def calculate_e2_coordinates(e2_img, img_dims) -> List[int]:
    """Calculate the coordinates at which to draw the E2 image.
    """
    e2_img_dims = e2_img.size
    E2_COORDS[0] = (img_dims[0] - e2_img_dims[0]) // 2

    return E2_COORDS


def calculate_e1_coordinates(e1_img, img_dims) -> List[int]:
    """Calculate the coordinates at which to draw the E1 image.
    """
    e1_coords = [0, 0]
    e1_img_dims = e1_img.size
    e1_coords[0] = (img_dims[0] - e1_img_dims[0]) // 2
    e1_coords[1] = img_dims[1] - e1_img_dims[1]

    return e1_coords


def increment_footer_color(operator_color: str, color_delta: str) -> str:
    """Increment the hexadecimal operator color using another color.
    """
    update_delta = 0.20
    st.write(operator_color, int(operator_color[1:3], 16))
    channels = [
        int(operator_color[1:3], 16), 
        int(operator_color[3:5], 16), 
        int(operator_color[5:], 16)
    ]
    st.write(channels)
    new_color = "0x"
    st.write("max channels", max(channels))
    for value in channels:
        st.write(max(channels), value, max(channels) == value)
        if (max(channels) == value) and (value != 255):
            updated_channel = int(value * (1+update_delta))
            if updated_channel > 255:
                updated_channel = 255
            st.write("updated_ channel:", updated_channel, hex(updated_channel))
            hex_channel = hex(updated_channel)[2:]
            st.write("hex channel", hex_channel)
            new_color += hex_channel
        else:
            hex_conv = hex(value)[2:]
            if len(hex_conv) == 1:
                hex_conv = "0" + hex_conv
            new_color += hex_conv
        st.write("wip string", new_color)

    # operator_color = operator_color.replace("#", "0x")
    # footer_color = hex(int(operator_color, 16) - int(color_delta, 16))
    # if int(footer_color, 16) < int("0x000", 16):
    st.write(new_color)
    if int(new_color, 16) < int("0x000", 16):
        new_color = "0xFFF"
    new_color = new_color.replace("0x", "#")
    return new_color


def create_and_paste_footer(img: Image.Image, operator_color: str) -> None:
    """Draw the footer in a new image and save it, load it, and paste it into the working image.
    The footer image is deleted at the end.
    """
    # Create a new image for the footer
    img_dims = img.size
    footer_img = Image.new("RGBA", img_dims)
    d = ImageDraw.Draw(footer_img)

    # Draw the footer polygon
    footer_coords = [(0, 1100), (640, 1000), (640, 1280), (0, 1280)]
    footer_color_delta = "0x050505"
    footer_color = increment_footer_color(operator_color, footer_color_delta)
    d.polygon(footer_coords, fill=footer_color)
    # Save the temporary footer image
    footer_img_name = "footer.png"
    footer_img.save(footer_img_name)

    # Load the footer image
    footer_img = Image.open(footer_img_name, "r").convert("RGBA")
    footer_img = change_alpha(footer_img, 0.7)
    # And paste it into the working image
    img.paste(footer_img, (0, 0), mask=footer_img)

    os.remove(footer_img_name)


def encode_img_to_b64(img_name: str) -> bytes:
    """Given the name of a image file, load it in bytes mode, and convert it to a base 64 bytes object.
    """
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/19
    with open(img_name, "rb") as f:
        img = f.read()
        encoded_img = base64.b64encode(img).decode()

    return encoded_img
