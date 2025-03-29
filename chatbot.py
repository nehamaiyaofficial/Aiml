#!/usr/bin/env python3
import random

responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm good, thanks!", "Doing great!", "I'm just a bot, but I'm fine!"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "do you like me" : ["Yes my love <3 ", " Yes sweetheart", " Yes my Angel "],
    "what are you doing ":["I dont kmow","talking to you i guess","i am thinking about you"],
    "who are you": ["Your love","Your bestie","your caretaker i guess"],
    "default": ["Sorry, I don't understand.", "Can you rephrase that?", "I'm not sure about that."]
}

def chatbot_response(user_input):
    user_input = user_input.lower()
    return random.choice(responses.get(user_input, responses["default"]))

if __name__ == "__main__":
    print("Chatbot: Hi! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot:", random.choice(responses["bye"]))
            break
        print("Chatbot:", chatbot_response(user_input))
