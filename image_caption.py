import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Load BLIP Model (Large version for better accuracy)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# OpenAI API Key (Replace with your own)
openai.api_key = "YOUR_OPENAI_API_KEY"

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
    """Load and preprocess the image"""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((384, 384))  # Resize for model consistency
    return img

def generate_blip_caption(image_path):
    """Generate an initial caption using the BLIP model"""
    img = preprocess_image(image_path)

    # Use a refined prompt to make captions more engaging
    prompt = "Describe this image with a beautiful and engaging Instagram-style caption."

    # Process image with BLIP
    inputs = processor(img, text=prompt, return_tensors="pt")
    
    with torch.no_grad():
        caption_ids = model.generate(**inputs, max_length=50)

    blip_caption = processor.decode(caption_ids[0], skip_special_tokens=True)

    return blip_caption

def enhance_caption_with_gpt4(blip_caption):
    """Use GPT-4 to refine the BLIP-generated caption for better accuracy"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at creating beautiful Instagram captions."},
                {"role": "user", "content": f"Improve this Instagram caption to make it more engaging and stylish: '{blip_caption}'"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"GPT-4 Error: {e}")
        return blip_caption  # Use BLIP's caption if GPT-4 fails

def generate_final_caption(image_path):
    """Combine BLIP caption and GPT-4 refinement for the best result"""
    blip_caption = generate_blip_caption(image_path)
    final_caption = enhance_caption_with_gpt4(blip_caption)
    return final_caption

# Main function
if __name__ == "__main__":
    print("Please select an image...")
    image_path = load_image()

    if image_path:
        final_caption = generate_final_caption(image_path)
        print("\n✨ Perfect Instagram Caption: " + final_caption)




