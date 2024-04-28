import streamlit as st
from PIL import Image
import tempfile
import os


def resize_image(image, target_size):
    return image.resize(target_size)

def place_image_on_background(background_image, overlay_images, target_size=(1142, 552), margin=50):
    background = background_image
    
    # Create a blank image with the size of the background
    composite = background.copy()
    res = []
    # Calculate center position for each overlay image and place it on the background
    for overlay_image in overlay_images:
        composite = 0
        composite = background.copy()
        overlay = overlay_image
        resized_overlay = resize_image(overlay, target_size)
        bg_width, bg_height = background.size
        overlay_width, overlay_height = resized_overlay.size
        center_x = (bg_width - overlay_width) // 2
        center_y = (bg_height - overlay_height) // 2
        composite.paste(resized_overlay, (center_x, center_y), resized_overlay)
        res.append(composite)
    return res

def load_background_image(default_image_filename="BG.png"):
    uploaded_bg_image = st.file_uploader("Upload background image", type=["jpg", "png"])
    if uploaded_bg_image is not None:
        return Image.open(uploaded_bg_image)
    else:
        default_image_path = os.path.join(os.path.dirname(__file__), default_image_filename)
        return Image.open(default_image_path)

def main():
    st.title("Image Composition App")

    # Upload background image
    # bg_image = st.file_uploader("Upload background image", type=["jpg", "png"])
    bg_image = load_background_image()

    if bg_image:
        bg_image = bg_image
        #st.image(bg_image, caption="Background Image", use_column_width=True)

        # Upload multiple overlay images at once
        uploaded_overlay_images = st.file_uploader("Upload overlay images (up to 4)", type=["jpg", "png"], accept_multiple_files=True)

        if uploaded_overlay_images:
            overlay_images = [Image.open(overlay_image) for overlay_image in uploaded_overlay_images]
            st.subheader("Composite Images:")
            composite_images = place_image_on_background(bg_image, overlay_images)
            for composite_image in composite_images:
                st.image(composite_image, caption="Composite Image", use_column_width=True, output_format='PNG')
       


if __name__ == "__main__":
    main()
