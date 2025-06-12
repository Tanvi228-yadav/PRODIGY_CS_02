import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import random
import os

class ImageEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool - PRODIGY_CS_02")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.original_image = None
        self.processed_image = None
        self.current_image_path = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="Image Encryption Tool", 
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Control frame
        control_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File operations
        file_frame = tk.Frame(control_frame, bg='#34495e')
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            file_frame, 
            text="Select Image", 
            command=self.load_image,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            file_frame, 
            text="Save Result", 
            command=self.save_image,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            file_frame, 
            text="Reset", 
            command=self.reset_image,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Encryption controls
        encrypt_frame = tk.Frame(control_frame, bg='#34495e')
        encrypt_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Method selection
        tk.Label(
            encrypt_frame, 
            text="Encryption Method:", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        self.method_var = tk.StringVar(value="pixel_shuffle")
        method_combo = ttk.Combobox(
            encrypt_frame, 
            textvariable=self.method_var,
            values=["pixel_shuffle", "math_operation"],
            state="readonly",
            width=15
        )
        method_combo.pack(side=tk.LEFT, padx=5)
        
        # Key input
        tk.Label(
            encrypt_frame, 
            text="Key:", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.key_var = tk.StringVar(value="12345")
        key_entry = tk.Entry(
            encrypt_frame, 
            textvariable=self.key_var,
            width=10,
            font=("Arial", 10)
        )
        key_entry.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        tk.Button(
            encrypt_frame, 
            text="Encrypt", 
            command=self.encrypt_image,
            bg='#f39c12',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            encrypt_frame, 
            text="Decrypt", 
            command=self.decrypt_image,
            bg='#9b59b6',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Image display frame
        display_frame = tk.Frame(self.root, bg='#2c3e50')
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Original image
        original_frame = tk.Frame(display_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            original_frame, 
            text="Original Image", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 12, "bold")
        ).pack(pady=5)
        
        self.original_label = tk.Label(original_frame, bg='#34495e')
        self.original_label.pack(expand=True)
        
        # Processed image
        processed_frame = tk.Frame(display_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            processed_frame, 
            text="Processed Image", 
            bg='#34495e', 
            fg='#ecf0f1',
            font=("Arial", 12, "bold")
        ).pack(pady=5)
        
        self.processed_label = tk.Label(processed_frame, bg='#34495e')
        self.processed_label.pack(expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - Select an image to begin")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg='#34495e',
            fg='#ecf0f1'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image_path = file_path
                self.processed_image = None
                
                # Display original image
                self.display_image(self.original_image, self.original_label)
                
                # Clear processed image
                self.processed_label.configure(image='')
                self.processed_label.image = None
                
                self.status_var.set(f"Loaded: {os.path.basename(file_path)} ({self.original_image.size[0]}x{self.original_image.size[1]})")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.status_var.set("Error loading image")
    
    def display_image(self, image, label):
        # Resize image to fit display while maintaining aspect ratio
        display_size = (350, 350)
        image_copy = image.copy()
        image_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image_copy)
        label.configure(image=photo)
        label.image = photo
    
    def get_key(self):
        try:
            key = int(self.key_var.get())
            if key <= 0:
                raise ValueError("Key must be positive")
            return key
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer key")
            return None
    
    def pixel_shuffle_encrypt(self, image, key):
        """Encrypt image by shuffling pixels based on key"""
        # Convert to numpy array
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # Create list of pixel coordinates
        coordinates = [(i, j) for i in range(height) for j in range(width)]
        
        # Shuffle coordinates using key as seed
        random.seed(key)
        shuffled_coords = coordinates.copy()
        random.shuffle(shuffled_coords)
        
        # Create new image array
        new_array = np.zeros_like(img_array)
        
        # Map original coordinates to shuffled coordinates
        for idx, (orig_coord) in enumerate(coordinates):
            new_coord = shuffled_coords[idx]
            new_array[new_coord[0], new_coord[1]] = img_array[orig_coord[0], orig_coord[1]]
        
        return Image.fromarray(new_array.astype('uint8'))
    
    def pixel_shuffle_decrypt(self, image, key):
        """Decrypt image by reversing pixel shuffle"""
        # Convert to numpy array
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # Create list of pixel coordinates
        coordinates = [(i, j) for i in range(height) for j in range(width)]
        
        # Shuffle coordinates using same key and seed
        random.seed(key)
        shuffled_coords = coordinates.copy()
        random.shuffle(shuffled_coords)
        
        # Create new image array
        new_array = np.zeros_like(img_array)
        
        # Reverse the mapping
        for idx, (orig_coord) in enumerate(coordinates):
            shuffled_coord = shuffled_coords[idx]
            new_array[orig_coord[0], orig_coord[1]] = img_array[shuffled_coord[0], shuffled_coord[1]]
        
        return Image.fromarray(new_array.astype('uint8'))
    
    def math_operation_encrypt(self, image, key):
        """Encrypt image by adding key to pixel values"""
        img_array = np.array(image, dtype=np.int16)
        
        # Add key to all pixel values
        encrypted_array = (img_array + key) % 256
        
        return Image.fromarray(encrypted_array.astype('uint8'))
    
    def math_operation_decrypt(self, image, key):
        """Decrypt image by subtracting key from pixel values"""
        img_array = np.array(image, dtype=np.int16)
        
        # Subtract key from all pixel values
        decrypted_array = (img_array - key) % 256
        
        return Image.fromarray(decrypted_array.astype('uint8'))
    
    def encrypt_image(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        key = self.get_key()
        if key is None:
            return
        
        try:
            method = self.method_var.get()
            
            if method == "pixel_shuffle":
                self.processed_image = self.pixel_shuffle_encrypt(self.original_image, key)
                method_name = "Pixel Shuffle"
            elif method == "math_operation":
                self.processed_image = self.math_operation_encrypt(self.original_image, key)
                method_name = "Math Operation"
            
            self.display_image(self.processed_image, self.processed_label)
            self.status_var.set(f"Encrypted using {method_name} with key {key}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            self.status_var.set("Encryption failed")
    
    def decrypt_image(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # Use processed image if available, otherwise use original
        source_image = self.processed_image if self.processed_image else self.original_image
        
        key = self.get_key()
        if key is None:
            return
        
        try:
            method = self.method_var.get()
            
            if method == "pixel_shuffle":
                self.processed_image = self.pixel_shuffle_decrypt(source_image, key)
                method_name = "Pixel Shuffle"
            elif method == "math_operation":
                self.processed_image = self.math_operation_decrypt(source_image, key)
                method_name = "Math Operation"
            
            self.display_image(self.processed_image, self.processed_label)
            self.status_var.set(f"Decrypted using {method_name} with key {key}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
            self.status_var.set("Decryption failed")
    
    def save_image(self):
        if not self.processed_image:
            messagebox.showwarning("Warning", "No processed image to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                self.status_var.set("Save failed")
    
    def reset_image(self):
        if self.original_image:
            self.processed_image = None
            self.processed_label.configure(image='')
            self.processed_label.image = None
            self.status_var.set("Reset - Original image restored")
        else:
            self.status_var.set("No image to reset")

def main():
    root = tk.Tk()
    app = ImageEncryptor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
