import cv2
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import torchvision.transforms as transforms
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def select_image():
    """Open a file dialog for the user to select an image."""
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.webp")]
    )

    if not file_path:
        print("No file selected.")
        return None

    try:
        img = Image.open(file_path).convert("RGB")
        img.show()  # Display the image
        print("Image loaded successfully.")
        return img
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

def generate_caption(image):
    """Generate a caption for the selected image."""
    if image is None:
        print("No valid image provided.")
        return

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")
    
    # Generate caption
    caption_ids = model.generate(**inputs)
    caption = processor.batch_decode(caption_ids, skip_special_tokens=True)[0]
    
    print("\nGenerated Caption:", caption)

if __name__ == "__main__":
    image = select_image()
    generate_caption(image)



