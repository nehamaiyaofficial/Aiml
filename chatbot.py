#!/usr/bin/env python3
import random
import sympy as sp

responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm good, thanks!", "Doing great!", "I'm just a bot, but I'm fine!"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "what can you do": [
        "I can chat with you, answer questions, and even solve math problems!",
        "I can help with coding, jokes, general knowledge, and math calculations!"
    ],
    "tell me a joke": [
        "Why don’t programmers like nature? Because it has too many bugs!",
        "Why did the AI break up with the chatbot? It just wasn’t processing feelings correctly!",
        "I told my computer a joke, but it didn’t laugh. Guess it’s not on my level!"
    ],
    "do you like ai": ["Of course! AI is amazing!", "I am AI, so yes, I love it!"],
    "what is machine learning": [
        "Machine learning is a type of AI that allows computers to learn from data.",
        "It's a field of AI where models improve by learning from experience!",
        "ML is used in self-driving cars, recommendation systems, and chatbots like me!"
    ],
    "who created you": ["I was created by a cool developer!", "A programmer built me using Python."],
    "what is your name": ["I'm ChatBot!", "You can call me ChatBot.", "Just a friendly AI assistant."],
    "do you like me": ["Yes my love <3", "Yes sweetheart", "Yes my Angel"],
    "what are you doing": ["I don't know", "Talking to you, I guess", "I'm thinking about the universe"],
    "who are you": ["Your love", "Your bestie", "Your caretaker, I guess"],
    "default": ["Sorry, I don't understand.", "Can you rephrase that?", "I'm not sure about that."]
}

def solve_math(expression):
    try:
        # Use sympy to safely evaluate mathematical expressions
        result = sp.sympify(expression)
        return f"The answer is: {result}"
    except Exception:
        return "Sorry, I couldn't solve that. Make sure it's a valid math expression."

def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Check if input contains mathematical operators or functions
    if any(op in user_input for op in ["+", "-", "*", "/", "^", "(", ")", "sin", "cos", "tan"]):
        return solve_math(user_input)
    
    return random.choice(responses.get(user_input, responses["default"]))

if __name__ == "__main__":
    print("Chatbot: Hi! I can chat and solve math problems! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot:", random.choice(responses["bye"]))
            break
        print("Chatbot:", chatbot_response(user_input))

