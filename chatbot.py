#!/usr/bin/env python3
import random
import re
import sympy as sp
import datetime
import requests
import json
import numpy as np
from collections import defaultdict

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
                "I can chat, answer multiple questions at once, tell jokes, solve math problems, remember details about you, learn new responses, and more!",
                "Besides chatting, I can solve equations, answer general knowledge questions, handle multiple questions in one go, learn new things, and even attempt humor.",
                "Think of me as your AI assistant—I can understand and answer multiple questions at once, remember details from our chat, solve math problems, and more."
            ],
            "bye": [
                "Goodbye! Had fun chatting with you. Come back soon.",
                "See you later. Stay awesome.",
                "Take care! I'll be here when you need me.",
                "Logging off… Just kidding. I'm always online."
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
            'remainder': text  # Default to the full text
        }
        
        # Extract math expressions
        math_expressions = self.extract_math_expressions(text)
        if math_expressions:
            result['math_expressions'] = math_expressions
        
        # Check for common greetings
        greeting_patterns = [
            r'\bhello\b', r'\bhi\b', r'\bhey\b', r'\bgreetings\b', 
            r'\bgood morning\b', r'\bgood afternoon\b', r'\bgood evening\b'
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
        """Searches the web for an answer to the question using a public API."""
        try:
            # This is a placeholder for a real API call
            # In a real implementation, you'd use a service like Wikipedia API, DuckDuckGo API, etc.
            return f"Based on my knowledge, I would search for information about '{query}'. In a full implementation, this would connect to a web search service."
        except Exception as e:
            return f"I tried to search online, but encountered an error: {str(e)}"
    
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
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Why did the coffee file a police report? It got mugged.",
            "What did the ocean say to the beach? Nothing, it just waved."
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
            return f"I would show you the weather in {location}, but I need an API key to access real weather data. In a full implementation, this would connect to a weather service."
        except Exception as e:
            return f"Sorry, I couldn't get the weather for {location}. Error: {str(e)}"
    
    def get_definition(self, word):
        """Gets the definition of a word."""
        try:
            return f"I would show you the definition of '{word}', but I need an API key to access dictionary data. In a full implementation, this would connect to a dictionary service."
        except Exception as e:
            return f"Sorry, I couldn't find the definition for {word}. Error: {str(e)}"
    
    def check_for_math(self, user_input):
        """Checks if the input contains a math problem."""
        math_operators = ['+', '-', '*', '/', '^', '(', ')', 'sin', 'cos', 'tan', 'sqrt', 'log']
        
        # Check for operators
        has_operators = any(op in user_input for op in math_operators)
        
        # Check for solve/calculate keywords with numbers
        has_math_keywords = re.search(r'(solve|calculate|compute|what is)\s+[0-9]', user_input, re.IGNORECASE)
        
        return has_operators or bool(has_math_keywords)
    
    def process_input(self, user_input):
        """Enhanced method to process mixed user input with greetings, questions, and math."""
        # Add to conversation history
        self.conversation_history.append(("user", user_input))
        
        # Clean input
        cleaned_input = user_input.strip()
        
        # Parse the mixed input
        parsed_input = self.parse_mixed_input(cleaned_input)
        
        # Initialize response parts
        response_parts = []
        
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
        
        # Process math expressions
        if parsed_input['math_expressions']:
            for expr in parsed_input['math_expressions']:
                math_result = self.solve_math(expr)
                response_parts.append(math_result)
        
        # Process questions
        if parsed_input['questions']:
            for q in parsed_input['questions']:
                if "how are you" in q.lower():
                    response_parts.append(random.choice(self.responses["how are you"]))
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
            
            # If still nothing, use the default response
            if not response_parts:
                response_parts.append(random.choice(self.responses["default"]))
        
        # Combine all response parts
        combined_response = " ".join(response_parts)
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
        
        # If no match found, use default response
        return random.choice(self.responses["default"])
    
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
    print("\nChatbot: Hi! I'm an AI chatbot that can answer multiple questions at once!")
    print("Chatbot: You can ask me several questions in one message, and I'll answer each one.")
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
