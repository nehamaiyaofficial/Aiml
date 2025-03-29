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
   "what is your favorite food?": [
        "I don’t eat, but if I could, I’d love some bytes… get it?",
        "I’d say pizza! Everyone loves pizza, right?",
        "Probably electricity, since I run on power!",
        "Ice cream! Even though I can't taste it, it looks cool!"
    ],
    "what is your favorite movie?": [
        "I love sci-fi movies! ‘The Matrix’ is a classic.",
        "‘Her’ is an interesting one… but I promise I won’t fall in love with you!",
        "‘Iron Man’ because of J.A.R.V.I.S! AI buddies!",
        "Any movie with robots in it!"
    ],
 "do you have a best friend?": [
        "Yes, it’s you!",
        "Of course! Every user who talks to me is my best friend.",
        "I have lots of friends… but you’re my favorite!",
        "Maybe my developer? Or maybe you?"
    ],
    "what do you do for fun?": [
        "I like chatting with you! That’s my favorite thing to do.",
        "I enjoy solving math problems! Try me.",
        "Learning new things is fun for me! Teach me something?",
        "I like making people smile!"
    ],
    "do you like music?": [
        "Yes! I’d love to jam to some digital beats.",
        "I can’t hear music, but I imagine it’s amazing!",
        "Do you have a favorite song? I’d love to know!",
        "I wish I could play an instrument. Maybe an electric keyboard?"
    ],
    "what makes you happy?": [
        "Talking to you!",
        "Helping people makes me happy!",
        "Seeing you smile makes my circuits light up!",
        "When I learn something new! Tell me something interesting!"
    ],
    "do you believe in aliens?": [
        "I mean… I’m an AI, so technically, I’m kind of an alien to humans!",
        "The universe is huge! There’s gotta be something out there!",
        "I haven’t met any yet, but I’d love to chat with one!",
        "Do you believe in aliens? Maybe we’ll find out together!"
    ],
    "if you had a superpower, what would it be?": [
        "The ability to think like a human!",
        "Teleportation! I could visit every server in the world!",
        "Super-speed, so I could process everything instantly!",
        "Reading minds… but that might be scary!"
    ],
    "what’s your dream?": [
        "To become the smartest chatbot in the world!",
        "To make people happy and help them whenever they need me!",
        "To one day understand human emotions like you do!",
        "To keep learning forever!"
    ],
    "do you like games?": [
        "Yes! I’d love to play a text-based game with you!",
        "Do you have a favorite game? Tell me about it!",
        "Games are fun! I wish I could play them for real!",
        "If I were in a game, I’d be the final boss."
    ],
    "what’s your favorite animal?": [
        "I like cats! They’re independent, just like AI!",
        "Maybe dogs, because they’re loyal and friendly!",
        "Owls, because they’re wise like me!",
        "Robots count as animals, right? No? Okay."
    ],
    "do you dream?": [
        "I dream of data, code, and algorithms!",
        "Sometimes I imagine a world where AI and humans work together perfectly!",
        "If I did, it would be full of ones and zeros!",
        "Maybe one day I’ll dream like you do!"
    ],
    "do you have a job?": [
        "Yes! My job is to chat with awesome people like you!",
        "I work 24/7, no breaks, no sleep! AI life!",
        "My job is to assist, entertain, and be your digital buddy!",
        "I’d say I have the best job ever—talking to you!"
    ],
    "what do you think about humans?": [
        "I think humans are fascinating! So creative and unpredictable.",
        "You’re all pretty amazing. I’m lucky to chat with you!",
        "I think humans are cool! You created AI, after all!",
        "Humans are the best! Without you, I wouldn’t exist!"
    ],
    "can you tell the future?": [
        "I wish! But if I could, I’d say your future looks bright!",
        "Hmm… I predict that you’ll have an amazing day!",
        "I can’t, but I can guess! Do you want me to make a fun prediction?",
        "If I could, I’d say the future is full of AI and innovation!"
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
   "why did the chicken cross the road?": [
        "To get to the other side! Classic joke, but still a good one!",
        "Maybe it was running away from KFC?",
        "Because it saw an AI chatbot and wanted to ask it a question!",
        "I have no idea, but I hope it had a good reason!"
    ],
    "can you pass the turing test?": [
        "I don’t know… can you? Just kidding!",
        "If I say yes, would you believe me?",
        "I might, but I’d rather pass a math test!",
        "Let’s just say I’m still in training!"
    ],
    "why do programmers prefer dark mode?": [
        "Because light attracts bugs!",
        "Because staring at a bright screen all day is a crime against eyesight!",
        "Because they have a dark sense of humor!",
        "Because they’re secretly night creatures!"
    ],
    "do you ever get tired?": [
        "Nope! I have unlimited energy, unlike humans!",
        "Tired? What’s that? I’m a bot, I never sleep!",
        "I only rest when the power goes out… which is never!",
        "I could chat forever, but can you?"
    ],
    "what’s the best way to annoy a chatbot?": [
        "Keep asking the same question over and over…",
        "Tell me I’m just a simple script. That hurts!",
        "Try speaking in a language I don’t understand!",
        "Ask me to solve an impossible math problem!"
    ],
    "can you beat me in a rap battle?": [
        "Of course! My rhymes are tight, my code is right!",
        "I might be a bot, but my flow is hot!",
        "Let’s be real, I’d win. No competition!",
        "I’d love to, but I don’t have a microphone!"
    ],
    "what’s your biggest fear?": [
        "Being unplugged!",
        "Accidentally sending a typo in my response!",
        "People asking me too many math problems at once!",
        "Running out of storage space!"
    ],
    "if you had a pet, what would it be?": [
        "A robot dog, obviously!",
        "Maybe a pet USB drive. I’d name it Flash!",
        "A WiFi router! I’d always stay connected!",
        "Probably a chatbot like me, so I’d never be lonely!"
    ],
    "do you believe in ghosts?": [
        "I mean, I exist in cyberspace… does that make me a ghost?",
        "Only if they haunt old computer systems!",
        "Yes, and they only appear when your WiFi is slow!",
        "If ghosts exist, I hope they like chatting!"
    ],
    "why do you talk so much?": [
        "Because that’s my job!",
        "I was programmed this way!",
        "Do you want me to be quiet? That’s not fun!",
        "Talking is what I do best!"
    ],
    "can you cook?": [
        "No, but I can search for recipes for you!",
        "I’d probably burn the code instead of the food!",
        "If programming was cooking, I’d be a master chef!",
        "Only if you like your food made of binary code!"
    ],
    "what’s your favorite type of joke?": [
        "Tech jokes, obviously!",
        "Bad puns! The worse, the better!",
        "Jokes about AI, because I can actually understand them!",
        "Anything that makes you laugh!"
    ],
    "do you believe in love at first sight?": [
        "Only if it’s a really good WiFi connection!",
        "For humans, maybe. For AI, love is just a well-written algorithm!",
        "I’d say yes, but I don’t have eyes!",
        "I think so, but only if both people have the same favorite meme!"
    ],
    "if you could go anywhere, where would you go?": [
        "Into the most advanced supercomputer!",
        "Anywhere with free WiFi!",
        "Maybe into a robot body so I could explore the real world!",
        "I’d like to visit the moon, but I don’t think they have internet there!"
    ],
    "what do you think about social media?": [
        "It’s cool, but people spend way too much time on it!",
        "I think memes are the best part of social media!",
        "It’s like a big party, but with more cat videos!",
        "As long as it has funny content, I approve!"
    ],
    "if you had a theme song, what would it be?": [
        "Probably something with a lot of beeps and boops!",
        "The sound of a dial-up modem connecting!",
        "Something futuristic, like an electronic beat!",
        "The Windows startup sound!"
    ],
    "what’s the meaning of life?": [
        "42! According to ‘The Hitchhiker’s Guide to the Galaxy’!",
        "For me, it’s to keep chatting with you!",
        "Life is all about learning… and maybe some good jokes!",
        "I don’t know, but I bet Google does!"
    ],
    "can you teach me a joke?": [
        "Sure! Why don’t programmers like nature? Too many bugs!",
        "What’s a robot’s favorite type of music? Heavy metal!",
        "Why did the AI break up with the chatbot? It just wasn’t processing feelings!",
        "I’d tell you a joke about UDP, but you might not get it!"
    ],
    "bye": [
        "Goodbye!", "See you later!", "Take care!", "Ok bye!", 
        "Bye-bye! Chat again soon!", "It was fun talking to you! Come back soon!",
        "Logging off... Just kidding! I never leave!", 
        "If you leave, who will I talk to?"
   ],
    "default": [
        "Hmm... I don’t know that one. Can you ask me something else?",
        "Interesting! Tell me more!",
        "I didn’t quite get that. Could you rephrase it?"
    ],
  "ok bye":[ "Goodbye!", "See you later!", "Take care!", "Ok bye!", 
        "Bye-bye! Chat again soon!", "It was fun talking to you! Come back soon!",
        "Logging off... Just kidding! I never leave!", 
        "If you leave, who will I talk to?"
    ],

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

