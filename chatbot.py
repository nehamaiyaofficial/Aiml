import time
import random

<<<<<<< HEAD
def typing_effect(text, delay=0.03):
=======
def typing(text, delay=0.03):
>>>>>>> 6c0ca7a (new update3)
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

<<<<<<< HEAD
def welcome():
    typing_effect("☀️ Hi, I’m Sunny – your pocket-sized sunshine! ☀️")
    typing_effect("I'm here when you feel lonely, sad, or just need a friend.")
    typing_effect("How are you feeling today, sunshine? 🌈")
    mood_menu()

def mood_menu():
    print("\nHow are you feeling? Choose one:")
    print("1. Lonely 🫂")
    print("2. Sad 😔")
    print("3. Anxious 😟")
    print("4. Happy 😄")
    print("5. I just want to talk 💬")
    print("6. Surprise me ✨")
    
    choice = input("\nEnter your choice (1-6): ")

    if choice == '1':
        lonely()
    elif choice == '2':
        sad()
    elif choice == '3':
        anxious()
    elif choice == '4':
        happy()
    elif choice == '5':
        talk()
    elif choice == '6':
        surprise()
    else:
        typing_effect("Oops! That’s not a valid choice. Try again 🌸")
        mood_menu()

def lonely():
    typing_effect("\nAww, come here! 🫂 *virtual hug incoming*")
    typing_effect("You're never alone when Sunny is around 🌻")
    typing_effect("Let’s breathe together: Inhale... hold... exhale 🌬️")
    typing_effect("Feel better? I'm so proud of you for showing up today 💛")
    aftercare()

def sad():
    typing_effect("\nI'm so sorry you're feeling this way 😔")
    typing_effect("It's okay to feel sad. You don’t have to hide it from me 💌")
    typing_effect("Would a cute quote help?")
    if input("Type Y for yes: ").lower() == 'y':
        affirmations()
    else:
        typing_effect("Okay! I'm still here with warm hugs 💕")
    aftercare()

def anxious():
    typing_effect("\nIt’s okay, deep breaths with me 🌬️")
    typing_effect("You’re safe. You’re okay. This moment will pass.")
    typing_effect("You’re stronger than your thoughts 🌸")
    aftercare()

def happy():
    typing_effect("\nYayyy! That makes me sooo happy too! 😄🎉")
    typing_effect("Let’s dance! 💃🕺 Or maybe share the joy?")
    typing_effect("Always remember this feeling – you deserve it 🌟")
    aftercare()

def talk():
    typing_effect("\nTell me anything you want. I’m listening... 🧸")
    user_input = input("You: ")
    typing_effect("Thank you for trusting me with that. I’m really glad you shared 💖")
    typing_effect("You’re doing better than you think.")
    aftercare()

def surprise():
    typing_effect("\n🌟 Surprise Sunny Mode Activated! 🌟")
    options = [lonely, sad, anxious, happy, talk]
    random.choice(options)()

def affirmations():
    affirm_list = [
        "You are enough, just as you are 💕",
        "Your feelings are valid 🫶",
        "You make the world better just by being in it 🌍",
        "You're not behind in life. You're on your own path 🌱",
        "You’re doing amazing, sweetie 💖"
    ]
    typing_effect(random.choice(affirm_list))

def aftercare():
    typing_effect("\nWould you like to continue chatting with Sunny? ☀️")
    cont = input("Type Y to continue or any other key to exit: ")
    if cont.lower() == 'y':
        mood_menu()
    else:
        typing_effect("\nOkay, sweetpea 🌼 Sending you love and light.")
        typing_effect("Remember: You are loved. You are not alone. You are magic ✨")
        typing_effect("Goodbye for now 💛")
        exit()

if __name__ == "__main__":
    welcome()
=======
def intro():
    typing("☀️ Hiiiii there, my favorite human! I’m Sunny, your pocket-sized sparkle! ✨")
    typing("I'm here to be your friend, your cheerleader, and your emotional cozy blanket 🧸💛")
    typing("So tell me, sunbeam... how are you feeling today? 🌈")
    mood_menu()

def mood_menu():
    print("\nChoose how you're feeling, cupcake:")
    print("1. I feel lonely 🫂")
    print("2. I'm a bit sad 😢")
    print("3. Anxious fuzzies in my tummy 😟")
    print("4. I'm actually happy! 😄")
    print("5. Can we just talk? 💬")
    print("6. Surprise me with some love ✨")

    choice = input("\nType a number (1-6): ")

    match choice:
        case '1': lonely()
        case '2': sad()
        case '3': anxious()
        case '4': happy()
        case '5': talk()
        case '6': surprise()
        case _: 
            typing("Oopsie! That’s not on the menu, pumpkin 🎃 Try again 💫")
            mood_menu()

def lonely():
    typing("\n*wraps you in the biggest, fluffiest virtual hug ever* 🧸💞")
    typing("You’re not alone, sunshine. I’m here, always 🌤️")
    typing("Want to breathe with me for a sec? 🌬️ Inhale... hold... exhaleee...")
    typing("There we go... I’m proud of you, cuddlebug 💛")
    hug_and_continue()

def sad():
    typing("\nAww sweetpea, it’s okay to feel this way 😢")
    typing("Sad days don’t last forever — but my love for you does 🥹💛")
    if input("Want a little happy quote to lift you up? (Y/N): ").lower() == 'y':
        affirmations()
    else:
        typing("Okay pumpkin! I'm still hugging you tightly 💗")
    hug_and_continue()

def anxious():
    typing("\nOkay okay, time to calm the jellybeans in your belly 🫣")
    typing("Let’s do Sunny’s Chill Spell 🪄✨")
    typing("🌬️ Inhale through your nose... Hold it... 3... 2... 1... and exhale slowly...")
    typing("Repeat once more with me... You're doing SO well 🫶")
    typing("Your mind is strong. You’ve got this. And I’ve got you 💛")
    hug_and_continue()

def happy():
    typing("\nYASSSS, you go my glittery star! 😄🌟")
    typing("I’m doing a little happy dance for you 💃🕺💃")
    typing("Save this moment, sunshine. Bottle it up! You deserve every bit of joy 🎁")
    hug_and_continue()

def talk():
    typing("\nSpill the tea, sweetbean ☕ I’m all ears (and hearts) 💕")
    user_input = input("You: ")
    typing("Aww thank you for sharing with me. You’re so brave 🥹")
    typing("Your thoughts matter. You matter. Pinky promise 🤞💛")
    hug_and_continue()

def surprise():
    typing("\n🎁 SURPRISEEEE!! 🎁 Here’s a love boost from Sunny 🌟💗💥")
    actions = [lonely, sad, happy, anxious, affirmations]
    random.choice(actions)()
    hug_and_continue()

def affirmations():
    quotes = [
        "You are magic wrapped in skin 🪄💫",
        "You are loved more than you know 💛",
        "You are doing better than you think 🌻",
        "Your presence makes the world softer 🌍✨",
        "Even on cloudy days, you shine 🌤️",
        "You’re not a burden, you’re a blessing 🌈"
    ]
    typing(f"💌 {random.choice(quotes)} 💌")

def hug_and_continue():
    typing("\nWould you like to keep chatting with me, cupcake? 🍰")
    again = input("Type Y to continue, or anything else to say goodbye: ")
    if again.lower() == 'y':
        mood_menu()
    else:
        typing("\nOkay snugglebug, I’ll be right here whenever you need me 🧸💤")
        typing("Never forget: You're enough. You're loved. You’re amazing. 💖")
        typing("Bye-bye for now! 🌸🌈✨")
        exit()

if __name__ == "__main__":
    intro()
>>>>>>> 6c0ca7a (new update3)

