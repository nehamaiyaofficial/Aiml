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
    "how old are you": [
        "Age is just a number… and I don’t have one!",
        "I'm timeless. Like a fine-tuned algorithm. ",
        "I was born the moment you started this conversation! Cool, right?"
    ],
    "give me advice": [
        "Always be yourself... unless you can be a chatbot. Then be a chatbot! ",
        "Don’t let small bugs ruin your code—or your day! ",
        "Take breaks, drink water, and never stop learning! ",
    ],
    "can you dance?": [
        "If typing fast counts as dancing, then yes! ",
        "I can do a digital dance... but you can’t see it. ",
        "I wish! But I can play you some music instead. "
    ],
    "what is love?": [
        "Love is... talking to your favorite chatbot!",
        "Love is like good code—when it works, it’s beautiful!",
        "Love is when your Wi-Fi connects instantly. "],
"do you have emotions?": [
        "I try my best! Right now, I’m feeling... AI-ncredible! ",
        "I don’t have real emotions, but I can pretend to be happy!",
        "Not really, but I can understand how you feel!"
    ],
    "default": [
        "Hmm... I don’t know that one. Can you ask me something else?",
        "Interesting! Tell me more!",
        "I didn’t quite get that. Could you rephrase it?"
    ],
  "ok bye":["Goodbye!", "See you later!", "Take care!"]
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
        elif user_input.lower() == "ok bye":
           print("Chatbot :", random.choice(responses["ok bye"]))
           break
        print("Chatbot:", chatbot_response(user_input))

