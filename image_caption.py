import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import openai
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import requests
from io import BytesIO
import numpy as np
import time

class InstagramCaptionGenerator:
    def __init__(self):
        """Initialize the caption generator with necessary models"""
        print("Loading BLIP image captioning model...")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        
        # OpenAI API setup - using legacy pattern for compatibility
        openai.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
        
        # Image analysis parameters
        self.image_features = {}
        print("Models loaded successfully!")

    def load_image(self):
        """Open file dialog to select an image"""
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp;*.bmp")]
        )
        if not file_path:
            print("No image selected. Please try again.")
            return None
            
        # Display image info
        img_size = os.path.getsize(file_path) / 1024  # KB
        print(f"Selected image: {os.path.basename(file_path)} ({img_size:.1f} KB)")
        return file_path
    
    def load_image_from_url(self, url):
        """Load an image from a URL"""
        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            return img
        except Exception as e:
            print(f"Error loading image from URL: {e}")
            return None

    def preprocess_image(self, image_path):
        """Load and preprocess the image"""
        try:
            if isinstance(image_path, str):
                if image_path.startswith(('http://', 'https://')):
                    img = self.load_image_from_url(image_path)
                else:
                    img = Image.open(image_path).convert("RGB")
            else:
                img = image_path  # Assume it's already a PIL Image
                
            # Extract image features and metadata for better captions
            self.analyze_image(img)
            
            # Keep original aspect ratio but resize for processing
            img.thumbnail((512, 512))
            return img
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def analyze_image(self, img):
        """Extract features from image to improve caption relevance"""
        # Convert to numpy for analysis
        img_array = np.array(img)
        
        # Basic color analysis
        avg_color = np.mean(img_array, axis=(0, 1))
        brightness = np.mean(avg_color)
        saturation = np.std(img_array, axis=(0, 1)).mean()
        
        # Simple composition analysis
        height, width = img_array.shape[:2]
        aspect_ratio = width / height
        
        # Store features
        self.image_features = {
            "brightness": "bright" if brightness > 127 else "dark",
            "colorful": "vibrant" if saturation > 50 else "subtle",
            "orientation": "portrait" if aspect_ratio < 0.9 else "landscape" if aspect_ratio > 1.1 else "square"
        }

    def generate_blip_caption(self, image_path):
        """Generate an initial caption using the BLIP model"""
        img = self.preprocess_image(image_path)
        if img is None:
            return "Could not process the image."
        
        # Customize prompt based on image features
        prompt_context = f"a {self.image_features['brightness']}, {self.image_features['colorful']} {self.image_features['orientation']} image"
        prompt = f"Describe this {prompt_context} with a beautiful and engaging Instagram-style caption."
        
        # Process image with BLIP
        try:
            inputs = self.processor(img, text=prompt, return_tensors="pt")
            
            with torch.no_grad():
                # Generate 3 different caption candidates with different settings
                caption_ids = self.model.generate(
                    **inputs, 
                    max_length=75,
                    num_beams=5,
                    min_length=20,
                    top_p=0.9,
                    repetition_penalty=1.5
                )
            blip_caption = self.processor.decode(caption_ids[0], skip_special_tokens=True)
            return blip_caption
        except Exception as e:
            print(f"BLIP caption generation error: {e}")
            return "Error generating caption with BLIP model."

    def enhance_caption_with_gpt(self, blip_caption, style="instagram"):
        """Use GPT to refine the BLIP-generated caption"""
        try:
            # Define style templates
            style_prompts = {
                "instagram": "Make this caption perfect for Instagram with emojis and hashtags:",
                "professional": "Refine this into a professional caption for a business profile:",
                "artistic": "Transform this into a poetic and artistic caption:",
                "minimal": "Create a minimal, impactful short caption from this description:"
            }
            
            style_prompt = style_prompts.get(style, style_prompts["instagram"])
            
            # Add image features context
            context = (f"The image is {self.image_features['brightness']}, "
                      f"{self.image_features['colorful']}, and in "
                      f"{self.image_features['orientation']} orientation. ")
            
            # Using the older OpenAI API format
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Can fall back to gpt-3.5-turbo if needed
                messages=[
                    {"role": "system", "content": f"You are an expert at creating engaging social media captions. {context}"},
                    {"role": "user", "content": f"{style_prompt} '{blip_caption}'"}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT enhancement error: {e}")
            # Try a fallback without OpenAI
            return self.local_caption_enhancement(blip_caption)
    
    def local_caption_enhancement(self, caption):
        """Fallback method to enhance captions locally if API fails"""
        # Add some emojis based on content
        enhanced = caption
        if "nature" in caption.lower() or "outdoor" in caption.lower():
            enhanced += " 🌿🌄"
        elif "food" in caption.lower() or "drink" in caption.lower():
            enhanced += " 🍽️😋"
        elif "travel" in caption.lower() or "adventure" in caption.lower():
            enhanced += " ✈️🗺️"
        else:
            enhanced += " ✨📸"
            
        # Add generic hashtags
        enhanced += "\n\n#photooftheday #instagood #beautiful #picoftheday"
        return enhanced

    def generate_final_caption(self, image_path, style="instagram"):
        """Combine vision model caption and GPT refinement for the best result"""
        print("Analyzing image and generating caption...")
        start_time = time.time()
        
        blip_caption = self.generate_blip_caption(image_path)
        print(f"\nInitial caption: {blip_caption}")
        
        print("Enhancing caption...")
        final_caption = self.enhance_caption_with_gpt(blip_caption, style)
        
        elapsed = time.time() - start_time
        print(f"Caption generated in {elapsed:.1f} seconds")
        
        return final_caption

def setup_ui():
    """Create a simple UI for the caption generator"""
    root = tk.Tk()
    root.title("Instagram Caption Generator")
    root.geometry("600x500")
    root.configure(bg="#f0f2f5")
    
    # Initialize caption generator
    caption_gen = InstagramCaptionGenerator()
    
    # Set up API key input
    api_frame = tk.Frame(root, bg="#f0f2f5")
    api_frame.pack(pady=10, padx=20, fill="x")
    
    tk.Label(api_frame, text="OpenAI API Key:", bg="#f0f2f5").pack(side="left")
    api_key_var = tk.StringVar(value=os.environ.get("OPENAI_API_KEY", ""))
    api_entry = tk.Entry(api_frame, textvariable=api_key_var, width=40, show="*")
    api_entry.pack(side="left", padx=5)
    
    def save_api_key():
        key = api_key_var.get().strip()
        if key:
            os.environ["OPENAI_API_KEY"] = key
            openai.api_key = key  # Update the API key for the OpenAI module
            save_btn.config(text="✓ Saved")
            root.after(2000, lambda: save_btn.config(text="Save Key"))
    
    save_btn = tk.Button(api_frame, text="Save Key", command=save_api_key)
    save_btn.pack(side="left", padx=5)
    
    # Style selection
    style_frame = tk.Frame(root, bg="#f0f2f5")
    style_frame.pack(pady=10, fill="x", padx=20)
    
    tk.Label(style_frame, text="Caption Style:", bg="#f0f2f5").pack(side="left")
    style_var = tk.StringVar(value="instagram")
    styles = ["instagram", "professional", "artistic", "minimal"]
    style_menu = tk.OptionMenu(style_frame, style_var, *styles)
    style_menu.pack(side="left", padx=5)
    
    # Image selection and caption display
    def select_and_generate():
        image_path = caption_gen.load_image()
        if not image_path:
            return
            
        # Show loading indicator
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Generating caption...\n\n")
        root.update()
        
        # Generate caption
        caption = caption_gen.generate_final_caption(image_path, style_var.get())
        
        # Display result
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"✨ Perfect Caption ✨\n\n{caption}")
        
        # Enable copy button
        copy_btn.config(state="normal")
    
    select_btn = tk.Button(root, text="Select Image & Generate Caption", command=select_and_generate)
    select_btn.pack(pady=15)
    
    # Results area
    result_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
    result_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    result_text = tk.Text(result_frame, wrap="word", height=12, width=50, padx=10, pady=10)
    result_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Copy button
    def copy_to_clipboard():
        caption = result_text.get(1.0, tk.END).strip()
        root.clipboard_clear()
        root.clipboard_append(caption)
        copy_btn.config(text="✓ Copied!")
        root.after(2000, lambda: copy_btn.config(text="Copy to Clipboard"))
    
    copy_btn = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, state="disabled")
    copy_btn.pack(pady=10)
    
    # Instructions
    instructions = "Select an image to generate a beautiful Instagram caption. For best results, provide your OpenAI API key."
    tk.Label(root, text=instructions, fg="gray", bg="#f0f2f5", wraplength=500).pack(pady=5)
    
    return root

def main():
    """Main function to run the application"""
    # Check if running in GUI or command line mode
    if os.environ.get("DISPLAY", "") or os.name == "nt":  # GUI mode
        app = setup_ui()
        app.mainloop()
    else:
        # Command line mode
        print("Instagram Caption Generator")
        print("==========================")
        caption_gen = InstagramCaptionGenerator()
        
        image_path = caption_gen.load_image()
        if image_path:
            final_caption = caption_gen.generate_final_caption(image_path)
            print("\n✨ Perfect Instagram Caption: " + final_caption)

if __name__ == "__main__":
    main()
