import streamlit as st
from PIL import Image

def resize_image(image, target_size):
    return image.resize(target_size)

def place_image_on_background(background, overlay, target_size=(1150, 550), margin=50):

    # Resize overlay image to the specified target size
    resized_overlay = resize_image(overlay, target_size)

    bg_width, bg_height = background.size
    overlay_width, overlay_height = resized_overlay.size

    # Calculate center position for the resized overlay image
    center_x = (bg_width - overlay_width) // 2
    center_y = (bg_height - overlay_height) // 2

    # Create a blank image with the size of the background
    composite = background.copy()

    # Paste resized overlay onto composite image
    composite.paste(resized_overlay, (center_x, center_y), resized_overlay)

    return composite

def main():
    st.title("Image Composition App")

    # Upload background image
    bg_image = st.file_uploader("Upload background image", type=["jpg", "png"])

    if bg_image:
        bg_image = Image.open(bg_image)
        st.image(bg_image, caption="Background Image", use_column_width=True)

        # Upload other images
        for i in range(4):
            uploaded_image = st.file_uploader(f"Upload image {i+1}", type=["jpg", "png"])
            if uploaded_image:
                uploaded_image = Image.open(uploaded_image)
                st.subheader(f"Composite Image {i+1}:")
                composite_image = place_image_on_background(bg_image, uploaded_image)
                st.image(composite_image, caption=f"Composite Image {i+1}", use_column_width=True, output_format='PNG')

if __name__ == "__main__":
    main()
