# Image Encryption Tool - PRODIGY_CS_02

A Python-based image encryption tool that uses pixel manipulation techniques to encrypt and decrypt images.

## Features

- **Two Encryption Methods:**
  - **Pixel Shuffle**: Scrambles pixel locations based on a numerical key
  - **Math Operation**: Adds/subtracts a key value to each pixel's RGB values

- **User-Friendly GUI:**
  - Load and preview images
  - Select encryption method
  - Enter encryption key
  - Encrypt/decrypt images
  - Save processed images
  - Reset functionality

- **Key-Based Security:**
  - Uses positive integer keys for encryption
  - Same key required for decryption
  - Deterministic encryption/decryption

## Requirements

- Python 3.x
- Pillow (PIL)
- NumPy
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Usage

1. Run the application:
   \`\`\`bash
   python pixel_encryptor.py
   \`\`\`

2. Using the GUI:
   - Click "Select Image" to load an image file
   - Choose encryption method (Pixel Shuffle or Math Operation)
   - Enter a positive integer key
   - Click "Encrypt" to encrypt the image
   - Click "Decrypt" to decrypt the image
   - Click "Save Result" to save the processed image
   - Click "Reset" to clear the processed image

## Encryption Methods

### Pixel Shuffle
- Scrambles pixel positions based on the key
- Uses the key as a seed for random number generation
- Maintains image colors but changes pixel locations
- Reversible with the same key

### Math Operation
- Adds the key value to each pixel's RGB values
- Uses modulo 256 to keep values in valid range
- Changes image colors and appearance
- Reversible by subtracting the same key

## Security Note

This tool is designed for educational purposes and basic image obfuscation. For serious security applications, consider using established cryptographic libraries and algorithms.

## License

Apache License, Version 2.0, January 2004
