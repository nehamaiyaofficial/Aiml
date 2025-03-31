import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import requests
from io import BytesIO
import numpy as np
import time
import random

class InstagramCaptionGenerator:
    def __init__(self):
        """Initialize the caption generator with necessary models"""
        print("Loading BLIP image captioning model...")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        
        # Image analysis parameters
        self.image_features = {}
        
        # Templates for different types of captions
        self.caption_templates = self._load_caption_templates()
        
        print("Models loaded successfully!")

    def _load_caption_templates(self):
        """Load caption templates for different image types and styles"""
        templates = {
            "instagram": {
                "nature": [
                    "Lost in the beauty of nature 🌿 {description} #naturelovers #outdooradventures",
                    "Finding peace in the great outdoors ✨ {description} #naturephotography #wilderness",
                    "Mother Nature showing off again 🌄 {description} #naturelover #outdoorlife"
                ],
                "urban": [
                    "City vibes 🏙️ {description} #citylife #urbanphotography",
                    "Concrete jungle where dreams are made ✨ {description} #cityscape #urban",
                    "Streets have their own stories 🌃 {description} #streetphotography #citylights"
                ],
                "portrait": [
                    "Captured moments ✨ {description} #portrait #photooftheday",
                    "Being my authentic self 💫 {description} #selfcare #goodvibes",
                    "The best moments are the ones that take your breath away 💖 {description} #lifestyle"
                ],
                "food": [
                    "Foodie heaven 😋 {description} #foodporn #delicious",
                    "Eating well is a form of self-respect 🍽️ {description} #foodie #yummy",
                    "Good food, good mood 🍕 {description} #instafood #foodlover"
                ],
                "generic": [
                    "Living in the moment ✨ {description} #liveauthentic #photooftheday",
                    "Making memories that will last forever 💫 {description} #instagood #blessed",
                    "Life is beautiful when you focus on what truly matters 🌟 {description} #gratitude"
                ]
            },
            "professional": {
                "generic": [
                    "Excellence in every detail. {description}",
                    "Innovation meets precision. {description}",
                    "Setting new standards. {description}"
                ]
            },
            "artistic": {
                "generic": [
                    "Between shadow and light, we find ourselves. {description}",
                    "The poetry of vision captured in a fleeting moment. {description}",
                    "A whisper of beauty in a world of noise. {description}"
                ]
            },
            "minimal": {
                "generic": [
                    "{description}",
                    "Present moment. ✨",
                    "Simplicity is the ultimate sophistication."
                ]
            }
        }
        return templates

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

    def preprocess_image(self, image_path):
        """Load and preprocess the image"""
        try:
            if isinstance(image_path, str):
                if image_path.startswith(('http://', 'https://')):
                    response = requests.get(image_path, timeout=10)
                    img = Image.open(BytesIO(response.content)).convert("RGB")
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
        
        # Use OpenCV to detect faces for portrait detection
        try:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            has_faces = len(faces) > 0
        except:
            has_faces = False
            
        # Detect if image is likely food
        # Simple heuristic based on color ranges common in food photography
        food_colors = [
            np.array([0, 50, 50]),   # Red-orange tones
            np.array([30, 50, 50]),  # Yellow-brown tones
            np.array([120, 30, 30])  # Some green (vegetables)
        ]
        
        color_matches = 0
        for food_color in food_colors:
            if np.sum(np.abs(avg_color - food_color)) < 150:  # Threshold for similarity
                color_matches += 1
        
        is_food = color_matches >= 1
        
        # Detect if image is likely nature/outdoors
        # Higher green channel relative to red and blue suggests nature
        is_nature = (avg_color[1] > avg_color[0] * 1.1 and 
                    avg_color[1] > avg_color[2] * 1.1 and
                    brightness > 80)
        
        # Detect if urban/city scene (lots of straight lines/edges)
        try:
            edges = cv2.Canny(img_array, 100, 200)
            is_urban = np.count_nonzero(edges) > (edges.size * 0.1)  # If >10% pixels are edges
        except:
            is_urban = False
        
        # Store features
        self.image_features = {
            "brightness": "bright" if brightness > 127 else "dark",
            "colorful": "vibrant" if saturation > 50 else "subtle",
            "orientation": "portrait" if aspect_ratio < 0.9 else "landscape" if aspect_ratio > 1.1 else "square",
            "has_faces": has_faces,
            "is_food": is_food,
            "is_nature": is_nature,
            "is_urban": is_urban
        }
        
        # Determine content type for templating
        if self.image_features["has_faces"]:
            self.image_features["content_type"] = "portrait"
        elif self.image_features["is_food"]:
            self.image_features["content_type"] = "food"
        elif self.image_features["is_nature"]:
            self.image_features["content_type"] = "nature"
        elif self.image_features["is_urban"]:
            self.image_features["content_type"] = "urban"
        else:
            self.image_features["content_type"] = "generic"
            
        print(f"Image analysis: {self.image_features}")

    def generate_blip_caption(self, image_path):
        """Generate an initial caption using the BLIP model"""
        img = self.preprocess_image(image_path)
        if img is None:
            return "Could not process the image."
        
        # Customize prompt based on image features
        content_type = self.image_features["content_type"]
        prompt_lookup = {
            "portrait": "a portrait photograph of a person",
            "food": "a delicious food photograph",
            "nature": "a beautiful nature or landscape photograph",
            "urban": "an urban or city photograph",
            "generic": "a photograph"
        }
        
        prompt_context = prompt_lookup.get(content_type, "a photograph")
        style_context = f"that is {self.image_features['brightness']} and {self.image_features['colorful']}"
        
        prompt = f"Describe this {prompt_context} {style_context} with interesting detail."
        
        # Process image with BLIP
        try:
            inputs = self.processor(img, text=prompt, return_tensors="pt")
            
            with torch.no_grad():
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

    def enhance_caption_locally(self, blip_caption, style="instagram"):
        """Enhance caption without relying on external APIs"""
        content_type = self.image_features["content_type"]
        
        # Get appropriate templates
        if style in self.caption_templates:
            if content_type in self.caption_templates[style]:
                templates = self.caption_templates[style][content_type]
            else:
                templates = self.caption_templates[style]["generic"]
        else:
            templates = self.caption_templates["instagram"]["generic"]
        
        # Select a random template and fill it with the BLIP description
        template = random.choice(templates)
        
        # Clean up the BLIP caption for better integration
        cleaned_caption = blip_caption.replace("the image shows ", "")
        cleaned_caption = cleaned_caption.replace("the image depicts ", "")
        cleaned_caption = cleaned_caption.replace("in the image ", "")
        
        # Create the enhanced caption
        enhanced_caption = template.format(description=cleaned_caption)
        
        # Add style-specific enhancements
        if style == "instagram":
            # Add more relevant hashtags based on content type
            hashtags = {
                "portrait": "#portrait #model #photography",
                "food": "#foodie #foodphotography #delicious",
                "nature": "#nature #outdoors #naturephotography",
                "urban": "#urban #city #architecture",
                "generic": "#photography #photooftheday"
            }
            
            # Add brightness/color hashtags
            if self.image_features["brightness"] == "bright":
                hashtags[content_type] += " #bright #light"
            else:
                hashtags[content_type] += " #moody #dark"
                
            if self.image_features["colorful"] == "vibrant":
                hashtags[content_type] += " #colorful #vibrant"
            else:
                hashtags[content_type] += " #minimal #subtle"
                
            # If not already present, add the hashtags
            if not enhanced_caption.endswith(hashtags[content_type]):
                if "#" in enhanced_caption:
                    # If caption already has hashtags, just add more
                    enhanced_caption += " " + hashtags[content_type]
                else:
                    # If no hashtags, add a line break and then hashtags
                    enhanced_caption += "\n\n" + hashtags[content_type]
                    
        elif style == "professional":
            # Professional captions are clean, no emojis or hashtags
            enhanced_caption = enhanced_caption.replace("#", "").strip()
            
        elif style == "artistic":
            # Artistic captions should be poetic
            enhanced_caption = enhanced_caption.replace("#", "").strip()
            
        return enhanced_caption

    def generate_final_caption(self, image_path, style="instagram"):
        """Combine vision model caption and local enhancement for the best result"""
        print("Analyzing image and generating caption...")
        start_time = time.time()
        
        blip_caption = self.generate_blip_caption(image_path)
        print(f"\nInitial caption: {blip_caption}")
        
        print("Enhancing caption...")
        final_caption = self.enhance_caption_locally(blip_caption, style)
        
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
    
    # Style selection
    style_frame = tk.Frame(root, bg="#f0f2f5")
    style_frame.pack(pady=20, fill="x", padx=20)
    
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
        result_text.insert(tk.END, "Analyzing image and generating caption...\n\n")
        root.update()
        
        # Generate caption
        caption = caption_gen.generate_final_caption(image_path, style_var.get())
        
        # Display result
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"✨ Perfect Caption ✨\n\n{caption}")
        
        # Enable copy button
        copy_btn.config(state="normal")
        
        # Generate alternative button
        def generate_alternative():
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Generating alternative caption...\n\n")
            root.update()
            
            # Generate a new caption with the same style
            caption = caption_gen.generate_final_caption(image_path, style_var.get())
            
            # Display result
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"✨ Alternative Caption ✨\n\n{caption}")
        
        alt_btn.config(state="normal", command=generate_alternative)
    
    select_btn = tk.Button(root, text="Select Image & Generate Caption", command=select_and_generate)
    select_btn.pack(pady=15)
    
    # Results area
    result_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
    result_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    result_text = tk.Text(result_frame, wrap="word", height=12, width=50, padx=10, pady=10)
    result_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Button frame
    button_frame = tk.Frame(root, bg="#f0f2f5")
    button_frame.pack(pady=10, fill="x")
    
    # Copy button
    def copy_to_clipboard():
        caption = result_text.get(1.0, tk.END).strip()
        root.clipboard_clear()
        root.clipboard_append(caption)
        copy_btn.config(text="✓ Copied!")
        root.after(2000, lambda: copy_btn.config(text="Copy to Clipboard"))
    
    copy_btn = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard, state="disabled")
    copy_btn.pack(side="left", padx=10)
    
    # Alternative button
    alt_btn = tk.Button(button_frame, text="Generate Alternative", state="disabled")
    alt_btn.pack(side="right", padx=10)
    
    # Instructions
    instructions = "Select an image to generate a beautiful Instagram caption that matches the content of your photo."
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

