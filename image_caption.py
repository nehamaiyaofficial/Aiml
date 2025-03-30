import cv2
import os
import random
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Cute & Aesthetic Instagram caption templates
CUTE_CAPTIONS = [
    "Sunshine mixed with a little bit of magic.",
    "Golden hour glow and a heart full of dreams.",
    "Smile, sparkle, shine – repeat!",
    "Lost in the beauty of the moment.",
    "Happiness looks good on me, right?",
    "Dripping in sunshine and positivity.",
    "Chasing dreams and catching sunsets.",
    "Sparkle like you mean it.",
    "Blooming like the prettiest flower.",
    "Wander often, wonder always."
]

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
    """Generate a cute and aesthetic caption for Instagram."""
    if image is None:
        print("No valid image provided.")
        return

    # AI-generated caption
    inputs = processor(images=image, return_tensors="pt")
    caption_ids = model.generate(**inputs)
    ai_caption = processor.batch_decode(caption_ids, skip_special_tokens=True)[0]

    # Select a cute caption randomly and merge with AI-generated caption
    cute_caption = random.choice(CUTE_CAPTIONS)
    final_caption = f"{cute_caption} ✨ {ai_caption}"

    print("\nInstagram-Ready Caption:", final_caption)

if __name__ == "__main__":
    image = select_image()
    generate_caption(image)



