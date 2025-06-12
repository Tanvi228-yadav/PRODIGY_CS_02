import streamlit as st
from PIL import Image
import numpy as np
import random
import io

st.set_page_config(page_title="Image Encryption Tool - PRODIGY_CS_02", layout="wide")

st.title("Image Encryption Tool - PRODIGY_CS_02")
st.markdown(
    """
    **Encrypt and decrypt images using pixel manipulation.**
    - Choose your image.
    - Select encryption method.
    - Set a key.
    - Encrypt or decrypt!
    """
)

# Functions

def pixel_shuffle_encrypt(image, key):
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    coordinates = [(i, j) for i in range(height) for j in range(width)]
    random.seed(key)
    shuffled_coords = coordinates.copy()
    random.shuffle(shuffled_coords)
    new_array = np.zeros_like(img_array)
    for idx, (orig_coord) in enumerate(coordinates):
        new_coord = shuffled_coords[idx]
        new_array[new_coord[0], new_coord[1]] = img_array[orig_coord[0], orig_coord[1]]
    return Image.fromarray(new_array.astype('uint8'))

def pixel_shuffle_decrypt(image, key):
    img_array = np.array(image)
    height, width = img_array.shape[:2]
    coordinates = [(i, j) for i in range(height) for j in range(width)]
    random.seed(key)
    shuffled_coords = coordinates.copy()
    random.shuffle(shuffled_coords)
    new_array = np.zeros_like(img_array)
    for idx, (orig_coord) in enumerate(coordinates):
        shuffled_coord = shuffled_coords[idx]
        new_array[orig_coord[0], orig_coord[1]] = img_array[shuffled_coord[0], shuffled_coord[1]]
    return Image.fromarray(new_array.astype('uint8'))

def math_operation_encrypt(image, key):
    img_array = np.array(image, dtype=np.int16)
    encrypted_array = (img_array + key) % 256
    return Image.fromarray(encrypted_array.astype('uint8'))

def math_operation_decrypt(image, key):
    img_array = np.array(image, dtype=np.int16)
    decrypted_array = (img_array - key) % 256
    return Image.fromarray(decrypted_array.astype('uint8'))

# Sidebar controls
st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader("Select Image", type=["jpg", "jpeg", "png", "bmp", "tiff", "gif"])
method = st.sidebar.selectbox("Encryption Method", ["Pixel Shuffle", "Math Operation"])
key = st.sidebar.number_input("Key (positive integer)", min_value=1, value=12345, step=1)

action = st.sidebar.radio("Action", ["Encrypt", "Decrypt"])

# Main logic
if uploaded_file:
    try:
        original_image = Image.open(uploaded_file).convert("RGB")
    except Exception as e:
        st.error(f"Failed to load image: {str(e)}")
        st.stop()

    st.subheader("Original Image")
    st.image(original_image, use_column_width=True)

    processed_image = None
    method_name = ""
    if st.sidebar.button(f"{action} Image"):
        try:
            if method == "Pixel Shuffle":
                if action == "Encrypt":
                    processed_image = pixel_shuffle_encrypt(original_image, key)
                else:
                    processed_image = pixel_shuffle_decrypt(original_image, key)
                method_name = "Pixel Shuffle"
            elif method == "Math Operation":
                if action == "Encrypt":
                    processed_image = math_operation_encrypt(original_image, key)
                else:
                    processed_image = math_operation_decrypt(original_image, key)
                method_name = "Math Operation"
        except Exception as e:
            st.error(f"{action}ion failed: {str(e)}")

        if processed_image:
            st.subheader(f"{action}ed Image ({method_name})")
            st.image(processed_image, use_column_width=True)
            # Download button
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button(
                label="Download Result",
                data=byte_im,
                file_name=f"{action.lower()}ed_image.png",
                mime="image/png"
            )
else:
    st.info("Please upload an image file using the sidebar.")
