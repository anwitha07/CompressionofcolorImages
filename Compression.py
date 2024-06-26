import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import os


# Function to open an image file
def open_image():
    global img_path, original_size, original_size_kb, resized_size, resized_size_kb
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.jpeg;.png;.bmp;*.tiff")])
    if img_path:
        img = cv2.imread(img_path)
        height, width = img.shape[:2]
        original_size = (width, height)
        original_size_kb = os.path.getsize(img_path) / 1024  # Size in KB
        resized_size = None  # Reset resized size
        resized_size_kb = None  # Reset resized size in KB
        update_size_labels()
        display_image(img)


# Function to resize the image to half
def resize_image():
    global resized_img, img_path, resized_size, resized_size_kb
    if img_path:
        img = cv2.imread(img_path)
        height, width = img.shape[:2]
        resized_img = cv2.resize(img, (width // 2, height // 2))
        resized_size = (width // 2, height // 2)

        # Save the resized image temporarily to calculate its size
        temp_path = os.path.join(os.path.dirname(img_path), "temp_resized_image.jpg")
        cv2.imwrite(temp_path, resized_img)
        resized_size_kb = os.path.getsize(temp_path) / 1024  # Size in KB
        os.remove(temp_path)  # Remove the temporary file

        update_size_labels()
        display_image(resized_img)
        save_image(resized_img)


# Function to display an image on the GUI
def display_image(img):
    b, g, r = cv2.split(img)
    img = cv2.merge((r, g, b))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    panel.config(image=imgtk)
    panel.image = imgtk


# Function to display resized image
def display_resized_image():
    if resized_img is not None:
        display_image(resized_img)
    else:
        messagebox.showerror("Error", "No image has been resized yet.")


# Function to save the resized image
def save_image(img):
    if img_path:
        directory, filename = os.path.split(img_path)
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(directory, f"{name}_resized{ext}")
        cv2.imwrite(save_path, img)
        messagebox.showinfo("Image Saved", f"Resized image saved as {save_path}")


# Function to update size labels
def update_size_labels():
    if original_size:
        original_size_label.config(
            text=f"Original Size: {original_size[0]}x{original_size[1]}, {original_size_kb:.2f} KB")
    else:
        original_size_label.config(text="Original Size: N/A")

    if resized_size:
        resized_size_label.config(text=f"Resized Size: {resized_size[0]}x{resized_size[1]}, {resized_size_kb:.2f} KB")
    else:
        resized_size_label.config(text="Resized Size: N/A")


# Initialize the main window
root = tk.Tk()
root.title("Image Resizer")

# Initialize global variables
img_path = None
original_size = None
original_size_kb = None
resized_img = None
resized_size = None
resized_size_kb = None

# Create buttons, labels, and image display panel
open_btn = tk.Button(root, text="Open Image", command=open_image)
resize_btn = tk.Button(root, text="Resize Image", command=resize_image)
display_btn = tk.Button(root, text="Display Resized Image", command=display_resized_image)
panel = tk.Label(root)
original_size_label = tk.Label(root, text="Original Size: N/A")
resized_size_label = tk.Label(root, text="Resized Size: N/A")

# Place widgets on the window
open_btn.pack(side="top", fill="both", expand="yes", padx=10, pady=5)
resize_btn.pack(side="top", fill="both", expand="yes", padx=10, pady=5)
display_btn.pack(side="top", fill="both", expand="yes", padx=10, pady=5)
original_size_label.pack(side="top", fill="both", expand="yes", padx=10, pady=5)
resized_size_label.pack(side="top", fill="both", expand="yes", padx=10, pady=5)
panel.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

# Start the GUI event loop
root.mainloop()