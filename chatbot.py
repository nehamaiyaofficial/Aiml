import time
import random

def typing_effect(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

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

