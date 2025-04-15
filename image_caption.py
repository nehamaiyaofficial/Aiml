import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
        self.current_image_path = None
        self.current_image_pil = None
        
        # Templates for different types of captions
        self.caption_templates = self._load_caption_templates()
        
        print("Models loaded successfully!")

    def _load_caption_templates(self):
        """Load caption templates for different image types and styles"""
        templates = {
            "instagram": {
                "nature": [
                    "Lost in the beauty of nature Γëí╞Æ├«ΓöÉ {description} #naturelovers #outdooradventures",
                    "Finding peace in the great outdoors ╬ô┬ú┬┐ {description} #naturephotography #wilderness",
                    "Mother Nature showing off again Γëí╞Æ├«├ñ {description} #naturelover #outdoorlife"
                ],
                "urban": [
                    "City vibes Γëí╞Æ├à├ûΓê⌐Γòò├à {description} #citylife #urbanphotography",
                    "Concrete jungle where dreams are made ╬ô┬ú┬┐ {description} #cityscape #urban",
                    "Streets have their own stories Γëí╞Æ├«├ó {description} #streetphotography #citylights"
                ],
                "portrait": [
                    "Captured moments ╬ô┬ú┬┐ {description} #portrait #photooftheday",
                    "Being my authentic self Γëí╞Æ├å┬╜ {description} #selfcare #goodvibes",
                    "The best moments are the ones that take your breath away Γëí╞Æ├å├╗ {description} #lifestyle"
                ],
                "food": [
                    "Foodie heaven Γëí╞Æ├┐├» {description} #foodporn #delicious",
                    "Eating well is a form of self-respect Γëí╞Æ├¼Γò£Γê⌐Γòò├à {description} #foodie #yummy",
                    "Good food, good mood Γëí╞Æ├¼├▓ {description} #instafood #foodlover"
                ],
                "generic": [
                    "Living in the moment ╬ô┬ú┬┐ {description} #liveauthentic #photooftheday",
                    "Making memories that will last forever Γëí╞Æ├å┬╜ {description} #instagood #blessed",
                    "Life is beautiful when you focus on what truly matters Γëí╞Æ├«╞Æ {description} #gratitude"
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
                    "Present moment. ╬ô┬ú┬┐",
                    "Simplicity is the ultimate sophistication."
                ]
            }
        }
        return templates

    def load_image(self):
        """Open file dialog to select an image"""
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
        
        # Store the current image path
        self.current_image_path = file_path
        self.current_image_pil = Image.open(file_path).convert("RGB")
        
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

class ModernCaptionGeneratorUI:
    def __init__(self, root):
        """Initialize the modern UI for the Instagram Caption Generator"""
        self.root = root
        root.title("Instagram Caption Generator")
        root.geometry("900x700")
        root.minsize(800, 600)
        
        # Set application icon
        # try:
        #     root.iconbitmap("path/to/icon.ico")  # For Windows
        #     # For macOS/Linux you would use a different approach
        # except:
        #     pass  # Ignore if icon can't be set
        
        # Color scheme
        self.colors = {
            "primary": "#405DE6",  # Instagram blue
            "secondary": "#5851DB",  # Instagram purple
            "accent": "#833AB4",  # Instagram magenta
            "background": "#FAFAFA",  # Light gray background
            "text": "#262626",  # Dark text
            "light_text": "#8E8E8E",  # Light gray text
            "border": "#DBDBDB",  # Border color
            "success": "#58D68D"  # Green success color
        }
        
        # Configure styles
        self.configure_styles()
        
        # Initialize caption generator
        self.caption_gen = InstagramCaptionGenerator()
        
        # Variables
        self.style_var = tk.StringVar(value="instagram")
        self.selected_image_path = None
        self.current_caption = ""
        
        # Create UI elements
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Apply background color to root
        root.configure(bg=self.colors["background"])
    
    def configure_styles(self):
        """Configure ttk styles for the application"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure button style
        style.configure('Accent.TButton', 
                         background=self.colors["primary"],
                         foreground='white',
                         font=('Helvetica', 11, 'bold'),
                         padding=10)
        
        style.map('Accent.TButton',
                  background=[('active', self.colors["secondary"])],
                  foreground=[('active', 'white')])
        
        # Configure secondary button style
        style.configure('Secondary.TButton', 
                         background='white',
                         foreground=self.colors["text"],
                         padding=10)
        
        # Configure combobox style
        style.configure('TCombobox', 
                        fieldbackground='white',
                        foreground=self.colors["text"])
        
        # Configure label style
        style.configure('TLabel',
                        background=self.colors["background"],
                        foreground=self.colors["text"])
        
        style.configure('Header.TLabel',
                        font=('Helvetica', 18, 'bold'),
                        background=self.colors["background"],
                        foreground=self.colors["primary"])
        
        style.configure('Subheader.TLabel',
                        font=('Helvetica', 12),
                        background=self.colors["background"],
                        foreground=self.colors["light_text"])
    
    def create_header(self):
        """Create the app header section"""
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # App title
        title_label = ttk.Label(header_frame, text="Instagram Caption Generator", style='Header.TLabel')
        title_label.pack(side='left')
        
        # Version info
        version_label = ttk.Label(header_frame, text="v2.0", style='Subheader.TLabel')
        version_label.pack(side='left', padx=(5, 0))
        
        # Settings button
        settings_button = ttk.Button(header_frame, text="⚙️ Settings", style='Secondary.TButton')
        settings_button.pack(side='right')
    
    def create_main_content(self):
        """Create the main content area with image preview and caption sections"""
        # Create main container with two columns
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Configure grid
        main_frame.columnconfigure(0, weight=1)  # Image column
        main_frame.columnconfigure(1, weight=1)  # Caption column
        main_frame.rowconfigure(0, weight=1)
        
        # Create left panel for image
        self.create_image_panel(main_frame)
        
        # Create right panel for captions
        self.create_caption_panel(main_frame)
    
    def create_image_panel(self, parent):
        """Create the left panel for image display and selection"""
        image_frame = ttk.Frame(parent, style='TFrame')
        image_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Create inner frame with border
        image_display_frame = tk.Frame(image_frame, bg='white', bd=1, relief='solid', 
                              highlightbackground=self.colors["border"], highlightthickness=1)
        image_display_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Canvas for image preview with scrollbars
        self.image_canvas = tk.Canvas(image_display_frame, bg='white')
        scrollbar_y = ttk.Scrollbar(image_display_frame, orient='vertical', command=self.image_canvas.yview)
        scrollbar_x = ttk.Scrollbar(image_display_frame, orient='horizontal', command=self.image_canvas.xview)
        
        # Configure canvas
        self.image_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack scrollbars and canvas
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        self.image_canvas.pack(side='left', fill='both', expand=True)
        
        # Image placeholder
        self.image_label = ttk.Label(self.image_canvas, text="No image selected\nClick below to select an image", 
                                    anchor='center', justify='center')
        self.image_canvas.create_window((0, 0), window=self.image_label, anchor='nw')
        
        # Image selection controls
        control_frame = ttk.Frame(image_frame)
        control_frame.pack(fill='x')
        
        # Select image button
        select_btn = ttk.Button(control_frame, text="Select Image", 
                              command=self.select_image, style='Accent.TButton')
        select_btn.pack(side='left', fill='x', expand=True)
    
    def create_caption_panel(self, parent):
        """Create the right panel for caption display and controls"""
        caption_frame = ttk.Frame(parent, style='TFrame')
        caption_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        
        # Caption style selection
        style_frame = ttk.Frame(caption_frame)
        style_frame.pack(fill='x', pady=(0, 10))
        
        style_label = ttk.Label(style_frame, text="Caption Style:", style='TLabel')
        style_label.pack(side='left', padx=(0, 5))
        
        styles = ["instagram", "professional", "artistic", "minimal"]
        style_combo = ttk.Combobox(style_frame, textvariable=self.style_var, values=styles, state='readonly')
        style_combo.pack(side='left', fill='x', expand=True)
        
        # Generate caption button
        generate_btn = ttk.Button(caption_frame, text="Generate Caption", 
                                command=self.generate_caption, style='Accent.TButton')
        generate_btn.pack(fill='x', pady=(0, 10))
        
        # Caption display
        caption_display_frame = tk.Frame(caption_frame, bg='white', bd=1, relief='solid',
                                      highlightbackground=self.colors["border"], highlightthickness=1)
        caption_display_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Caption output text widget with scrollbar
        self.caption_text = tk.Text(caption_display_frame, wrap='word', bg='white', fg=self.colors["text"],
                                 font=('Helvetica', 12), padx=15, pady=15)
        caption_scrollbar = ttk.Scrollbar(caption_display_frame, orient='vertical', command=self.caption_text.yview)
        
        self.caption_text.configure(yscrollcommand=caption_scrollbar.set)
        
        caption_scrollbar.pack(side='right', fill='y')
        self.caption_text.pack(side='left', fill='both', expand=True)
        
        # Initial text
        self.caption_text.insert('1.0', "Your Instagram caption will appear here...\n\n" +
                              "Select an image and click 'Generate Caption' to create a perfect caption for your post!")
        self.caption_text.config(state='disabled')
        
        # Action buttons
        action_frame = ttk.Frame(caption_frame)
        action_frame.pack(fill='x')
        
        # Copy button
        self.copy_btn = ttk.Button(action_frame, text="Copy to Clipboard", 
                                command=self.copy_to_clipboard, state='disabled')
        self.copy_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Alternative button
        self.alt_btn = ttk.Button(action_frame, text="Generate Alternative", 
                               command=lambda: self.generate_caption(alternative=True), state='disabled')
        self.alt_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
    
    def create_footer(self):
        """Create footer with status and progress information"""
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill='x', padx=20, pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to generate captions")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var, 
                              foreground=self.colors["light_text"])
        status_label.pack(side='left')
        
        # Progress bar
        self.progress = ttk.Progressbar(footer_frame, orient='horizontal', length=200, mode='indeterminate')
        self.progress.pack(side='right')
    
    def select_image(self):
        """Handle image selection"""
        image_path = self.caption_gen.load_image()
        if not image_path:
            return
        
        self.selected_image_path = image_path
        self.display_selected_image()
        
        # Update status
        self.status_var.set(f"Image selected: {os.path.basename(image_path)}")
    
    def display_selected_image(self):
        """Display the selected image in the canvas"""
        if not self.selected_image_path or not os.path.exists(self.selected_image_path):
            return
        
        # Get the PIL image
        pil_img = self.caption_gen.current_image_pil
        
        # Calculate dimensions to fit the canvas while preserving aspect ratio
        canvas_width = self.image_canvas.winfo_width() or 300
        canvas_height = self.image_canvas.winfo_height() or 300
        
        # Get original image dimensions
        img_width, img_height = pil_img.size
        
        # Calculate new dimensions
        scale = min(canvas_width/img_width, canvas_height/img_height)
        new_width = int(img_width * scale * 0.9)  # 90% of available space
        new_height = int(img_height * scale * 0.9)
        
        # Resize for display (not for processing)
        display_img = pil_img.copy()
        display_img.thumbnail((new_width, new_height))
        
        # Convert to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(display_img)
        
        # Update canvas
        self.image_canvas.delete("all")
        self.image_canvas.create_image(canvas_width//2, canvas_height//2, anchor=tk.CENTER, image=photo)
        self.image_canvas.image = photo  # Keep a reference to prevent garbage collection
        
        # Configure scrolling region
        self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
    
    def generate_caption(self, alternative=False):
        """Generate or regenerate a caption for the selected image"""
        if not self.selected_image_path:
            messagebox.showinfo("No Image", "Please select an image first.")
            return
        
        # Update status and show progress
        status_message = "Generating alternative caption..." if alternative else "Analyzing image and generating caption..."
        self.status_var.set(status_message)
        self.progress.start()
        
        # Enable text widget for updating
        self.caption_text.config(state='normal')
        self.caption_text.delete('1.0', tk.END)
        self.caption_text.insert('1.0', status_message)
        
        # Use after to allow UI to update before processing
        self.root.after(100, lambda: self._process_caption_generation(alternative))
    
    def _process_caption_generation(self, alternative):
        """Process caption generation in a separate step to allow UI updates"""
        try:
            # Generate caption
            style = self.style_var.get()
            caption = self.caption_gen.generate_final_caption(self.selected_image_path, style)
            
            # Store caption
            self.current_caption = caption
            
            # Update text widget
            self.caption_text.config(state='normal')
            self.caption_text.delete('1.0', tk.END)
            
            # Format caption with emoji and styling
            emoji_prefix = "✨" if alternative else "🔥"
            caption_type = "Alternative" if alternative else "Perfect"
            
            self.caption_text.insert('1.0', f"{emoji_prefix} {caption_type} Caption {emoji_prefix}\n\n")
            
            # Insert the main caption with styling
            self.caption_text.insert('end', caption)
            
            # Apply styling
            self.caption_text.tag_configure('heading', font=('Helvetica', 14, 'bold'), foreground=self.colors["primary"])
            self.caption_text.tag_add('heading', '1.0', '3.0')
            
            # Make read-only again
            self.caption_text.config(state='disabled')
            
            # Enable buttons
            self.copy_btn.config(state='normal')
            self.alt_btn.config(state='normal')
            
        except Exception as e:
            # Handle errors
            self.caption_text.config(state='normal')
            self.caption_text.delete('1.0', tk.END)
            self.caption_text.insert('1.0', f"Error generating caption: {str(e)}")
            self.caption_text.config(state='disabled')
            
        finally:
            # Stop progress and update status
            self.progress.stop()
            self.status_var.set("Caption generated successfully" if self.current_caption else "Error generating caption")
    
    def copy_to_clipboard(self):
        """Copy the current caption to clipboard"""
        if not self.current_caption:
            return
            
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_caption)
        
        # Change button text temporarily
        original_text = self.copy_btn['text']
        self.copy_btn['text'] = "✓ Copied!"
        
        # Schedule text restoration
        self.root.after(2000, lambda: self.copy_btn.config(text=original_text))
        
        # Update status
        self.status_var.set("Caption copied to clipboard")

def main():
    """Main function to run the application"""
    try:
        # Import ImageTk for image display
        global ImageTk
        from PIL import ImageTk
        
        # Check if running in GUI or command line mode
        if os.environ.get("DISPLAY", "") or os.name == "nt":  # GUI mode
            root = tk.Tk()
            app = ModernCaptionGeneratorUI(root)
            
                 # Set window properties
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            # Start the app
            root.mainloop()
        else:
            # Command line mode
            print("Instagram Caption Generator")
            print("==========================")
            caption_gen = InstagramCaptionGenerator()

            image_path = caption_gen.load_image()
            if image_path:
                final_caption = caption_gen.generate_final_caption(image_path)
                print("\n🔥 Perfect Instagram Caption: " + final_caption)
    except ImportError:
        print("Error: PIL.ImageTk is required for the GUI. Install it with: pip install pillow")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully...")
        # If you're using tkinter, you might need to explicitly destroy the root window
        try:
            if 'root' in locals() and hasattr(root, 'destroy'):
                root.destroy()
        except:
            pass
    except Exception as e:
        print(f"\nAn error occurred: {e}")

# Add a splash screen function to enhance the startup experience
def show_splash_screen():
    """Show a splash screen while loading models"""
    splash_root = tk.Tk()
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    # Set splash screen size and position
    width = 500
    height = 300
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    splash_root.geometry(f"{width}x{height}+{x}+{y}")
    splash_root.overrideredirect(True)  # Remove window decorations

    # Create a frame with a gradient background
    splash_frame = tk.Frame(splash_root, bg="#405DE6", bd=2, relief=tk.RIDGE)
    splash_frame.pack(fill=tk.BOTH, expand=True)

    # Create a gradient effect (simple version)
    gradient_canvas = tk.Canvas(splash_frame, width=width, height=height, bd=0, highlightthickness=0)
    gradient_canvas.pack(fill=tk.BOTH, expand=True)

    # Draw gradient
    for i in range(height):
        # Calculate color for each line
        r = int(64 + (min(i / height * 2, 1.0) * 30))
        g = int(93 + (min(i / height * 2, 1.0) * 110))
        b = int(230 - (min(i / height * 2, 1.0) * 50))
        color = f"#{r:02x}{g:02x}{b:02x}"
        gradient_canvas.create_line(0, i, width, i, fill=color)

    # Add logo or text
    logo_text = "Instagram\nCaption Generator"
    gradient_canvas.create_text(width//2, height//3, text=logo_text, font=("Helvetica", 28, "bold"),
                               fill="white", justify=tk.CENTER)

    # Add loading text
    loading_text = tk.StringVar(value="Loading models, please wait...")
    loading_label = tk.Label(splash_frame, textvariable=loading_text, font=("Helvetica", 10),
                           fg="white", bg="#405DE6")
    loading_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Add progress bar
    progress_bar = ttk.Progressbar(splash_frame, orient=tk.HORIZONTAL, length=width-40, mode='indeterminate')
    progress_bar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    progress_bar.start(10)

    # Version info
    version_label = tk.Label(splash_frame, text="v2.0", font=("Helvetica", 8),
                           fg="white", bg="#405DE6")
    version_label.place(relx=0.9, rely=0.95, anchor=tk.E)

    # Update the splash screen
    splash_root.update()

    return splash_root, loading_text, progress_bar

# Modified main function to include the splash screen
def main_with_splash():
    """Main function with splash screen"""
    try:
        # Import ImageTk for image display
        global ImageTk
        from PIL import ImageTk

        # Show splash screen
        splash_root, loading_text, progress_bar = show_splash_screen()

        # Initialize caption generator in the background
        caption_gen = InstagramCaptionGenerator()

        # Close splash screen
        splash_root.destroy()

        # Check if running in GUI or command line mode
        if os.environ.get("DISPLAY", "") or os.name == "nt":  # GUI mode
            root = tk.Tk()
            app = ModernCaptionGeneratorUI(root)
            app.caption_gen = caption_gen  # Use the already initialized generator

            # Set window properties
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f"{width}x{height}+{x}+{y}")

            # Start the app
            root.mainloop()
        else:
            # Command line mode
            print("Instagram Caption Generator")
            print("==========================")

            image_path = caption_gen.load_image()
            if image_path:
                final_caption = caption_gen.generate_final_caption(image_path)
                print("\n🔥 Perfect Instagram Caption: " + final_caption)
    except ImportError:
        print("Error: PIL.ImageTk is required for the GUI. Install it with: pip install pillow")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully...")
        # If you're using tkinter, you might need to explicitly destroy the root window
        try:
            if 'splash_root' in locals() and hasattr(splash_root, 'destroy'):
                splash_root.destroy()
            if 'root' in locals() and hasattr(root, 'destroy'):
                root.destroy()
        except:
            pass
    except Exception as e:
        print(f"\nAn error occurred: {e}")

# Add theme customization function
class ThemeManager:
    """Class to manage app themes"""

    THEMES = {
        "default": {
            "primary": "#405DE6",  # Instagram blue
            "secondary": "#5851DB",  # Instagram purple
            "accent": "#833AB4",  # Instagram magenta
            "background": "#FAFAFA",  # Light gray background
            "text": "#262626",  # Dark text
            "light_text": "#8E8E8E",  # Light gray text
            "border": "#DBDBDB",  # Border color
            "success": "#58D68D"  # Green success color
        },
        "dark": {
            "primary": "#405DE6",  # Instagram blue
            "secondary": "#5851DB",  # Instagram purple
            "accent": "#833AB4",  # Instagram magenta
            "background": "#121212",  # Dark background
            "text": "#FFFFFF",  # White text
            "light_text": "#BBBBBB",  # Light gray text
            "border": "#333333",  # Dark border
            "success": "#58D68D"  # Green success color
        },
        "vintage": {
            "primary": "#D4A373",  # Warm brown
            "secondary": "#CCD5AE",  # Light olive
            "accent": "#E9EDC9",  # Cream
            "background": "#FAEDCD",  # Light beige
            "text": "#4A4238",  # Dark brown text
            "light_text": "#7D7365",  # Medium brown text
            "border": "#D4A373",  # Warm brown border
            "success": "#588157"  # Muted green
        }
    }

    @staticmethod
    def apply_theme(ui_instance, theme_name="default"):
        """Apply a theme to the UI"""
        if theme_name not in ThemeManager.THEMES:
            theme_name = "default"

        # Get theme colors
        colors = ThemeManager.THEMES[theme_name]

        # Update colors
        ui_instance.colors = colors

        # Update root background
        ui_instance.root.configure(bg=colors["background"])

        # Update styles
        style = ttk.Style()

        # Update button styles
        style.configure('Accent.TButton',
                        background=colors["primary"],
                        foreground='white')

        style.map('Accent.TButton',
                  background=[('active', colors["secondary"])],
                  foreground=[('active', 'white')])

        # Update label styles
        style.configure('TLabel',
                        background=colors["background"],
                        foreground=colors["text"])

        style.configure('Header.TLabel',
                        background=colors["background"],
                        foreground=colors["primary"])

        style.configure('Subheader.TLabel',
                        background=colors["background"],
                        foreground=colors["light_text"])

        # Update text widgets
        ui_instance.caption_text.config(
            bg=colors["background"],
            fg=colors["text"],
            insertbackground=colors["text"]
        )

        # Update canvas
        ui_instance.image_canvas.config(
            bg=colors["background"]
        )

        # Update frames
        for widget in ui_instance.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=colors["background"],
                                       highlightbackground=colors["border"])

        # Force update
        ui_instance.root.update_idletasks()

# Create settings dialog
class SettingsDialog:
    """Settings dialog for the application"""
    def __init__(self, parent, ui_instance):
        self.parent = parent
        self.ui = ui_instance

        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center dialog
        self.center_window()

        # Create settings UI
        self.create_settings_ui()

    def center_window(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()

        # Get parent and dialog dimensions
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()

        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        # Calculate position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        # Set position
        self.dialog.geometry(f"+{x}+{y}")

    def create_settings_ui(self):
        """Create the settings UI elements"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Settings", style='Header.TLabel')
        title_label.pack(pady=(0, 20), anchor='w')

        # Theme selection
        theme_frame = ttk.LabelFrame(main_frame, text="Theme")
        theme_frame.pack(fill='x', pady=(0, 20))

        self.theme_var = tk.StringVar(value="default")

        # Theme options
        for i, theme in enumerate(["default", "dark", "vintage"]):
            theme_pretty_name = theme.capitalize()
            rb = ttk.Radiobutton(theme_frame, text=theme_pretty_name, value=theme,
                               variable=self.theme_var, command=self.on_theme_change)
            rb.pack(anchor='w', padx=20, pady=5)

        # Model settings
        model_frame = ttk.LabelFrame(main_frame, text="Caption Model")
        model_frame.pack(fill='x', pady=(0, 20))

        # Default style
        style_frame = ttk.Frame(model_frame)
        style_frame.pack(fill='x', padx=20, pady=10)

        style_label = ttk.Label(style_frame, text="Default Style:")
        style_label.pack(side='left')

        self.default_style_var = tk.StringVar(value=self.ui.style_var.get())
        styles = ["instagram", "professional", "artistic", "minimal"]
        style_combo = ttk.Combobox(style_frame, textvariable=self.default_style_var,
                                 values=styles, state='readonly', width=15)
        style_combo.pack(side='right', padx=(10, 0))

        # Model temperature
        temp_frame = ttk.Frame(model_frame)
        temp_frame.pack(fill='x', padx=20, pady=10)

        temp_label = ttk.Label(temp_frame, text="Creativity Level:")
        temp_label.pack(side='left')

        self.temp_var = tk.DoubleVar(value=0.7)
        temp_scale = ttk.Scale(temp_frame, from_=0.1, to=1.0, orient='horizontal',
                             variable=self.temp_var, length=150)
        temp_scale.pack(side='right')

        # Caption length
        length_frame = ttk.Frame(model_frame)
        length_frame.pack(fill='x', padx=20, pady=10)

        length_label = ttk.Label(length_frame, text="Caption Length:")
        length_label.pack(side='left')

        self.length_var = tk.StringVar(value="medium")
        length_options = ["short", "medium", "long"]
        for i, option in enumerate(length_options):
            rb = ttk.Radiobutton(length_frame, text=option.capitalize(), value=option,
                               variable=self.length_var)
            rb.pack(side='left', padx=(10 if i > 0 else 20, 0))

        # Advanced settings
        adv_frame = ttk.LabelFrame(main_frame, text="Advanced")
        adv_frame.pack(fill='x')

        # Hashtag toggle
        self.hashtag_var = tk.BooleanVar(value=True)
        hashtag_check = ttk.Checkbutton(adv_frame, text="Include hashtags", variable=self.hashtag_var)
        hashtag_check.pack(anchor='w', padx=20, pady=5)

        # Emoji toggle
        self.emoji_var = tk.BooleanVar(value=True)
        emoji_check = ttk.Checkbutton(adv_frame, text="Include emojis", variable=self.emoji_var)
        emoji_check.pack(anchor='w', padx=20, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))

        save_btn = ttk.Button(button_frame, text="Save Changes", command=self.save_settings,
                            style='Accent.TButton')
        save_btn.pack(side='right')

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side='right', padx=(0, 10))

    def on_theme_change(self):
        """Handle theme change"""
        ThemeManager.apply_theme(self.ui, self.theme_var.get())

    def save_settings(self):
        """Save settings and close dialog"""
        # Apply settings to UI
        self.ui.style_var.set(self.default_style_var.get())

        # Save settings (these would be used in the caption generation)
        settings = {
            "theme": self.theme_var.get(),
            "default_style": self.default_style_var.get(),
            "creativity": self.temp_var.get(),
            "caption_length": self.length_var.get(),
            "use_hashtags": self.hashtag_var.get(),
            "use_emojis": self.emoji_var.get()
        }

        # Here you would actually save these settings to a file
        print(f"Settings saved: {settings}")

        # Close dialog
        self.dialog.destroy()

# Use the splash screen version of main instead
if __name__ == "__main__":
    main_with_splash()
