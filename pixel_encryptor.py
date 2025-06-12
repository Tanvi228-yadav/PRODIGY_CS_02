import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import random

def pixel_shuffle(img_arr, key, mode):
    random.seed(key)
    h, w, c = img_arr.shape
    total = h * w
    idxs = list(range(total))
    random.shuffle(idxs)
    flat = img_arr.reshape((-1, c)).copy()
    if mode == "encrypt":
        shuffled = flat[idxs]
    else:
        # Build inverse mapping for decryption
        inv = np.zeros_like(idxs)
        for i, idx in enumerate(idxs):
            inv[idx] = i
        shuffled = flat[inv]
    return shuffled.reshape((h, w, c))

def math_op(img_arr, key, mode):
    if mode == "encrypt":
        result = (img_arr + key) % 256
    else:
        result = (img_arr - key) % 256
    return result.astype(np.uint8)

class PixelEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Shuffle & Math Encryptor")
        self.root.geometry("750x580")
        self.root.configure(bg="#181824")
        self.img_path = None
        self.original_img = None
        self.processed_img = None

        # Title
        title = tk.Label(root, text="🧩 Pixel Shuffle & Math Encryptor 🧩", font=("Arial", 22, "bold"), fg="#2EE59D", bg="#181824")
        title.pack(pady=10)

        # Image preview
        self.img_panel = tk.Label(root, bg="#23232b", width=320, height=210, relief="ridge", bd=4)
        self.img_panel.pack(pady=10)

        # Image info
        self.info_label = tk.Label(root, text="No image selected.", font=("Arial", 12, "italic"), bg="#181824", fg="#E0E0E0")
        self.info_label.pack()

        # Controls
        control_frame = tk.Frame(root, bg="#181824")
        control_frame.pack(pady=15)

        tk.Label(control_frame, text="Key (Integer):", font=("Arial", 12), bg="#181824", fg="#E0E0E0").grid(row=0, column=0, padx=6, pady=4)
        self.key_entry = tk.Entry(control_frame, width=10, font=("Arial", 12))
        self.key_entry.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(control_frame, text="Method:", font=("Arial", 12), bg="#181824", fg="#E0E0E0").grid(row=0, column=2, padx=6, pady=4)
        self.method_var = tk.StringVar(value="shuffle")
        tk.Radiobutton(control_frame, text="Pixel Shuffle", variable=self.method_var, value="shuffle", font=("Arial", 12), bg="#181824", fg="#E0E0E0", selectcolor="#23232b").grid(row=0, column=3, padx=6)
        tk.Radiobutton(control_frame, text="Math Operation", variable=self.method_var, value="math", font=("Arial", 12), bg="#181824", fg="#E0E0E0", selectcolor="#23232b").grid(row=0, column=4, padx=6)

        # Buttons
        btn_frame = tk.Frame(root, bg="#181824")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Select Image", command=self.select_image, font=("Arial", 13), bg="#2EE59D", fg="#181824").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frame, text="Encrypt", command=lambda: self.process("encrypt"), font=("Arial", 13), bg="#2EE59D", fg="#181824").pack(side=tk.LEFT, padx=12)
        tk.Button(btn_frame, text="Decrypt", command=lambda: self.process("decrypt"), font=("Arial", 13), bg="#2EE59D", fg="#181824").pack(side=tk.LEFT, padx=12)
        self.save_btn = tk.Button(btn_frame, text="Save Result", command=self.save_image, font=("Arial", 13), bg="#2EE59D", fg="#181824", state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=12)

        self.status_label = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#181824", fg="#2EE59D")
        self.status_label.pack(pady=8)

    def select_image(self):
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)
        if path:
            self.img_path = path
            img = Image.open(path).convert("RGB")
            self.original_img = img
            self.display_image(img)
            self.info_label.config(text=f"Selected: {os.path.basename(path)} | {img.size[0]}x{img.size[1]}")
            self.status_label.config(text="")
            self.save_btn.config(state=tk.DISABLED)

    def display_image(self, img):
        img_cpy = img.copy()
        img_cpy.thumbnail((320, 210))
        tk_img = ImageTk.PhotoImage(img_cpy)
        self.img_panel.config(image=tk_img)
        self.img_panel.image = tk_img

    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if key < 1:
                raise ValueError
            return key
        except Exception:
            messagebox.showerror("Invalid Key", "Please enter a positive integer as the key.")
            return None

    def process(self, mode):
        if self.original_img is None:
            messagebox.showwarning("No Image", "Please select an image first.")
            return
        key = self.get_key()
        if key is None:
            return
        img = self.original_img
        arr = np.array(img)
        method = self.method_var.get()
        if method == "shuffle":
            new_arr = pixel_shuffle(arr, key, mode)
        else:
            new_arr = math_op(arr, key, mode)
        out_img = Image.fromarray(new_arr)
        self.processed_img = out_img
        self.display_image(out_img)
        self.status_label.config(text=f"Image {mode.title()}ed using '{'Pixel Shuffle' if method == 'shuffle' else 'Math Operation'}'.")
        self.save_btn.config(state=tk.NORMAL)

    def save_image(self):
        if self.processed_img:
            filetypes = [("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
            if save_path:
                self.processed_img.save(save_path)
                messagebox.showinfo("Saved", f"Image saved as {save_path}")
                self.status_label.config(text="Image saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelEncryptorApp(root)
    root.mainloop()