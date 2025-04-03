#!/usr/bin/env python3
import random
import re
import sympy as sp
import datetime
import requests
import json
import numpy as np
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AIChatbot:
    def __init__(self):
        # Initialize conversation memory
        self.conversation_history = []
        self.user_preferences = defaultdict(str)
        self.learning_dictionary = {}
        
        # Initialize NLP components
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            print("NLP components initialized successfully.")
        except ImportError:
            print("NLTK not installed. Some NLP features will be limited.")
            self.lemmatizer = None
            self.stop_words = set()
        
        # Knowledge base for general questions
        self.knowledge_base = self.load_knowledge_base()
        
        # Initialize the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        if self.knowledge_base:
            questions = [item['question'] for item in self.knowledge_base]
            self.tfidf_matrix = self.vectorizer.fit_transform(questions)
        
        # Predefined responses
        self.responses = {
            "hello": [
                "Hey there! How's your day going?",
                "Hello! What's on your mind today?",
                "Hi there! Need help with something?",
                "Greetings! What exciting thing do we chat about today?"
            ],
            "how are you": [
                "I'm just a bunch of code, but I'm feeling pretty smart today.",
                "I don't have emotions, but if I did, I'd be happy talking to you.",
                "Functioning at 100% efficiency! What about you?",
                "Running at optimal AI levels! What's up?"
            ],
            "what can you do": [
                "I can chat, answer questions on various topics, tell jokes, solve math problems, remember details about you, learn new responses, and more!",
                "Besides chatting, I can solve equations, answer general knowledge questions, remember our conversation, learn new things, and even attempt humor.",
                "Think of me as your AI assistant—I can search for answers to your questions, remember details from our chat, solve math problems, and more.",
                "I can help with math, general knowledge, random fun facts, remember your preferences, and even answer questions about science, history, and technology."
            ],
            "who created you": [
                "I was crafted by a developer who probably drinks too much coffee.",
                "A programmer built me with a mix of logic and creativity.",
                "I came into existence through lines of code and some AI magic.",
                "A tech-savvy human gave me life. AI evolution at its finest."
            ],
            "bye": [
                "Goodbye! Had fun chatting with you. Come back soon.",
                "See you later. Stay awesome.",
                "Take care! I'll be here when you need me.",
                "Logging off… Just kidding. I'm always online."
            ],
            "ok bye": [
                "Alright, bye! Come back soon for more fun chats.",
                "Okay, see you later! Stay curious.",
                "Goodbye! It was great talking with you.",
                "Take care! I'll be waiting for our next conversation."
            ],
            "default": [
                "Hmm… I'm not sure about that, but I'd love to learn.",
                "Interesting! Can you rephrase or give me more details?",
                "That's a great question! Let me process that.",
                "I don't know that one yet, but I'm always learning."
            ]
        }
        
        # Command patterns
        self.commands = {
            r'what time is it': self.get_time,
            r'what( is|\'s) the date': self.get_date,
            r'remember that my (\w+) is (.+)': self.remember_preference,
            r'what( is|\'s) my (\w+)': self.recall_preference,
            r'learn that (.*?) -> (.*)': self.learn_response,
            r'what do you know about (.*)': self.check_learned_response,
            r'tell me a joke': self.tell_joke,
            r'flip a coin': self.flip_coin,
            r'roll a dice': self.roll_dice,
            r'roll a (\d+)-sided dice': self.roll_n_sided_dice,
            r'weather in (.+)': self.get_weather,
            r'define (.+)': self.get_definition
        }

    def load_knowledge_base(self):
        """Loads the knowledge base from a JSON file or creates a default one if not found."""
        try:
            with open('knowledge_base.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create a default knowledge base
            default_kb = [
                {
                    "question": "What is AI?",
                    "answer": "Artificial Intelligence (AI) refers to systems or machines that mimic human intelligence to perform tasks and can iteratively improve themselves based on the information they collect."
                },
                {
                    "question": "Who invented the light bulb?",
                    "answer": "Thomas Edison is typically credited with inventing the light bulb, though earlier inventors like Joseph Swan also developed similar technologies."
                },
                {
                    "question": "What is the capital of France?",
                    "answer": "Paris is the capital of France."
                },
                {
                    "question": "How far is the moon from Earth?",
                    "answer": "The average distance between the Earth and the Moon is about 238,855 miles (384,400 kilometers)."
                },
                {
                    "question": "What is the largest planet in our solar system?",
                    "answer": "Jupiter is the largest planet in our solar system."
                },
                {
                    "question": "How does photosynthesis work?",
                    "answer": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar."
                },
                {
                    "question": "Who wrote Romeo and Juliet?",
                    "answer": "William Shakespeare wrote Romeo and Juliet."
                },
                {
                    "question": "What is the theory of relativity?",
                    "answer": "The theory of relativity, developed by Albert Einstein, describes how space and time are linked for objects moving at a consistent speed in a straight line. It includes special relativity and general relativity theories."
                },
                {
                    "question": "What are black holes?",
                    "answer": "Black holes are regions of spacetime where gravity is so strong that nothing—including light or other electromagnetic waves—can escape from it."
                },
                {
                    "question": "How do vaccines work?",
                    "answer": "Vaccines work by training the immune system to recognize and combat pathogens by introducing a weakened or inactivated form of the pathogen, triggering an immune response without causing the disease."
                }
            ]
            # Save the default knowledge base
            with open('knowledge_base.json', 'w') as file:
                json.dump(default_kb, file, indent=4)
            print("Created a new knowledge base file with default entries.")
            return default_kb

    def save_knowledge_base(self):
        """Saves the knowledge base to a JSON file."""
        with open('knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file, indent=4)

    def preprocess_text(self, text):
        """Preprocesses text for NLP tasks."""
        if not self.lemmatizer:
            return text.lower()
        
        word_tokens = word_tokenize(text.lower())
        filtered_text = [self.lemmatizer.lemmatize(w) for w in word_tokens if w not in self.stop_words]
        return " ".join(filtered_text)

    def answer_question(self, question):
        """Searches the knowledge base for an answer to the question."""
        if not self.knowledge_base:
            return None
        
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
        
        # Try to get an answer from the web API
        try:
            return self.search_web(question)
        except:
            return None

    def search_web(self, query):
        """Searches the web for an answer to the question using a public API."""
        try:
            # This is a placeholder for a real API call
            # For a real implementation, you'd use a service like Wikipedia API, DuckDuckGo API, etc.
            api_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(api_url, timeout=5)
            data = response.json()
            
            # Extract abstract from the response
            if data.get("Abstract"):
                return data["Abstract"]
            
            # If no abstract, try to get answer from related topics
            if data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                return data["RelatedTopics"][0].get("Text", "No information found.")
            
            return "I couldn't find information about that online."
        except Exception as e:
            return f"I tried to search online, but encountered an error: {str(e)}"

    def learn_from_answer(self, question, answer):
        """Adds a new question-answer pair to the knowledge base."""
        new_entry = {
            "question": question,
            "answer": answer
        }
        self.knowledge_base.append(new_entry)
        
        # Update the TF-IDF matrix
        questions = [item['question'] for item in self.knowledge_base]
        self.tfidf_matrix = self.vectorizer.fit_transform(questions)
        
        # Save the updated knowledge base
        self.save_knowledge_base()
        
        return f"I've learned: Q: {question} A: {answer}"

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
            
            # Extract the math expression from the text
            math_pattern = r'[-+*/().\d\s^sincotan\w]+'
            match = re.search(math_pattern, expression)
            if match:
                expression = match.group(0)
            
            # Clean up the expression
            expression = expression.replace('^', '**')
            
            # Solve the math problem
            result = sp.sympify(expression)
            return f"The answer is: {result}"
        except Exception as e:
            return f"Oops! I couldn't solve that. Make sure it's a valid math expression. Error: {str(e)}"

    def get_time(self, *args):
        """Returns the current time."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    def get_date(self, *args):
        """Returns the current date."""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    def remember_preference(self, key, value):
        """Stores user preference."""
        self.user_preferences[key] = value
        return f"I'll remember that your {key} is {value}."

    def recall_preference(self, _, key):
        """Recalls stored user preference."""
        if key in self.user_preferences:
            return f"You told me your {key} is {self.user_preferences[key]}."
        else:
            return f"You haven't told me your {key} yet."

    def learn_response(self, trigger, response):
        """Learns a new response pattern."""
        self.learning_dictionary[trigger.strip()] = response.strip()
        return f"I've learned to respond to '{trigger}' with '{response}'."

    def check_learned_response(self, trigger):
        """Checks what response is associated with a learned trigger."""
        if trigger.strip() in self.learning_dictionary:
            return f"For '{trigger}', I'll respond with: '{self.learning_dictionary[trigger.strip()]}'."
        else:
            return f"I haven't learned anything about '{trigger}' yet."

    def tell_joke(self, *args):
        """Returns a random joke."""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why couldn't the bicycle stand up by itself? It was two tired!",
            "How does a computer get drunk? It takes screenshots!",
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up.",
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "Why did the invisible man turn down the job offer? He couldn't see himself doing it."
        ]
        return random.choice(jokes)

    def flip_coin(self, *args):
        """Simulates flipping a coin."""
        return f"I flipped a coin and got: {random.choice(['Heads', 'Tails'])}!"

    def roll_dice(self, *args):
        """Simulates rolling a 6-sided dice."""
        return f"I rolled a dice and got: {random.randint(1, 6)}!"

    def roll_n_sided_dice(self, sides):
        """Simulates rolling an n-sided dice."""
        try:
            sides = int(sides)
            return f"I rolled a {sides}-sided dice and got: {random.randint(1, sides)}!"
        except ValueError:
            return "Sorry, I need a valid number of sides for the dice."

    def get_weather(self, location):
        """Gets weather information for a location."""
        try:
            # This is a placeholder. In a real application, you would use a weather API
            # such as OpenWeatherMap or WeatherAPI
            return f"I would show you the weather in {location}, but I need an API key to access real weather data. In a full implementation, this would connect to a weather service."
        except Exception as e:
            return f"Sorry, I couldn't get the weather for {location}. Error: {str(e)}"

    def get_definition(self, word):
        """Gets the definition of a word."""
        try:
            # This is a placeholder. In a real application, you would use a dictionary API
            # such as Merriam-Webster or Oxford Dictionary API
            return f"I would show you the definition of '{word}', but I need an API key to access dictionary data. In a full implementation, this would connect to a dictionary service."
        except Exception as e:
            return f"Sorry, I couldn't find the definition for {word}. Error: {str(e)}"

    def check_for_math(self, user_input):
        """Checks if the input contains a math problem."""
        math_operators = ['+', '-', '*', '/', '^', '(', ')', 'sin', 'cos', 'tan', 'sqrt', 'log']
        return any(op in user_input for op in math_operators)

    def is_question(self, text):
        """Determines if the input is likely a question."""
        question_starters = ['what', 'who', 'where', 'when', 'why', 'how', 'can', 'could', 'would', 'should', 'is', 'are', 'was', 'were']
        first_word = text.split()[0].lower() if text.split() else ""
        return text.endswith('?') or first_word in question_starters

    def process_input(self, user_input):
        """Main method to process user input and generate a response."""
        # Add to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Clean input and convert to lowercase
        cleaned_input = user_input.lower().strip()
        
        # Check for command patterns
        for pattern, command_function in self.commands.items():
            match = re.match(pattern, cleaned_input)
            if match:
                groups = match.groups()
                response = command_function(*groups)
                self.conversation_history.append(("bot", response))
                return response
        
        # Check learned responses
        for trigger, response in self.learning_dictionary.items():
            if trigger.lower() in cleaned_input:
                self.conversation_history.append(("bot", response))
                return response
        
        # Check if input is a math problem
        if self.check_for_math(cleaned_input):
            response = self.solve_math(cleaned_input)
            self.conversation_history.append(("bot", response))
            return response
        
        # Check if the input is likely a question
        if self.is_question(cleaned_input):
            # Try to find an answer in the knowledge base
            answer = self.answer_question(cleaned_input)
            if answer:
                self.conversation_history.append(("bot", answer))
                return answer
        
        # Get response from predefined list if exact match exists
        if cleaned_input in self.responses:
            response = random.choice(self.responses[cleaned_input])
            self.conversation_history.append(("bot", response))
            return response
            
        # Handle partial matches
        for key in self.responses:
            if key in cleaned_input:
                response = random.choice(self.responses[key])
                self.conversation_history.append(("bot", response))
                return response
        
        # If no match found, use default response
        response = random.choice(self.responses["default"])
        self.conversation_history.append(("bot", response))
        return response

    def add_to_knowledge_base(self, user_input):
        """Allows the user to add new information to the knowledge base."""
        try:
            # Extract question and answer from user input
            parts = user_input.split('::')
            if len(parts) != 2:
                return "To add to my knowledge base, use the format: 'learn question::answer'"
            
            question = parts[0].strip()
            answer = parts[1].strip()
            
            return self.learn_from_answer(question, answer)
        except Exception as e:
            return f"Sorry, I couldn't add that to my knowledge base. Error: {str(e)}"


def main():
    """Main function to run the chatbot."""
    print("Initializing chatbot. This may take a moment...")
    chatbot = AIChatbot()
    print("\nChatbot: Hi! I'm an AI chatbot that can answer questions, chat, solve math, and more!")
    print("Chatbot: You can ask me general knowledge questions, or try specialized commands.")
    print("Chatbot: To teach me new facts, type: 'learn What is X::X is Y'")
    print("Chatbot: Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "ok bye", "goodbye"]:
            print("Chatbot:", random.choice(chatbot.responses["bye"]))
            break
        
        if user_input.lower().startswith("learn ") and "::" in user_input:
            response = chatbot.add_to_knowledge_base(user_input[6:])
        else:
            response = chatbot.process_input(user_input)
            
        print("Chatbot:", response)


if __name__ == "__main__":
    main()
