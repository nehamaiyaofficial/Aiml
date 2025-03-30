import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Load BLIP Model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def load_image():
    """Open file dialog to select an image"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select an Image",
                                           filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        print("No image selected. Please try again.")
        return None
    return file_path

def preprocess_image(image_path):
    """Convert image to PIL format"""
    img = Image.open(image_path).convert("RGB")
    return img

def generate_caption(image_path):
    """Generate a caption using AI"""
    img = preprocess_image(image_path)
    
    # Process image for BLIP model
    inputs = processor(img, return_tensors="pt")
    with torch.no_grad():
        caption_ids = model.generate(**inputs)
    
    caption = processor.decode(caption_ids[0], skip_special_tokens=True)
    return caption

# Main function
if __name__ == "__main__":
    print("Please select an image...")
    image_path = load_image()

    if image_path:
        caption = generate_caption(image_path)
        print("\n✨ Instagram Caption: " + caption)




