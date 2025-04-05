#!/usr/bin/env python3
import random
import re
import sympy as sp
import datetime
import json
import time
import threading
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

# Global NLP availability flag
NLP_AVAILABLE = False

class AIChatbot:
    def __init__(self):
        global NLP_AVAILABLE
        
        # Initialize conversation memory
        self.conversation_history: List[Tuple[str, str]] = []
        self.user_preferences: Dict[str, str] = defaultdict(str)
        self.learning_dictionary: Dict[str, str] = {}
        self.user_name: str = ""
        self.last_topic: str = ""
        self.chat_start_time: float = time.time()
        self.is_typing: bool = False
        
        # Personality traits
        self.personality = {
            "name": "Assistant",
            "tone": "friendly and helpful",
            "verbosity": "detailed",
            "formality": "balanced"
        }
        
        # Initialize NLP
        self._initialize_nlp()
        
        # Knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Command patterns
        self.commands = {
            r'(what|tell me).*time': self._get_time,
            r'(what|tell me).*date': self._get_date,
            r'remember (that )?my (\w+) is (.+)': self._remember_preference,
            r'my (\w+) is (.+)': self._remember_preference,
            r'what( is|\'s) my (\w+)': self._recall_preference,
            r'learn that (.*?) -> (.*)': self._learn_response,
            r'tell me a joke': self._tell_joke,
            r'(flip|toss) a coin': self._flip_coin,
            r'roll a dice': self._roll_dice,
            r'roll a (\d+)-sided dice': self._roll_n_sided_dice,
            r'weather in (.+)': self._get_weather,
            r'define (.+)': self._get_definition,
            r'what( is|\'s) your name': self._get_name,
            r'who are you': self._get_name,
            r'how long have we been talking': self._get_chat_duration,
            r'(my name is|call me) (.+)': self._set_user_name,
            r'(exit|quit|bye|goodbye)': self._exit_chat,
            r'calculate (.+)': self._calculate_expression,
            r'what is (.+) (plus|\+|minus|\-|times|\*|divided by|/) (.+)': self._calculate_simple,
            r'solve (.+)': self._solve_equation
        }

        # Conversation prompts
        self.conversation_prompts = {
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! What would you like to talk about?",
                "Greetings! I'm ready to help with anything you need."
            ],
            "farewell": [
                "Goodbye! Feel free to come back if you have more questions.",
                "It was nice chatting with you! Have a great day.",
                "Until next time! Don't hesitate to reach out if you need anything."
            ],
            "acknowledgment": [
                "I see. ",
                "Interesting. ",
                "I understand. ",
                "That makes sense. "
            ],
            "clarification": [
                "Could you explain that in more detail?",
                "Can you elaborate on that point?",
                "I want to make sure I understand. Could you rephrase that?",
                "What specifically would you like to know about this?"
            ]
        }

    def _initialize_nlp(self):
        """Initialize NLP components if available"""
        global NLP_AVAILABLE
        try:
            import nltk
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from nltk.stem import WordNetLemmatizer
            
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            NLP_AVAILABLE = True
        except ImportError:
            NLP_AVAILABLE = False

    def _load_knowledge_base(self) -> List[Dict[str, str]]:
        """Load knowledge base from file or create default"""
        try:
            with open('knowledge_base.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            default_kb = [
                {"question": "What is AI?", "answer": "AI refers to systems that mimic human intelligence."},
                {"question": "Who invented the light bulb?", "answer": "Thomas Edison invented the practical light bulb."},
                {"question": "What is the capital of France?", "answer": "The capital of France is Paris."}
            ]
            try:
                with open('knowledge_base.json', 'w') as file:
                    json.dump(default_kb, file, indent=4)
            except Exception:
                pass
            return default_kb

    def _get_time(self, *args) -> str:
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."

    def _get_date(self, *args) -> str:
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}."

    def _remember_preference(self, *args) -> str:
        """Store user preference"""
        if len(args) == 2:  # For pattern without "that"
            key, value = args[1], args[2]
        else:  # For pattern with "that"
            key, value = args[2], args[3]
        self.user_preferences[key] = value
        return f"I'll remember your {key} is {value}."

    def _recall_preference(self, *args) -> str:
        """Recall user preference"""
        key = args[2] if len(args) > 2 else args[1]
        if key in self.user_preferences:
            return f"Your {key} is {self.user_preferences[key]}."
        return f"I don't know your {key} yet."

    def _learn_response(self, *args) -> str:
        """Learn a new response pattern"""
        trigger, response = args[1], args[2]
        self.learning_dictionary[trigger.strip()] = response.strip()
        return f"I've learned to respond to '{trigger}' with '{response}'."

    def _tell_joke(self, *args) -> str:
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "Why don't skeletons fight each other? They don't have the guts."
        ]
        return random.choice(jokes)

    def _flip_coin(self, *args) -> str:
        """Flip a coin"""
        return f"It's {random.choice(['heads', 'tails'])}!"

    def _roll_dice(self, *args) -> str:
        """Roll a 6-sided die"""
        return f"You rolled a {random.randint(1, 6)}!"

    def _roll_n_sided_dice(self, *args) -> str:
        """Roll an n-sided die"""
        try:
            sides = int(args[1])
            return f"You rolled a {random.randint(1, sides)} on a {sides}-sided die!"
        except ValueError:
            return "Please specify a valid number of sides."

    def _get_weather(self, *args) -> str:
        """Get weather for location (simulated)"""
        location = args[1]
        conditions = ["sunny", "cloudy", "rainy", "snowy"]
        temp = f"{random.randint(50, 90)}°F"
        return f"In {location}, it's currently {random.choice(conditions)} and {temp}."

    def _get_definition(self, *args) -> str:
        """Get definition of word (simulated)"""
        word = args[1]
        definitions = {
            "computer": "an electronic device for storing and processing data",
            "book": "a written or printed work consisting of pages bound together",
            "science": "the systematic study of the structure and behavior of the physical world"
        }
        if word.lower() in definitions:
            return f"{word.capitalize()}: {definitions[word.lower()]}"
        return f"I don't have a definition for '{word}' in my dictionary."

    def _get_name(self, *args) -> str:
        """Return assistant name"""
        return f"I'm {self.personality['name']}, your AI assistant."

    def _get_chat_duration(self, *args) -> str:
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

    def _set_user_name(self, *args) -> str:
        """Set user's name"""
        self.user_name = args[2].strip() if len(args) > 2 else args[1].strip()
        return f"Nice to meet you, {self.user_name}! I'll remember your name."

    def _exit_chat(self, *args) -> None:
        """Handle chat exit"""
        response = f"Goodbye{f', {self.user_name}' if self.user_name else ''}! It was nice chatting with you."
        print(f"Assistant: {response}")
        exit(0)

    def _calculate_expression(self, *args) -> str:
        """Calculate mathematical expressions"""
        expression = args[1]
        try:
            # Clean the expression
            expr = expression.replace('^', '**').replace('×', '*').replace('÷', '/')
            expr = re.sub(r'[^0-9+\-*/(). ]', '', expr)
            
            # Evaluate safely
            result = eval(expr, {'__builtins__': None}, {})
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Sorry, I couldn't calculate that: {str(e)}"

    def _calculate_simple(self, *args) -> str:
        """Calculate simple operations"""
        try:
            num1 = float(args[1])
            num2 = float(args[3])
            op = args[2]
            
            if op in ['plus', '+']:
                result = num1 + num2
                return f"{num1} plus {num2} equals {result}"
            elif op in ['minus', '-']:
                result = num1 - num2
                return f"{num1} minus {num2} equals {result}"
            elif op in ['times', '*']:
                result = num1 * num2
                return f"{num1} times {num2} equals {result}"
            elif op in ['divided by', '/']:
                result = num1 / num2
                return f"{num1} divided by {num2} equals {result}"
        except Exception as e:
            return f"Sorry, I couldn't calculate that: {str(e)}"

    def _solve_equation(self, *args) -> str:
        """Solve mathematical equations"""
        equation = args[1]
        try:
            x = sp.symbols('x')
            solution = sp.solve(equation, x)
            return f"The solution to {equation} is x = {solution}"
        except Exception as e:
            return f"Sorry, I couldn't solve that equation: {str(e)}"

    def _process_conversation(self, user_input: str) -> str:
        """Handle conversational responses"""
        # Analyze input for conversation context
        context = self._analyze_context(user_input)
        
        # Generate appropriate response
        if context['is_question']:
            answer = self._answer_question(user_input)
            if answer:
                return answer
        
        if context['emotion']:
            return self._respond_to_emotion(context['emotion'])
        
        if context['topic']:
            return self._respond_to_topic(context['topic'])
        
        return random.choice([
            "That's interesting. Tell me more about that.",
            "I'd love to hear more about your thoughts on this.",
            "What else would you like to discuss?",
            "That's a fascinating point. Could you elaborate?"
        ])

    def _analyze_context(self, text: str) -> Dict:
        """Analyze conversation context"""
        text_lower = text.lower()
        return {
            'is_question': self._is_question(text),
            'emotion': self._detect_emotion(text_lower),
            'topic': self._detect_topic(text_lower)
        }

    def _is_question(self, text: str) -> bool:
        """Check if text is a question"""
        return text.endswith('?') or any(
            text.lower().startswith(q_word) 
            for q_word in ['what', 'who', 'where', 'when', 'why', 'how', 'is', 'are']
        )

    def _detect_emotion(self, text: str) -> Optional[str]:
        """Detect emotional tone"""
        positive = ['happy', 'joy', 'excited', 'great']
        negative = ['sad', 'angry', 'frustrated', 'upset']
        
        if any(word in text for word in positive):
            return 'positive'
        elif any(word in text for word in negative):
            return 'negative'
        return None

    def _detect_topic(self, text: str) -> Optional[str]:
        """Detect conversation topic"""
        topics = {
            'technology': ['computer', 'tech', 'program', 'code'],
            'sports': ['sport', 'game', 'play', 'team'],
            'weather': ['weather', 'rain', 'sunny', 'temperature']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                return topic
        return None

    def _respond_to_emotion(self, emotion: str) -> str:
        """Generate emotion-appropriate response"""
        if emotion == 'positive':
            return random.choice([
                "That sounds wonderful! Tell me more about what makes you feel this way.",
                "I'm so happy to hear that! What's bringing you joy?",
                "That's fantastic! I'd love to hear more about your excitement."
            ])
        else:
            return random.choice([
                "I'm sorry to hear that. Would you like to talk about what's bothering you?",
                "That sounds difficult. I'm here to listen if you want to share more.",
                "I understand this might be tough. Would discussing it help?"
            ])

    def _respond_to_topic(self, topic: str) -> str:
        """Generate topic-appropriate response"""
        responses = {
            'technology': [
                "Technology is fascinating. What specific aspect interests you?",
                "I enjoy discussing technology. What would you like to know?",
                "Tech is always evolving. What recent developments caught your attention?"
            ],
            'sports': [
                "Sports can be so exciting! Which one is your favorite?",
                "I enjoy sports discussions. What game are you following?",
                "Sports bring people together. What team do you support?"
            ],
            'weather': [
                "The weather affects us all. How's it where you are?",
                "Weather is always changing. What's your favorite season?",
                "I can discuss weather patterns. What specifically interests you?"
            ]
        }
        return random.choice(responses.get(topic, ["That's an interesting topic. Tell me more."]))

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
        
        # Default to conversation handling
        return self._process_conversation(user_input)

    def _show_typing_indicator(self):
        """Show typing indicator animation"""
        while self.is_typing:
            for frame in ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']:
                if not self.is_typing:
                    break
                print(f"\rAssistant: {frame} Thinking...", end='', flush=True)
                time.sleep(0.1)

    def chat_loop(self):
        """Main chat loop"""
        print(random.choice(self.conversation_prompts["greeting"]))
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                    
                # Show typing indicator
                self.is_typing = True
                threading.Thread(target=self._show_typing_indicator).start()
                
                # Process input
                response = self._process_input(user_input)
                
                # Stop typing indicator
                self.is_typing = False
                print(f"\rAssistant: {response}")
                
            except KeyboardInterrupt:
                self._exit_chat()
            except Exception as e:
                print(f"\rAssistant: Sorry, I encountered an error. Could you try again?")
                print(f"(Debug: {str(e)})")

if __name__ == "__main__":
    bot = AIChatbot()
    bot.chat_loop()
