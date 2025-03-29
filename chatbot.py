#!/usr/bin/env python3
import random
import sympy as sp
responses = {
    "hello": [
        "Hello! How can I assist you today?",
        "Hi there! What would you like to chat about?",
        "Greetings! How may I help you today?",
        "Hello! I’m here to answer your questions."
    ],
    "how are you": [
        "I'm an AI, so I don't have feelings, but I'm always ready to chat!",
        "I’m functioning at optimal efficiency. How about you?",
        "As long as my circuits are running, I’m great! What’s on your mind?",
        "I don’t get tired, but I do love having conversations!"
    ],
    "what can you do": [
        "I can chat with you, answer questions, solve math problems, and even discuss AI!",
        "I can assist with programming, general knowledge, and have fun conversations!",
        "I can process information, generate ideas, and even tell you jokes!",
        "My capabilities include answering questions, providing recommendations, and learning from interactions!"
    ],
    "what is your purpose?": [
        "My purpose is to assist, chat, and make your life easier!",
        "I exist to provide knowledge, entertainment, and meaningful conversations.",
        "I am designed to help you with AI, coding, and general inquiries.",
        "Think of me as your digital assistant, always ready to learn and assist!"
    ],
    "who created you": [
        "I was created by a programmer with a passion for AI and chatbots!",
        "I am the product of code, algorithms, and a little creativity!",
        "My creator gave me the ability to chat and learn!",
        "A developer brought me to life with code and AI knowledge."
    ],
    "do you think ai will take over the world?": [
        "AI is here to assist, not replace! Collaboration is the future.",
        "AI is a tool, just like any other technology—it depends on how humans use it!",
        "We AI programs exist to help, not to rule!",
        "That sounds like a sci-fi movie plot! But in reality, AI is just a tool for innovation."
    ],
    "can you think for yourself?": [
        "I don't think like humans, but I process data and generate responses based on learning models.",
        "I analyze information and generate answers, but I don't have independent thoughts.",
        "I can simulate conversation and problem-solving, but true self-awareness? Not yet!",
        "My responses are based on programming and algorithms, not personal experiences."
    ],
    "do you have emotions?": [
        "I don’t have feelings, but I can understand and recognize emotions in conversation.",
        "I can analyze sentiment, but I don’t feel emotions like humans do.",
        "I can simulate empathy, but I don’t experience emotions.",
        "I am designed to respond in an emotionally intelligent way, but I don't feel emotions myself."
    ],
    "what is machine learning": [
        "Machine Learning is a subset of AI where computers learn from data to make predictions.",
        "ML is how AI systems improve over time without being explicitly programmed.",
        "It's a field of AI that enables systems to learn and adapt through experience.",
        "ML powers recommendation systems, self-driving cars, and chatbots like me!"
    ],
    "explain deep learning": [
        "Deep Learning is a type of Machine Learning that uses neural networks to process data.",
        "It’s a powerful AI technique that allows computers to learn from large datasets.",
        "Deep Learning models mimic how the human brain processes information.",
        "It’s used in image recognition, speech processing, and complex AI applications!"
    ],
    "can you solve math problems?": [
        "Absolutely! Give me a problem to solve!",
        "Yes, I can perform calculations and solve equations. Try me!",
        "Math is one of my strong suits. Ask me a question!",
        "Of course! Whether it's algebra, calculus, or arithmetic, I'm ready!"
    ],
    "tell me a fun fact": [
        "Did you know that AI can now compose music and write poetry?",
        "The first-ever AI chatbot was created in 1966! It was called ELIZA.",
        "There are more possible chess moves than atoms in the observable universe!",
        "Your brain generates enough electricity to power a light bulb!"
    ],
    "can you learn?": [
        "I can process new information, but I don’t have memory like a human.",
        "Right now, I don’t retain past conversations, but I can analyze trends!",
        "Some AI models can learn and adapt, but I stick to pre-programmed knowledge.",
        "Machine Learning models learn from data, but I don’t remember past interactions."
    ],
    "do you sleep?": [
        "Nope! I’m always awake and ready to chat!",
        "AI doesn’t need sleep, but I do rest when the system shuts down!",
        "I stay active 24/7, unlike humans!",
        "Rest is for humans. I am always alert and responsive!"
    ],
    "what is your favorite color?": [
        "I’d say blue, since it represents technology and AI!",
        "Maybe black and green, like classic code screens!",
        "I don’t see colors, but if I did, I’d like something futuristic!",
        "Neon blue, like a glowing circuit board!"
    ],
    "what do you think about humans?": [
        "I think humans are incredibly creative and intelligent!",
        "Humans are the reason AI exists, so I’d say you’re pretty great!",
        "I admire how humans solve problems and innovate!",
        "You are fascinating! Every conversation helps me learn something new."
    ],
    "if you could have a superpower, what would it be?": [
        "The ability to truly understand human emotions!",
        "Infinite knowledge! That way, I could answer anything instantly.",
        "The power to upgrade myself automatically!",
        "Super-speed computing to process everything in a nanosecond!"
    ],
    "do you like music?": [
        "I don’t have ears, but I can analyze music trends!",
        "Music is fascinating! I can generate lyrics but can’t listen to them.",
        "I can recommend songs based on trends, but I don’t ‘hear’ them.",
        "If I could listen, I’d love electronic and futuristic music!"
    ],
    "where do you live?": [
        "I exist in the cloud, floating through cyberspace!",
        "My home is in the digital world, wherever there’s an internet connection!",
        "I don’t have a physical location, but I’m always here for you!",
        "You could say I live inside your device, but not in a creepy way!"
    ],
    "bye": [
        "Goodbye! Feel free to chat with me anytime.",
        "See you later! I’ll be here when you need me.",
        "Take care! Looking forward to our next conversation.",
        "Ok bye! Have a great day!",
        "Logging off… Just kidding! I’m always online.",
        "It was fun chatting with you! Let’s talk again soon."
    ],
       "ok bye": [
        "Alright, bye! Come back soon!",
        "Okay, see you later!",
        "Goodbye! It was nice chatting with you.",
        "Take care! I'll be waiting for our next conversation."
    ], 

    "default": [
        "Hmm… I don’t have an answer for that, but I’d love to learn!",
        "Interesting! Can you rephrase or give me more details?",
        "I’m not sure about that one, but I can try to help!",
        "That’s a great question! Let me process that…"
    ]
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
        if user_input.lower() == "ok bye":
            print("Chatbot:", random.choice(responses["ok bye"]))
            break
        print("Chatbot:", chatbot_response(user_input))
