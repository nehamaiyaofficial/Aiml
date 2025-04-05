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
import threading
from typing import List, Dict, Tuple, Optional

# Global NLP availability flag
NLP_AVAILABLE = False

class AIChatbot:
    def __init__(self):
        # Access the global NLP_AVAILABLE variable
        global NLP_AVAILABLE
        
        # Initialize conversation memory
        self.conversation_history: List[Tuple[str, str]] = []
        self.user_preferences: Dict[str, str] = defaultdict(str)
        self.learning_dictionary: Dict[str, str] = {}
        self.user_name: str = ""
        self.last_topic: str = ""
        self.chat_start_time: float = time.time()
        self.is_typing: bool = False
        self.typing_event = threading.Event()
        
        # Personality traits
        self.personality = {
            "name": "Assistant",
            "tone": "friendly and helpful",
            "verbosity": "detailed",
            "formality": "balanced"
        }
        
        # Try to initialize NLP components
        self._initialize_nlp()
        
        # Knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize NLP components if available
        if NLP_AVAILABLE and self.knowledge_base:
            try:
                questions = [item['question'] for item in self.knowledge_base]
                self.tfidf_matrix = self.vectorizer.fit_transform(questions)
            except Exception as e:
                print(f"Error initializing TF-IDF matrix: {e}")
        
        # Command patterns
        self.commands = {
            r'(what|tell me).*time': self.get_time,
            r'(what|tell me).*date': self.get_date,
            r'remember (that )?my (\w+) is (.+)': self.remember_preference,
            r'my (\w+) is (.+)': self.remember_preference,
            r'what( is|\'s) my (\w+)': self.recall_preference,
            r'learn that (.*?) -> (.*)': self.learn_response,
            r'tell me a joke': self.tell_joke,
            r'(flip|toss) a coin': self.flip_coin,
            r'roll a dice': self.roll_dice,
            r'roll a (\d+)-sided dice': self.roll_n_sided_dice,
            r'weather in (.+)': self.get_weather,
            r'define (.+)': self.get_definition,
            r'what( is|\'s) your name': self.get_name,
            r'who are you': self.get_name,
            r'how long have we been talking': self.get_chat_duration,
            r'(my name is|call me) (.+)': self.set_user_name,
            r'(exit|quit|bye|goodbye)': self.exit_chat
        }

    def _initialize_nlp(self):
        """Initialize NLP components if available"""
        global NLP_AVAILABLE
        try:
            import nltk
            from nltk.tokenize import word_tokenize, sent_tokenize
            from nltk.corpus import stopwords
            from nltk.stem import WordNetLemmatizer
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Download NLTK data quietly
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            self.vectorizer = TfidfVectorizer()
            
            NLP_AVAILABLE = True
        except ImportError as e:
            print(f"NLP components not available: {e}")
            NLP_AVAILABLE = False
        except Exception as e:
            print(f"Error initializing NLP: {e}")
            NLP_AVAILABLE = False

    def _load_knowledge_base(self) -> List[Dict[str, str]]:
        """Load knowledge base from file or create default"""
        try:
            with open('knowledge_base.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default knowledge base
            default_kb = [
                {
                    "question": "What is AI?",
                    "answer": "Artificial Intelligence (AI) refers to systems or machines that mimic human intelligence to perform tasks and can iteratively improve themselves based on the information they collect."
                },
                {
                    "question": "Who invented the light bulb?",
                    "answer": "Thomas Edison is credited with inventing the practical incandescent light bulb, though earlier inventors like Joseph Swan also developed similar technologies."
                },
                {
                    "question": "What is the capital of France?",
                    "answer": "The capital of France is Paris."
                }
            ]
            try:
                with open('knowledge_base.json', 'w') as file:
                    json.dump(default_kb, file, indent=4)
            except Exception as e:
                print(f"Couldn't save knowledge base: {e}")
            return default_kb

    def _save_knowledge_base(self) -> None:
        """Save knowledge base to file"""
        try:
            with open('knowledge_base.json', 'w') as file:
                json.dump(self.knowledge_base, file, indent=4)
        except Exception as e:
            print(f"Couldn't save knowledge base: {e}")

    def typing_animation(self) -> None:
        """Display typing animation while generating response"""
        animations = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        while self.is_typing:
            for frame in animations:
                if not self.is_typing:
                    break
                print(f"\rAssistant: {frame} Thinking...", end='', flush=True)
                time.sleep(0.1)
        print('\r' + ' ' * 50 + '\r', end='')  # Clear line

    def get_time(self, *args) -> str:
        """Return current time"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    def get_date(self, *args) -> str:
        """Return current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    def remember_preference(self, _, key, value) -> str:
        """Store user preference"""
        self.user_preferences[key] = value
        return f"I'll remember your {key} is {value}."

    def recall_preference(self, _, key) -> str:
        """Recall user preference"""
        if key in self.user_preferences:
            return f"Your {key} is {self.user_preferences[key]}."
        return f"I don't know your {key} yet."

    def learn_response(self, trigger, response) -> str:
        """Learn a new response pattern"""
        self.learning_dictionary[trigger.strip()] = response.strip()
        return f"I've learned to respond to '{trigger}' with '{response}'."

    def tell_joke(self, *args) -> str:
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Why don't skeletons fight each other? They don't have the guts."
        ]
        return random.choice(jokes)

    def flip_coin(self, *args) -> str:
        """Flip a coin"""
        return f"It's {random.choice(['heads', 'tails'])}!"

    def roll_dice(self, *args) -> str:
        """Roll a 6-sided die"""
        return f"You rolled a {random.randint(1, 6)}!"

    def roll_n_sided_dice(self, sides) -> str:
        """Roll an n-sided die"""
        try:
            sides = int(sides)
            return f"You rolled a {random.randint(1, sides)} on a {sides}-sided die!"
        except ValueError:
            return "Please specify a valid number of sides."

    def get_weather(self, location) -> str:
        """Get weather for location (simulated)"""
        conditions = ["sunny", "cloudy", "rainy", "snowy"]
        temp = f"{random.randint(50, 90)}°F"
        return f"In {location}, it's currently {random.choice(conditions)} and {temp}."

    def get_definition(self, word) -> str:
        """Get definition of word (simulated)"""
        definitions = {
            "computer": "an electronic device for storing and processing data",
            "book": "a written or printed work consisting of pages bound together",
            "science": "the systematic study of the structure and behavior of the physical world"
        }
        if word.lower() in definitions:
            return f"{word.capitalize()}: {definitions[word.lower()]}"
        return f"I don't have a definition for '{word}' in my dictionary."

    def get_name(self, *args) -> str:
        """Return assistant name"""
        return f"I'm {self.personality['name']}, your AI assistant."

    def get_chat_duration(self, *args) -> str:
        """Return chat duration"""
        elapsed = time.time() - self.chat_start_time
        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            duration = f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}"
        elif minutes > 0:
            duration = f"{minutes} minute{'s' if minutes != 1 else ''}, {seconds} second{'s' if seconds != 1 else ''}"
        else:
            duration = f"{seconds} second{'s' if seconds != 1 else ''}"
            
        return f"We've been chatting for {duration}."

    def set_user_name(self, _, name) -> str:
        """Set user's name"""
        self.user_name = name.strip()
        return f"Nice to meet you, {self.user_name}! I'll remember your name."

    def exit_chat(self, *args) -> None:
        """Handle chat exit"""
        response = f"Goodbye{f', {self.user_name}' if self.user_name else ''}! It was nice chatting with you."
        print(f"Assistant: {response}")
        exit(0)

    def chat_loop(self) -> None:
        """Main chat loop"""
        print("Assistant: Hello! How can I help you today?")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                
                # Start typing animation
                self.is_typing = True
                typing_thread = threading.Thread(target=self.typing_animation)
                typing_thread.start()
                
                # Process input
                response = self._process_input(user_input)
                
                # Stop typing animation
                self.is_typing = False
                typing_thread.join()
                
                print(f"Assistant: {response}")
            
            except KeyboardInterrupt:
                self.exit_chat()
            except Exception as e:
                print(f"Assistant: I encountered an error. Could you try again?")
                print(f"(Debug: {str(e)})")

    def _process_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Check for commands first
        for pattern, handler in self.commands.items():
            if match := re.search(pattern, user_input, re.IGNORECASE):
                return handler(*match.groups())
        
        # Check learned responses
        for trigger, response in self.learning_dictionary.items():
            if trigger.lower() in user_input.lower():
                return response
        
        # If it's a question, try to answer it
        if self._is_question(user_input):
            answer = self._answer_question(user_input)
            if answer:
                return answer
        
        # Default response
        return "I'm not sure how to respond to that. Could you rephrase or ask something else?"

    def _is_question(self, text: str) -> bool:
        """Check if text is a question"""
        return text.endswith('?') or any(
            text.lower().startswith(q_word) 
            for q_word in ['what', 'who', 'where', 'when', 'why', 'how', 'is', 'are']
        )

    def _answer_question(self, question: str) -> Optional[str]:
        """Answer a question from knowledge base"""
        if not self.knowledge_base:
            return None
            
        # Simple keyword matching (could be enhanced with NLP if available)
        question_lower = question.lower()
        for entry in self.knowledge_base:
            if any(word in question_lower for word in entry['question'].lower().split()):
                return entry['answer']
        
        return None

if __name__ == "__main__":
    bot = AIChatbot()
    bot.chat_loop()
