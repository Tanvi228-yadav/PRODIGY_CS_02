# PRODIGY_CS_02

Develop a simple image encryption tool using pixel manipulation. You can perform operations like swapping pixel values or applying a basic mathematical operation to each pixel. Allow users to encrypt and decrypt images.

## Features

- Encrypt and decrypt images using:
  - Pixel Shuffle (scrambles pixel locations based on a key)
  - Math Operation (adds/subtracts a key value to each pixel's RGB values)
- Key-based encryption and decryption
- User-friendly GUI to select, preview, encrypt, decrypt, and save images

## Requirements

- Python 3.x
- Pillow (`pip install pillow`)
- NumPy (`pip install numpy`)

## Usage

1. Clone or download this repository.

2. Install dependencies:

   ```
   pip install pillow numpy
   ```

3. Run the tool:

   ```
   python pixel_encryptor.py
   ```

4. Use the GUI to:
   - Select an image
   - Choose an encryption method
   - Enter a key (positive integer)
   - Encrypt or decrypt your image
   - Save the result

## License

Apache License, Version 2.0, January 2004
See [LICENSE](LICENSE) for details.