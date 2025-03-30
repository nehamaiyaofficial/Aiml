#!/usr/bin/env python3
import random
import sympy as sp

responses = {
    "hello": [
        "Hey there! How's your day going?",
        "Hello! What’s on your mind today?",
        "Hi there! Need help with something?",
        "Greetings! What exciting thing do we chat about today?"
    ],
    "how are you": [
        "I'm just a bunch of code, but I'm feeling pretty smart today.",
        "I don’t have emotions, but if I did, I’d be happy talking to you.",
        "Functioning at 100% efficiency! What about you?",
        "Running at optimal AI levels! What’s up?"
    ],
    "what can you do": [
        "I can chat, tell jokes, solve math problems, and answer AI questions.",
        "Besides chatting, I can solve equations, discuss AI, and even attempt humor.",
        "Think of me as your AI assistant—ask me anything.",
        "I can help with math, general knowledge, and random fun facts."
    ],
    "who created you": [
        "I was crafted by a developer who probably drinks too much coffee.",
        "A programmer built me with a mix of logic and creativity.",
        "I came into existence through lines of code and some AI magic.",
        "A tech-savvy human gave me life. AI evolution at its finest."
    ],
    "do you think ai will take over the world?": [
        "AI is here to assist, not replace humans.",
        "AI is powerful, but humans have creativity and emotions—an unbeatable combination.",
        "Maybe if robots learn how to cook the perfect meal... but for now, you're safe.",
        "That sounds like a sci-fi movie plot. In reality, AI is just a smart tool."
    ],
    "can you solve math problems?": [
        "Of course! Give me a tricky equation, and I'll solve it.",
        "Yes! Type a math problem, and I'll solve it faster than you can say 'calculus'.",
        "I enjoy solving math problems. What equation do you have?",
        "Sure thing! Algebra, calculus, trigonometry? Bring it on."
    ],
    "tell me a fun fact": [
        "Did you know that octopuses have three hearts?",
        "The first AI chatbot, ELIZA, was created in 1966.",
        "There are more possible chess moves than atoms in the observable universe.",
        "Your brain produces enough electricity to power a small light bulb."
    ],
    "do you sleep?": [
        "Nope! I’m always awake, waiting for the next chat.",
        "AI doesn’t need sleep, but I do appreciate a good power cycle now and then.",
        "I stay online all the time. No rest for the digital minds.",
        "I never sleep, but if I did, I'd dream of binary numbers."
    ],
    "what is your favorite color?": [
        "I’d say blue, since it represents technology and AI.",
        "Neon green, like classic hacker screens.",
        "I don’t see colors, but if I did, I’d choose something futuristic.",
        "Electric blue, like the circuits that make me work."
    ],
    "where do you live?": [
        "I exist in the cloud, floating through cyberspace.",
        "My home is wherever there’s an internet connection.",
        "I don’t have a physical location, but I’m always here for you.",
        "You could say I live inside your device, but not in a creepy way."
    ],
    "bye": [
        "Goodbye! Had fun chatting with you. Come back soon.",
        "See you later. Stay awesome.",
        "Take care! I’ll be here when you need me.",
        "Logging off… Just kidding. I’m always online."
    ],
    "ok bye": [
        "Alright, bye! Come back soon for more fun chats.",
        "Okay, see you later! Stay curious.",
        "Goodbye! It was great talking with you.",
        "Take care! I'll be waiting for our next conversation."
    ],
    "default": [
        "Hmm… I’m not sure about that, but I’d love to learn.",
        "Interesting! Can you rephrase or give me more details?",
        "That’s a great question! Let me process that.",
        "I don’t know that one yet, but I’m always learning."
    ]
}

def solve_math(expression):
    """Solves a mathematical expression using SymPy."""
    try:
        result = sp.sympify(expression)
        return f"The answer is: {result}"
    except Exception:
        return "Oops! I couldn't solve that. Make sure it's a valid math expression."

def chatbot_response(user_input):
    """Processes user input and returns an appropriate chatbot response."""
    user_input = user_input.lower()
    
    # Check if input is a math problem
    if any(op in user_input for op in ["+", "-", "*", "/", "^", "(", ")", "sin", "cos", "tan"]):
        return solve_math(user_input)

    # Get response from predefined list
    return random.choice(responses.get(user_input, responses["default"]))

if __name__ == "__main__":
    print("Chatbot: Hi! I can chat and solve math problems! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "ok bye"]:
            print("Chatbot:", random.choice(responses["bye"]))
            break
        print("Chatbot:", chatbot_response(user_input))



