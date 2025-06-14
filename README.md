# PRODIGY_CS_02

A powerful image encryption tool with pixel shuffle and color math modes!

---

🚀 **Live Demo:** [https://prodigy-cs-02-3.onrender.com](https://prodigy-cs-02-3.onrender.com)

---

## Features

- Encrypt and decrypt images using two unique methods:
  - **Pixel Shuffle:** Scrambles image pixels using a numeric key for secure, reversible encryption.
  - **Math Operation:** Alters pixel colors by mathematically shifting RGB values with a key.
- User-friendly web interface for easy image upload, preview, and processing.
- Key-based security: use the same number key for both encryption and decryption.
- Supports saving and resetting your processed images.
- Deterministic results: the same key always produces the same output.

---

## How It Works

1. **Upload an image** via the web interface.
2. **Choose your encryption method**: Pixel Shuffle or Math Operation.
3. **Enter a positive integer key** for encryption/decryption.
4. **Encrypt or decrypt** your image with a click.
5. **Save or reset** your result as needed.

---

## Tech Stack

- Python 3.x
- Pillow (PIL)
- NumPy
- Flask (for the web app interface)

---

## Security Note

This tool is designed for educational purposes and simple image obfuscation. For production security, always use established cryptography libraries.

---

## License

Apache License, Version 2.0, January 2004

---
