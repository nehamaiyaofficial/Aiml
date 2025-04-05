#!/usr/bin/env python3
import random
import re
import sympy as sp
import datetime
import requests
import json
import numpy as np
from collections import defaultdict
import time

# Properly structured NLP imports and define NLP_AVAILABLE as global
NLP_AVAILABLE = False
try:
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import spacy
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

class AIChatbot:
    def __init__(self):
        # Initialize conversation memory
        self.conversation_history = []
        self.user_preferences = defaultdict(str)
        self.learning_dictionary = {}
        self.user_name = ""
        self.last_topic = ""
        self.chat_start_time = time.time()
        
        # Access global NLP_AVAILABLE variable
        global NLP_AVAILABLE
        
        # Initialize NLP components if available
        if NLP_AVAILABLE:
            try:
                import nltk
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                self.lemmatizer = WordNetLemmatizer()
                self.stop_words = set(stopwords.words('english'))
                self.vectorizer = TfidfVectorizer()
                print("NLP components initialized successfully.")
            except Exception as e:
                print(f"Error initializing NLP components: {e}")
                NLP_AVAILABLE = False
                
        # Knowledge base for general questions
        self.knowledge_base = self.load_knowledge_base()
        
        # Initialize the TF-IDF vectorizer if NLP is available
        if NLP_AVAILABLE and self.knowledge_base:
            questions = [item['question'] for item in self.knowledge_base]
            self.tfidf_matrix = self.vectorizer.fit_transform(questions)
            
        # Predefined responses with more human-like variability
        self.responses = {
            "hello": [
                "Hey there! How's your day going so far?",
                "Hello! What's on your mind today?",
                "Hi! Nice to chat with you. How are you feeling today?",
                "Greetings! What exciting thing shall we chat about today?",
                "Hey! It's good to see you. What can I help with?"
            ],
            "how are you": [
                "I'm doing quite well, thanks for asking! How about yourself?",
                "I'm feeling pretty good today. How has your day been so far?",
                "I'm great! Excited to have this conversation with you. How are you doing?",
                "I'm functioning perfectly and enjoying our chat! What about you?",
                "I'm having a wonderful day chatting with people like you. How are things on your end?"
            ],
            "what can you do": [
                "I can chat about almost anything, answer multiple questions at once, tell jokes, solve math problems, remember details about you, learn new responses, and more. What would you like to try first?",
                "Besides chatting, I can solve equations, answer knowledge questions, handle multiple questions in one go, learn new things, and even attempt humor. Got something specific in mind?",
                "Think of me as your AI assistant—I can understand and answer multiple questions at once, remember details from our chat, solve math problems, and even learn new information from you. What interests you most?",
                "I'm pretty versatile! I can chat naturally, solve math problems, tell jokes, remember things about you, answer general knowledge questions, and learn new information. What would you like help with today?"
            ],
            "bye": [
                "Goodbye! I really enjoyed our conversation. Hope to chat with you again soon!",
                "See you later! It was great talking with you today.",
                "Take care! I'll be here whenever you'd like to chat again.",
                "It was wonderful chatting with you. Have a great rest of your day!",
                "Goodbye for now! Looking forward to our next conversation."
            ],
            "thank you": [
                "You're very welcome! Happy I could help.",
                "Anytime! That's what I'm here for.",
                "No problem at all! Is there anything else you'd like to know?",
                "Glad I could be of assistance! Let me know if you need anything else.",
                "It's my pleasure to help! Feel free to ask if you have more questions."
            ],
            "confused": [
                "I'm not quite sure I understand. Could you rephrase that?",
                "Hmm, I'm a bit confused by what you mean. Could you explain it differently?",
                "I want to help, but I'm not following completely. Mind clarifying a bit?",
                "I'm having trouble understanding that. Could you try explaining it another way?",
                "Sorry, I'm not quite getting it. Could you give me a bit more context?"
            ],
            "default": [
                "That's interesting! Tell me more about what you're thinking.",
                "I'd love to explore that topic further with you. What aspects interest you most?",
                "That's a fascinating point. What are your thoughts on it?",
                "I'm curious to hear more about your perspective on this.",
                "Interesting! Would you like to discuss this more deeply?"
            ]
        }
        
        # Additional response categories for more human-like interaction
        self.emotional_responses = {
            "happy": [
                "That's wonderful to hear! What made your day so good?",
                "I'm so glad things are going well for you! Anything specific you'd like to share?",
                "That's great news! I'm happy for you. Tell me more!",
                "Awesome! It's always nice to hear positive things. What's next for you?"
            ],
            "sad": [
                "I'm sorry to hear that. Would you like to talk about what's bothering you?",
                "That sounds difficult. Is there anything I can do to help?",
                "I understand that can be tough. Sometimes talking about it helps. What happened?",
                "That's unfortunate. I'm here to listen if you want to share more."
            ],
            "excited": [
                "Your enthusiasm is contagious! Tell me more about what you're excited about!",
                "That sounds amazing! What are you looking forward to most?",
                "How wonderful! I'd love to hear all the details about this exciting news.",
                "That's fantastic! What made you so excited about this?"
            ],
            "frustrated": [
                "That does sound frustrating. What do you think would help the situation?",
                "I can understand why you'd feel that way. Have you tried any solutions yet?",
                "It's normal to feel frustrated sometimes. Would talking through it help?",
                "That's a challenging situation. What would make things better for you?"
            ]
        }
        
        # Topic-specific responses for more natural conversation flow
        self.topic_responses = {
            "technology": [
                "Technology is evolving so quickly these days. What recent developments have caught your interest?",
                "Are you generally an early adopter of new tech, or do you prefer to wait until things are well-established?",
                "What's your take on artificial intelligence and its impact on society?",
                "Do you have a favorite gadget or piece of technology that you couldn't live without?"
            ],
            "movies": [
                "Have you seen any good films lately? I'd love to hear your recommendations.",
                "What genres of movies do you typically enjoy the most?",
                "Who would you say is your favorite director or actor?",
                "Do you prefer watching movies at home or the theater experience?"
            ],
            "books": [
                "What kind of books do you enjoy reading? Any recommendations?",
                "Who are some of your favorite authors?",
                "Have you read anything recently that really moved you or changed your perspective?",
                "Do you prefer physical books, e-books, or audiobooks?"
            ],
            "music": [
                "What kind of music do you listen to most often?",
                "Have you discovered any new artists lately that you're excited about?",
                "Do you play any musical instruments yourself?",
                "What role does music play in your daily life?"
            ],
            "food": [
                "Do you enjoy cooking? What's your specialty?",
                "What's your favorite cuisine or dish?",
                "Have you tried any new restaurants or recipes lately?",
                "Are there any foods you absolutely cannot stand?"
            ],
            "travel": [
                "What's the most interesting place you've ever visited?",
                "Is there somewhere you've always dreamed of traveling to?",
                "Do you prefer beach vacations, city exploring, or something more adventurous?",
                "What's your approach to travel planning - structured itinerary or spontaneous exploring?"
            ]
        }
        
        # Follow-up questions to make conversation more natural
        self.follow_up_questions = [
            "What do you think about that?",
            "How does that sound to you?",
            "Have you had any experiences with this before?",
            "What's your take on this?",
            "I'm curious about your thoughts on this topic.",
            "Does that answer your question, or would you like me to elaborate?",
            "Is there anything specific about this you'd like to explore further?",
            "What aspects of this interest you most?",
            "Have I addressed what you were asking about?",
            "What are your thoughts on what I've shared?"
        ]
        
        # Command patterns with more natural language variations
        self.commands = {
            r'what time is it': self.get_time,
            r'what\'s the time': self.get_time,
            r'tell me the time': self.get_time,
            r'what( is|\'s) the date': self.get_date,
            r'what day is (it|today)': self.get_date,
            r'today\'s date': self.get_date,
            r'remember that my (\w+) is (.+)': self.remember_preference,
            r'my (\w+) is (.+)': self.remember_preference,
            r'what( is|\'s) my (\w+)': self.recall_preference,
            r'do you know my (\w+)': self.recall_preference,
            r'learn that (.*?) -> (.*)': self.learn_response,
            r'teach you that (.*?) means (.*)': self.learn_response,
            r'what do you know about (.*)': self.check_learned_response,
            r'tell me what you know about (.*)': self.check_learned_response,
            r'tell me a joke': self.tell_joke,
            r'make me laugh': self.tell_joke,
            r'say something funny': self.tell_joke,
            r'flip a coin': self.flip_coin,
            r'toss a coin': self.flip_coin,
            r'heads or tails': self.flip_coin,
            r'roll a dice': self.roll_dice,
            r'roll a die': self.roll_dice,
            r'roll a (\d+)-sided dice': self.roll_n_sided_dice,
            r'roll a (\d+)-sided die': self.roll_n_sided_dice,
            r'weather in (.+)': self.get_weather,
            r'what\'s the weather like in (.+)': self.get_weather,
            r'how\'s the weather in (.+)': self.get_weather,
            r'define (.+)': self.get_definition,
            r'what does (.+) mean': self.get_definition,
            r'what is the meaning of (.+)': self.get_definition,
            r'what\'s your name': self.get_name,
            r'who are you': self.get_name,
            r'tell me about yourself': self.get_name,
            r'how long have we been talking': self.get_chat_duration,
            r'my name is (.+)': self.set_user_name,
            r'call me (.+)': self.set_user_name
        }

    def load_knowledge_base(self):
        """Loads the knowledge base from a JSON file or creates a default one if not found."""
        try:
            with open('knowledge_base.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create a default knowledge base with more diverse questions
            default_kb = [
                {
                    "question": "What is AI?",
                    "answer": "Artificial Intelligence (AI) refers to systems or machines that mimic human intelligence to perform tasks and can iteratively improve themselves based on the information they collect. It's a broad field that includes machine learning, neural networks, natural language processing, and more."
                },
                {
                    "question": "Who invented the light bulb?",
                    "answer": "Thomas Edison is typically credited with inventing the practical incandescent light bulb, though earlier inventors like Joseph Swan also developed similar technologies. Edison's version from 1879 was more commercially viable and widely adopted."
                },
                {
                    "question": "What is the capital of France?",
                    "answer": "Paris is the capital of France. It's known as the 'City of Light' and is famous for iconic landmarks like the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral."
                },
                {
                    "question": "How far is the moon from Earth?",
                    "answer": "The average distance between the Earth and the Moon is about 238,855 miles (384,400 kilometers). This distance varies because the Moon follows an elliptical orbit around Earth."
                },
                {
                    "question": "What is the largest planet in our solar system?",
                    "answer": "Jupiter is the largest planet in our solar system. It's a gas giant with a mass more than 300 times that of Earth and is known for its Great Red Spot, which is a giant storm that has lasted for hundreds of years."
                },
                {
                    "question": "How does photosynthesis work?",
                    "answer": "Photosynthesis is the process by which plants, algae, and some bacteria convert sunlight, water, and carbon dioxide into glucose (sugar) and oxygen. The chlorophyll in plant cells captures energy from sunlight and uses it to combine water and CO2 to create glucose, which the plant uses for energy, while releasing oxygen as a byproduct."
                },
                {
                    "question": "Who wrote Romeo and Juliet?",
                    "answer": "William Shakespeare wrote Romeo and Juliet around 1595. It's one of his most famous tragedies about two young star-crossed lovers whose deaths ultimately reconcile their feuding families."
                },
                {
                    "question": "What is the theory of relativity?",
                    "answer": "The theory of relativity, developed by Albert Einstein, consists of two related theories: Special Relativity (1905) and General Relativity (1915). Special Relativity shows that space and time are interconnected for objects moving at constant speeds, while General Relativity explains that gravity is not a force but a curvature of spacetime caused by mass and energy."
                },
                {
                    "question": "What are black holes?",
                    "answer": "Black holes are regions of spacetime where gravity is so strong that nothing—including light or other electromagnetic waves—can escape from it. They form when very massive stars die and collapse under their own gravity. At the center of a black hole is a singularity, a point of infinite density where our current physics laws break down."
                },
                {
                    "question": "How do vaccines work?",
                    "answer": "Vaccines work by training the immune system to recognize and combat pathogens. They contain weakened or inactivated parts of a particular organism that triggers an immune response in the body. This helps the body develop immunity to that specific disease without having to get the illness first, creating memory cells that remember how to fight that disease in the future."
                },
                {
                    "question": "What is climate change?",
                    "answer": "Climate change refers to long-term shifts in temperatures and weather patterns. Since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil, and gas, which produces heat-trapping gases. This leads to rising global temperatures, changing precipitation patterns, more extreme weather events, and rising sea levels."
                },
                {
                    "question": "What are the benefits of exercise?",
                    "answer": "Regular exercise offers numerous benefits including weight management, reduced risk of heart diseases and certain cancers, stronger bones and muscles, improved mental health and mood, better sleep, increased energy levels, and enhanced cognitive function. It also helps reduce stress and anxiety while potentially extending your lifespan."
                },
                {
                    "question": "How does the internet work?",
                    "answer": "The internet works through a global network of interconnected computers that communicate via standardized protocols (primarily TCP/IP). When you access a website, your device sends a request through your Internet Service Provider to servers that host the website. The data is broken into packets, transmitted over various network paths, and reassembled at your device to display the website content."
                },
                {
                    "question": "What causes rainbows?",
                    "answer": "Rainbows form when sunlight enters water droplets in the atmosphere, gets refracted (bent), reflects off the back of the droplet, and then refracts again as it exits. This process separates white sunlight into its component colors. You'll only see a rainbow if the sun is behind you and rain or mist is in front of you at the right angle."
                },
                {
                    "question": "Why is the sky blue?",
                    "answer": "The sky appears blue because air molecules scatter sunlight. Specifically, they scatter shorter wavelengths of light (blue and violet) more than longer wavelengths. While violet light is actually scattered more than blue, our eyes are more sensitive to blue light, so the sky appears blue to us rather than violet."
                },
                {
                    "question": "What is quantum computing?",
                    "answer": "Quantum computing uses quantum bits or 'qubits' that can exist in multiple states simultaneously, unlike classical bits that are either 0 or 1. This allows quantum computers to process vast amounts of information and solve certain complex problems much faster than traditional computers. They have potential applications in cryptography, drug development, weather forecasting, and complex system optimization."
                },
                {
                    "question": "How do smartphones work?",
                    "answer": "Smartphones are essentially miniature computers that combine various technologies. They have processors that run operating systems and applications, cellular radios for communication, GPS for location tracking, various sensors (accelerometer, proximity sensor, etc.), and touchscreens for user interaction. They function by converting your touch inputs into electrical signals that the processor interprets to perform actions."
                },
                {
                    "question": "What is machine learning?",
                    "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It involves algorithms that identify patterns in data, make decisions, and improve over time. Common applications include recommendation systems, speech recognition, image classification, and predictive analytics."
                },
                {
                    "question": "How do dreams work?",
                    "answer": "Dreams occur primarily during REM (Rapid Eye Movement) sleep when brain activity is high. Scientists believe dreams may help process emotions, consolidate memories, and solve problems. The prefrontal cortex (responsible for logic) is less active during dreams, while the amygdala (involved in emotions) is more active, which may explain why dreams often have emotional content and unusual logic."
                },
                {
                    "question": "What is cryptocurrency?",
                    "answer": "Cryptocurrency is a digital or virtual currency that uses cryptography for security and operates on decentralized networks based on blockchain technology. Unlike traditional currencies issued by governments, cryptocurrencies typically aren't controlled by any central authority. Bitcoin, created in 2009, was the first cryptocurrency, but there are now thousands of different cryptocurrencies with various functions and specifications."
                }
            ]
            # Save the default knowledge base
            try:
                with open('knowledge_base.json', 'w') as file:
                    json.dump(default_kb, file, indent=4)
                print("Created a new knowledge base file with default entries.")
            except Exception as e:
                print(f"Warning: Couldn't save knowledge base: {e}")
            return default_kb
    
    def save_knowledge_base(self):
        """Saves the knowledge base to a JSON file."""
        try:
            with open('knowledge_base.json', 'w') as file:
                json.dump(self.knowledge_base, file, indent=4)
        except Exception as e:
            print(f"Warning: Couldn't save knowledge base: {e}")
    
    def preprocess_text(self, text):
        """Preprocesses text for NLP tasks."""
        global NLP_AVAILABLE
        if not NLP_AVAILABLE:
            return text.lower()
        try:
            word_tokens = word_tokenize(text.lower())
            filtered_text = [self.lemmatizer.lemmatize(w) for w in word_tokens if w not in self.stop_words]
            return " ".join(filtered_text)
        except Exception:
            return text.lower()

    def split_into_questions(self, text):
        """Splits a text into individual questions more reliably."""
        global NLP_AVAILABLE
        if NLP_AVAILABLE:
            try:
                # Use NLTK's sentence tokenizer to split text into sentences
                sentences = sent_tokenize(text)
                # Filter sentences that are likely questions
                questions = [s.strip() for s in sentences if self.is_question(s)]
                if not questions:  # If no questions were found, treat the whole text as one question
                    return [text.strip()]
                return questions
            except Exception as e:
                print(f"Warning: Error in NLP sentence splitting: {e}")
                # Fall back to regex if NLTK fails
                return self.split_questions_regex(text)
        else:
            return self.split_questions_regex(text)

    def split_questions_regex(self, text):
        """Splits text into questions using improved regex patterns."""
        # Split by common sentence terminators
        question_parts = re.split(r'(?<=[.!?])\s+', text)
        # Filter only parts that are likely questions and clean them
        questions = [part.strip() for part in question_parts if part.strip() and self.is_question(part)]
        
        # Handle the case where no questions were identified but the text might contain question marks
        if not questions and '?' in text:
            # Try to split by question marks
            question_parts = re.split(r'\?', text)
            questions = [f"{part.strip()}?" for part in question_parts if part.strip()]
        
        # If still no questions, treat the whole text as one query
        if not questions:
            return [text.strip()]
        
        return questions
    
    def extract_math_expressions(self, text):
        """Extracts math expressions from text."""
        # Define regex patterns for math expressions
        math_patterns = [
            r'\b\d+\s*[\+\-\*\/\^]\s*\d+\b',  # Simple operations like 4+5
            r'\b\d+\s*[\+\-\*\/\^]\s*\d+\s*[\+\-\*\/\^]\s*\d+\b',  # Complex operations like 4+5*6
            r'\b\d+\s*[\+\-\*\/\^]\s*\(\s*\d+\s*[\+\-\*\/\^]\s*\d+\s*\)\b',  # Operations with parentheses
            r'solve\s+([0-9\+\-\*\/\^\(\)\s]+)',  # When "solve" is used as a keyword
            r'calculate\s+([0-9\+\-\*\/\^\(\)\s]+)',  # When "calculate" is used as a keyword
            r'compute\s+([0-9\+\-\*\/\^\(\)\s]+)',  # When "compute" is used as a keyword
            r'what is\s+([0-9\+\-\*\/\^\(\)\s]+)',  # When "what is" is used as a keyword
        ]
        
        math_expressions = []
        for pattern in math_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # If the pattern has a capture group, use it; otherwise use the full match
                if match.groups():
                    math_expressions.append(match.group(1).strip())
                else:
                    math_expressions.append(match.group(0).strip())
        
        return math_expressions

    def detect_emotion(self, text):
        """Detects the emotional tone of the input."""
        text_lower = text.lower()
        
        # Simple emotion detection based on keywords
        happy_words = ['happy', 'glad', 'joy', 'excited', 'wonderful', 'great', 'awesome', 'fantastic', 'amazing', 'excellent']
        sad_words = ['sad', 'unhappy', 'depressed', 'miserable', 'disappointed', 'upset', 'down', 'terrible', 'bad', 'awful']
        excited_words = ['excited', 'thrilled', 'ecstatic', 'can\'t wait', 'looking forward', 'pumped', 'stoked', 'eager', 'enthusiastic']
        frustrated_words = ['frustrated', 'annoyed', 'irritated', 'angry', 'mad', 'furious', 'tired of', 'sick of', 'fed up']
        
        # Check for emotion words
        for word in happy_words:
            if word in text_lower:
                return "happy"
                
        for word in sad_words:
            if word in text_lower:
                return "sad"
                
        for word in excited_words:
            if word in text_lower:
                return "excited"
                
        for word in frustrated_words:
            if word in text_lower:
                return "frustrated"
                
        return None

    def detect_topic(self, text):
        """Detects the topic of the conversation based on keywords."""
        text_lower = text.lower()
        
        # Topic detection based on keywords
        tech_words = ['technology', 'computer', 'software', 'hardware', 'app', 'digital', 'electronic', 'device', 'smartphone', 'internet', 'tech', 'coding', 'programming']
        movie_words = ['movie', 'film', 'cinema', 'actor', 'actress', 'director', 'hollywood', 'watch', 'theater', 'series', 'show', 'tv']
        book_words = ['book', 'read', 'author', 'novel', 'story', 'literature', 'fiction', 'nonfiction', 'chapter', 'page', 'character', 'plot']
        music_words = ['music', 'song', 'band', 'artist', 'album', 'concert', 'listen', 'playlist', 'genre', 'instrument', 'melody', 'rhythm']
        food_words = ['food', 'eat', 'cook', 'recipe', 'meal', 'restaurant', 'cuisine', 'taste', 'flavor', 'dish', 'ingredient', 'dinner', 'lunch', 'breakfast']
        travel_words = ['travel', 'trip', 'vacation', 'visit', 'country', 'city', 'place', 'destination', 'journey', 'tour', 'sight', 'location', 'explore']
        
        # Check for topic words
        for word in tech_words:
            if word in text_lower:
                return "technology"
                
        for word in movie_words:
            if word in text_lower:
                return "movies"
                
        for word in book_words:
            if word in text_lower:
                return "books"
                
        for word in music_words:
            if word in text_lower:
                return "music"
                
        for word in food_words:
            if word in text_lower:
                return "food"
                
        for word in travel_words:
            if word in text_lower:
                return "travel"
                
        return None

    def parse_mixed_input(self, text):
        """
        Parses mixed input that may contain greetings, questions, and math expressions.
        Returns a dictionary with categorized parts of the input.
        """
        result = {
            'greetings': [],
            'questions': [],
            'math_expressions': [],
            'commands': [],
            'remainder': text,  # Default to the full text
            'emotion': self.detect_emotion(text),
            'topic': self.detect_topic(text)
        }
        
        # Extract math expressions
        math_expressions = self.extract_math_expressions(text)
        if math_expressions:
            result['math_expressions'] = math_expressions
        
        # Check for common greetings
        greeting_patterns = [
            r'\bhello\b', r'\bhi\b', r'\bhey\b', r'\bgreetings\b', 
            r'\bgood morning\b', r'\bgood afternoon\b', r'\bgood evening\b',
            r'\bhowdy\b', r'\bsup\b', r'\byo\b', r'\bhiya\b'
        ]
        
        for pattern in greeting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                result['greetings'].append(re.search(pattern, text, re.IGNORECASE).group(0))
        
        # Extract questions
        questions = self.split_into_questions(text)
        if questions and len(questions) > 1:  # Only consider multiple questions as split
            result['questions'] = questions
        
        # Check for commands
        for pattern in self.commands:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result['commands'].append((pattern, match.groups()))
        
        return result

    def is_question(self, text):
        """Improved method to determine if text is likely a question."""
        if not text or not isinstance(text, str):
            return False
        
        # Clean the text
        text = text.strip()
        if not text:
            return False
        
        # Check for question mark - strongest indicator
        if text.endswith('?'):
            return True
        
        # Check for question starters
        question_starters = [
            'what', 'who', 'where', 'when', 'why', 'how', 
            'can', 'could', 'would', 'should', 'will', 'shall',
            'is', 'are', 'was', 'were', 'am', 'do', 'does', 'did',
            'have', 'has', 'had', 'may', 'might', 'must'
        ]
        
        # Split and get first word, handling punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        if words and words[0] in question_starters:
            return True
        
        # Check for inverted subject-verb pattern (common in questions)
        inverted_patterns = [
            r'^(is|are|was|were|do|does|did|have|has|had|can|could|would|should|will) [a-z]+',
            r'^(have|has|had) [a-z]+ been'
        ]
        
        for pattern in inverted_patterns:
            if re.search(pattern, text.lower()):
                return True
        
        return False
    
    def answer_question(self, question):
        """Searches the knowledge base for an answer to the question."""
        global NLP_AVAILABLE
        if not self.knowledge_base:
            return None
            
        if NLP_AVAILABLE:
            try:
                # Preprocess the question
                processed_question = self.preprocess_text(question)
                # Transform the question using the fitted vectorizer
                question_vector = self.vectorizer.transform([processed_question])
                # Calculate similarity with all questions in the knowledge base
                similarities = cosine_similarity(question_vector, self.tfidf_matrix).flatten()
                # Find the most similar question
                best_match_index = np.argmax(similarities)
            # If similarity is above threshold, return the answer
                if similarities[best_match_index] > 0.3:
                    return self.knowledge_base[best_match_index]['answer']
            except Exception as e:
                print(f"Warning: Error in NLP question answering: {e}")
                # Fall back to simple keyword matching
                return self.keyword_match_answer(question)
        else:
            return self.keyword_match_answer(question)
        return None
    
    def keyword_match_answer(self, question):
        """Simple keyword matching for questions when NLP is not available."""
        question = question.lower()
        best_match = None
        best_score = 0
        for entry in self.knowledge_base:
            kb_question = entry['question'].lower()
            # Count matching words
            question_words = set(re.findall(r'\b\w+\b', question))
            kb_words = set(re.findall(r'\b\w+\b', kb_question))
            common_words = question_words.intersection(kb_words)
            # Calculate a simple match score
            score = len(common_words) / max(len(question_words), 1)
            if score > best_score and score > 0.3:  # Threshold
                best_score = score
                best_match = entry['answer']
        return best_match
    
    def search_web(self, query):
        """Simulates searching the web for an answer to the question."""
        try:
            # This is a placeholder for a real API call
            # In a real implementation, you'd use a service like Wikipedia API, DuckDuckGo API, etc.
            search_responses = [
                f"I looked that up for you! According to what I found, '{query}' is related to several interesting topics...",
                f"Let me search that for you. From what I can see, '{query}' has some fascinating aspects...",
                f"I checked some sources on '{query}' and found some relevant information that might help...",
                f"Based on current information, '{query}' is generally understood to involve..."
            ]
            return random.choice(search_responses)
        except Exception as e:
            return f"I tried to search for information about '{query}', but encountered an issue. Maybe we could try a different approach?"
    
    def learn_from_answer(self, question, answer):
        """Adds a new question-answer pair to the knowledge base."""
        global NLP_AVAILABLE
        new_entry = {
            "question": question,
            "answer": answer
        }
        self.knowledge_base.append(new_entry)
        # Update the TF-IDF matrix if NLP is available
        if NLP_AVAILABLE:
            try:
                questions = [item['question'] for item in self.knowledge_base]
                self.tfidf_matrix = self.vectorizer.fit_transform(questions)
            except Exception as e:
                print(f"Warning: Couldn't update TF-IDF matrix: {e}")
        # Save the updated knowledge base
        self.save_knowledge_base()
        
        # More human-like confirmation responses
        confirmations = [
            f"I've added that to my knowledge! Now I know that {question} → {answer}",
            f"Thanks for teaching me that! I'll remember that {question} is about {answer}",
            f"Got it! I've saved that {question} relates to {answer}",
            f"I've learned something new today! I'll remember your explanation about {question}"
        ]
        return random.choice(confirmations)
    
    def solve_math(self, expression):
        """Solves a mathematical expression using SymPy."""
        try:
            # Handle common words that might appear in math problems
            expression = expression.replace('square root', 'sqrt')
            expression = expression.replace('cubed', '**3')
            expression = expression.replace('squared', '**2')
            expression = expression.replace('plus', '+')
            expression = expression.replace('minus', '-')
            expression = expression.replace('times', '*')
            expression = expression.replace('divided by', '/')
            
            # Clean up the expression by keeping only valid math characters
            cleaned_expression = re.sub(r'[^0-9+\-*/().\s^]', '', expression)
            
            # Remove keywords like "solve", "calculate", etc.
            keywords = ['solve', 'calculate', 'compute', 'what is']
            for keyword in keywords:
                cleaned_expression = re.sub(f'{keyword}\s+', '', cleaned_expression, flags=re.IGNORECASE)
                
            # Clean up the expression
            cleaned_expression = cleaned_expression.replace('^', '**').strip()
            
            # Solve the math problem
            result = sp.sympify(cleaned_expression)
            
            # More conversational math responses
            math_responses = [
                f"I calculated that {expression} equals {result}.",
                f"The result of {expression} is {result}.",
                f"I worked out {expression} and got {result}.",
                f"That would be {result}."
            ]
            return random.choice(math_responses)
        except Exception as e:
            error_responses = [
                "I'm having a bit of trouble with that calculation. Could you double-check the expression?",
                "Hmm, that math problem is challenging me. Is the formula formatted correctly?",
                "I'm not quite able to solve that. Could you rephrase the math problem?",
                "Something's not quite right with that expression. Could you try writing it differently?"
            ]
            return random.choice(error_responses)
    
    def get_time(self, *args):
        """Returns the current time with varied responses."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        time_responses = [
            f"It's currently {current_time}.",
            f"The time right now is {current_time}.",
            f"It's {current_time} at the moment.",
            f"My clock shows {current_time}."
        ]
        return random.choice(time_responses)
    
    def get_date(self, *args):
        """Returns the current date with varied responses."""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        date_responses = [
            f"Today is {current_date}.",
            f"It's {current_date}.",
            f"The date today is {current_date}.",
            f"According to my calendar, it's {current_date}."
        ]
        return random.choice(date_responses)
    
    def get_name(self, *args):
        """Returns the chatbot's name and information."""
        name_responses = [
            "I'm an AI chatbot designed to have helpful conversations with you. You can call me Assistant if you'd like!",
            "I'm your friendly AI assistant. I don't have a specific name, but you're welcome to give me one!",
            "I'm an AI conversation partner here to chat, answer questions, and assist you. What would you like to call me?",
            "Just think of me as your helpful AI friend. I'm here to chat and help with whatever you need."
        ]
        # Add user name if known
        if self.user_name:
            personal_responses = [
                f"I'm your AI assistant, {self.user_name}! What can I help you with today?",
                f"I'm here to chat and help you, {self.user_name}. You can call me whatever you'd like!",
                f"Hello {self.user_name}! I'm your AI conversation partner. What would you like to talk about?"
            ]
            return random.choice(personal_responses)
        return random.choice(name_responses)
    
    def get_chat_duration(self, *args):
        """Returns how long the chat has been going."""
        elapsed = time.time() - self.chat_start_time
        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            duration = f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}"
        elif minutes > 0:
            duration = f"{minutes} minute{'s' if minutes != 1 else ''}, {seconds} second{'s' if seconds != 1 else ''}"
        else:
            duration = f"{seconds} second{'s' if seconds != 1 else ''}"
            
        responses = [
            f"We've been chatting for {duration}.",
            f"Our conversation has been going for {duration}.",
            f"It's been {duration} since we started talking.",
            f"Time flies! We've been chatting for {duration} already."
        ]
        return random.choice(responses)
    
    def set_user_name(self, name):
        """Sets the user's name."""
        self.user_name = name.strip()
        name_responses = [
            f"Nice to meet you, {self.user_name}! I'll remember your name.",
            f"Hello {self.user_name}! I'll keep that in mind.",
            f"Great! I'll call you {self.user_name} from now on.",
            f"It's a pleasure to meet you, {self.user_name}!"
        ]
        return random.choice(name_responses)
    
    def remember_preference(self, key, value):
        """Stores user preference with more natural responses."""
        self.user_preferences[key] = value
        preference_responses = [
            f"I'll remember that your {key} is {value}.",
            f"Got it! Your {key} is {value}. I'll keep that in mind.",
            f"Thanks for sharing! I'll remember your {key} is {value}.",
            f"I've noted that your {key} is {value} for future reference."
        ]
        return random.choice(preference_responses)
    
    def recall_preference(self, _, key):
        """Recalls stored user preference with varied responses."""
        if key in self.user_preferences:
            recall_responses = [
                f"You mentioned your {key} is {self.user_preferences[key]}.",
                f"I remember you told me your {key} is {self.user_preferences[key]}.",
                f"Based on what you've shared, your {key} is {self.user_preferences[key]}.",
                f"According to my notes, your {key} is {self.user_preferences[key]}."
            ]
            return random.choice(recall_responses)
        else:
            unknown_responses = [
                f"You haven't told me your {key} yet.",
                f"I don't think you've mentioned your {key} before.",
                f"I don't have any information about your {key} yet.",
                f"I don't recall you sharing your {key} with me."
            ]
            return random.choice(unknown_responses)
    
    def learn_response(self, trigger, response):
        """Learns a new response pattern with varied confirmations."""
        self.learning_dictionary[trigger.strip()] = response.strip()
        learn_responses = [
            f"I've learned to respond to '{trigger}' with '{response}'.",
            f"Got it! When you mention '{trigger}', I'll reply with '{response}'.",
            f"I'll remember that! When you say '{trigger}', I should respond with '{response}'.",
            f"Thanks for teaching me! I've associated '{trigger}' with '{response}'."
        ]
        return random.choice(learn_responses)
    
    def check_learned_response(self, trigger):
        """Checks what response is associated with a learned trigger."""
        if trigger.strip() in self.learning_dictionary:
            check_responses = [
                f"For '{trigger}', I'll respond with: '{self.learning_dictionary[trigger.strip()]}'.",
                f"I've learned to reply to '{trigger}' with '{self.learning_dictionary[trigger.strip()]}'.",
                f"When you mention '{trigger}', I'll say '{self.learning_dictionary[trigger.strip()]}'.",
                f"I know that '{trigger}' should prompt me to respond with '{self.learning_dictionary[trigger.strip()]}'."
            ]
            return random.choice(check_responses)
        else:
            unknown_responses = [
                f"I haven't learned anything about '{trigger}' yet.",
                f"I don't have any specific response for '{trigger}' in my memory.",
                f"You haven't taught me how to respond to '{trigger}' yet.",
                f"I don't recognize '{trigger}' as something you've taught me about."
            ]
            return random.choice(unknown_responses)
    
    def tell_joke(self, *args):
        """Returns a random joke with more variety."""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why couldn't the bicycle stand up by itself? It was two tired!",
            "How does a computer get drunk? It takes screenshots!",
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why did the coffee file a police report? It got mugged.",
            "What did the ocean say to the beach? Nothing, it just waved.",
            "Why don't eggs tell jokes? They'd crack each other up.",
            "What's orange and sounds like a parrot? A carrot!",
            "Why did the math book look sad? Because it had too many problems.",
            "What do you call a bear with no teeth? A gummy bear!",
            "How do you organize a space party? You planet!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
            "What do you call cheese that isn't yours? Nacho cheese!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "How do you catch a squirrel? Climb a tree and act like a nut!",
            "What's the best time to go to the dentist? Tooth-hurty!"
        ]
        joke = random.choice(jokes)
        joke_intros = [
            "Here's one for you: ",
            "This one always makes me laugh: ",
            "How about this: ",
            "Here's a classic: ",
            "I hope this brightens your day: ",
            "Try this one on for size: ",
            "This joke is my favorite: ",
            ""  # Sometimes no intro is more natural
        ]
        return f"{random.choice(joke_intros)}{joke}"
    
    def flip_coin(self, *args):
        """Simulates flipping a coin with varied responses."""
        result = random.choice(['Heads', 'Tails'])
        coin_responses = [
            f"I flipped a coin and got: {result}!",
            f"The coin landed on {result}.",
            f"It's {result}!",
            f"*flips coin* ... It's {result}!"
        ]
        return random.choice(coin_responses)
    
    def roll_dice(self, *args):
        """Simulates rolling a 6-sided dice with varied responses."""
        result = random.randint(1, 6)
        dice_responses = [
            f"I rolled a dice and got: {result}!",
            f"The dice shows {result}.",
            f"*rolls dice* ... It's a {result}!",
            f"You rolled a {result}."
        ]
        return random.choice(dice_responses)
    
    def roll_n_sided_dice(self, sides):
        """Simulates rolling an n-sided dice with varied responses."""
        try:
            sides = int(sides)
            result = random.randint(1, sides)
            roll_responses = [
                f"I rolled a {sides}-sided dice and got: {result}!",
                f"The {sides}-sided dice shows {result}.",
                f"*rolls {sides}-sided dice* ... It's a {result}!",
                f"You rolled a {result} on a {sides}-sided dice."
            ]
            return random.choice(roll_responses)
        except ValueError:
            error_responses = [
                "I need a valid number of sides for the dice.",
                "Could you specify a proper number for the dice sides?",
                "I'm not sure I understand how many sides you want on the dice.",
                "I need a number to know how many sides the dice should have."
            ]
            return random.choice(error_responses)
    
    def get_weather(self, location):
        """Gets weather information for a location with varied responses."""
        try:
            weather_conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "clear", "stormy", "windy", "foggy", "snowy"]
            temperatures = [f"{random.randint(50, 90)}°F", f"{random.randint(10, 32)}°C"]
            weather = random.choice(weather_conditions)
            temp = random.choice(temperatures)
            
            weather_responses = [
                f"In {location}, it's currently {weather} with a temperature of {temp}.",
                f"The weather in {location} right now is {weather} and {temp}.",
                f"Looking at {location}, you can expect {weather} conditions and around {temp}.",
                f"{location} is experiencing {weather} weather with temperatures at {temp}."
            ]
            
            disclaimer = " (Note: This is simulated data. In a real implementation, I would connect to a weather service.)"
            return random.choice(weather_responses) + disclaimer
        except Exception as e:
            error_responses = [
                f"I couldn't get the weather for {location}. Could you try another location?",
                f"I'm having trouble accessing weather data for {location}. Maybe try asking differently?",
                f"Something went wrong when checking {location}'s weather. Could you try again later?",
                f"I'm not able to get weather information for {location} right now."
            ]
            return random.choice(error_responses)
    
    def get_definition(self, word):
        """Gets the definition of a word with varied responses."""
        try:
            # Simulate dictionary definitions for common words
            common_definitions = {
                "happy": "feeling or showing pleasure or contentment",
                "sad": "feeling or showing sorrow; unhappy",
                "computer": "an electronic device for storing and processing data",
                "love": "an intense feeling of deep affection",
                "book": "a written or printed work consisting of pages bound together",
                "friend": "a person whom one knows and with whom one has a bond of mutual affection",
                "time": "the indefinite continued progress of existence and events in the past, present, and future",
                "food": "any nutritious substance that people or animals eat or drink to maintain life and growth",
                "water": "a colorless, transparent, odorless liquid that forms the seas, lakes, rivers, and rain",
                "music": "vocal or instrumental sounds combined in such a way as to produce beauty of form, harmony, and expression of emotion"
            }
            
            if word.lower() in common_definitions:
                definition = common_definitions[word.lower()]
                definition_responses = [
                    f"The word '{word}' means: {definition}.",
                    f"'{word}' is defined as: {definition}.",
                    f"According to definitions I know, '{word}' refers to {definition}.",
                    f"The meaning of '{word}' is {definition}."
                ]
                return random.choice(definition_responses)
            else:
                return f"I would look up the definition of '{word}' for you, but I need access to a dictionary service for that. In a full implementation, this would connect to a dictionary API."
        except Exception as e:
            error_responses = [
                f"I'm having trouble finding the definition of '{word}'. Could you try another word?",
                f"I can't seem to look up '{word}' right now. Maybe try a different term?",
                f"I'm not able to access definition data for '{word}' at the moment.",
                f"Something went wrong when defining '{word}'. Could you try again?"
            ]
            return random.choice(error_responses)
    
    def should_add_followup_question(self):
        """Determines if a follow-up question should be added to the response."""
        # Add follow-up questions occasionally (30% chance)
        return random.random() < 0.3
    
    def process_input(self, user_input):
        """Enhanced method to process mixed user input with more human-like responses."""
        # Add to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Clean input
        cleaned_input = user_input.strip()
        
        # Parse the mixed input
        parsed_input = self.parse_mixed_input(cleaned_input)
        
        # Initialize response parts
        response_parts = []
        
        # Remember detected topic if found
        if parsed_input['topic']:
            self.last_topic = parsed_input['topic']
        
        # First, check for command patterns
        for pattern, args in parsed_input['commands']:
            for cmd_pattern, cmd_function in self.commands.items():
                if pattern == cmd_pattern:
                    response = cmd_function(*args)
                    response_parts.append(response)
                    break
        
        # If commands were found, return immediately
        if response_parts:
            combined_response = " ".join(response_parts)
            
            # Occasionally add a follow-up question related to the command
            if self.should_add_followup_question():
                combined_response += f" {random.choice(self.follow_up_questions)}"
            
            self.conversation_history.append(("bot", combined_response))
            return combined_response
        
        # Check learned responses
        for trigger, response in self.learning_dictionary.items():
            if trigger.lower() in cleaned_input.lower():
                self.conversation_history.append(("bot", response))
                return response
        
        # Process greetings
        if parsed_input['greetings']:
            for greeting in parsed_input['greetings']:
                greeting_lower = greeting.lower()
                if greeting_lower in self.responses:
                    response_parts.append(random.choice(self.responses[greeting_lower]))
                elif "hello" in greeting_lower or "hi" in greeting_lower or "hey" in greeting_lower:
                    response_parts.append(random.choice(self.responses["hello"]))
        
        # Process emotions if detected
        if parsed_input['emotion'] and not response_parts:  # Only if no greeting response yet
            response_parts.append(random.choice(self.emotional_responses[parsed_input['emotion']]))
        
        # Process math expressions
        if parsed_input['math_expressions']:
            for expr in parsed_input['math_expressions']:
                math_result = self.solve_math(expr)
                response_parts.append(math_result)
        
        # Process questions
        if parsed_input['questions']:
            for q in parsed_input['questions']:
                if "how are you" in q.lower() or "how're you" in q.lower() or "how are you doing" in q.lower():
                    response_parts.append(random.choice(self.responses["how are you"]))
                elif "thank you" in q.lower() or "thanks" in q.lower():
                    response_parts.append(random.choice(self.responses["thank you"]))
                else:
                    answer = self.get_answer_for_question(q)
                    if answer:
                        # Format multi-question responses when there are other components
                        if len(parsed_input['questions']) > 1 or response_parts:
                            response_parts.append(f"About '{q}': {answer}")
                        else:
                            response_parts.append(answer)
        
        # If no specific parts were processed, check the entire input
        if not response_parts:
            # Try common phrases first
            for key in self.responses:
                if key in cleaned_input.lower():
                    response_parts.append(random.choice(self.responses[key]))
                    break
            
            # Check for topic responses if no specific response generated
            if not response_parts and self.last_topic:
                response_parts.append(random.choice(self.topic_responses[self.last_topic]))
            
            # If still nothing, use the default response
            if not response_parts:
                response_parts.append(random.choice(self.responses["default"]))
        
        # Combine all response parts
        combined_response = " ".join(response_parts)
        
        # Occasionally add a follow-up question
        if self.should_add_followup_question() and "?" not in combined_response:
            combined_response += f" {random.choice(self.follow_up_questions)}"
        
        self.conversation_history.append(("bot", combined_response))
        return combined_response

    def get_answer_for_question(self, question):
        """Helper method to get an answer for a single question."""
        # Try to find an answer in the knowledge base
        if self.is_question(question):
            answer = self.answer_question(question)
            if answer:
                return answer
        
        # Get response from predefined list if exact match exists
        if question.lower() in self.responses:
            return random.choice(self.responses[question.lower()])
        
        # Handle partial matches
        for key in self.responses:
            if key in question.lower():
                return random.choice(self.responses[key])
        
        # Check if it's a confused question
        confused_indicators = ["don't understand", "what do you mean", "confused", "not clear", "what's that", "what is that"]
        if any(indicator in question.lower() for indicator in confused_indicators):
            return random.choice(self.responses["confused"])
        
        # If no match found, use search simulation
        search_terms = re.sub(r'(what|who|when|where|why|how|is|are|do|does|can|could|would|should|will) ', '', question.lower())
        search_terms = re.sub(r'[?!.,]', '', search_terms).strip()
        
        if search_terms:
            return self.search_web(search_terms)
        
        # If all else fails, use default response
        return random.choice(self.responses["default"])
    
    def add_to_knowledge_base(self, user_input):
        """Allows the user to add new information to the knowledge base."""
        try:
            # Extract question and answer from user input
            parts = user_input.split('::')
            if len(parts) != 2:
                return "To add to my knowledge, use the format: 'learn question::answer'"
            question = parts[0].strip()
            answer = parts[1].strip()
            return self.learn_from_answer(question, answer)
        except Exception as e:
            return f"I'm having trouble adding that to my knowledge base. Could you try phrasing it differently?"

    def simulate_typing(self, message):
        """Simulates typing delay based on message length to appear more human-like."""
        delay = min(len(message) * 0.01, 1.5)  # Cap at 1.5 seconds
        time.sleep(delay)

def main():
    """Main function to run the chatbot with improved human-like interaction."""
    print("Initializing chatbot. This may take a moment...")
    chatbot = AIChatbot()
    print("\nChatbot: Hi there! I'm your AI conversation partner. How can I help you today?")
    print("Chatbot: You can ask me questions, chat about various topics, or just have a friendly conversation.")
    print("Chatbot: Type 'bye' when you'd like to end our conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "ok bye", "goodbye", "see ya", "cya", "farewell"]:
            response = random.choice(chatbot.responses["bye"])
            print("Chatbot:", response)
            break
        
        if user_input.lower().startswith("learn ") and "::" in user_input:
            response = chatbot.add_to_knowledge_base(user_input[6:])
        else:
            # Simulate thinking/typing for more human-like interaction
            print("Chatbot is typing...", end="\r")
            chatbot.simulate_typing(user_input)
            response = chatbot.process_input(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
