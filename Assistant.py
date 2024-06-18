import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import os
import psutil

# Initialize the recognizer and the speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the properties for the speech engine
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change to voices[1].id for female voice

uname = "Raja"
aname = "Rabbit"
listening = True

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.now().hour
    greeting = "Good Night"

    if 4 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= hour < 21:
        greeting = "Good Evening"
    
    speak(f"{greeting} {uname}")

def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I did not get that")
        return "None"
    except sr.RequestError:
        print("Could not request results; check your network connection")
        return "None"
    
    return query.lower()

def execute_command(command):
    global listening

    if 'hello' in command or 'hey' in command:
        speak(f"Hello {uname}")
        listening = True
    elif 'who are you' in command:
        speak(f"I'm your {aname}")
    elif 'open google' in command:
        webbrowser.open("https://google.com")
        speak("Opening Google...")
    elif 'hello rabbit' in command:
        speak("Hello Raja, How may I help you?")
        listening = True
    elif 'open youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube...")
    elif 'open facebook' in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook...")
    elif 'close facebook' in command:
        os.system("taskkill /im msedge.exe")  # Change `msedge.exe` to the process name of your browser if different
        speak("Closing Facebook...")
    elif 'what is' in command or 'who is' in command or 'what are' in command:
        search_query = command.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"This is what I found on the internet regarding {command}")
    elif 'wikipedia' in command:
        search_query = command.replace("wikipedia", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{search_query}")
        speak(f"This is what I found on Wikipedia regarding {command}")
    elif 'time' in command:
        time_str = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time_str}")
    elif 'date' in command:
        date_str = datetime.now().strftime("%B %d")
        speak(f"Today's date is {date_str}")
    elif 'calculator' in command:
        os.system("calc.exe")
        speak("Opening Calculator")
    elif 'close calculator' in command:
        for proc in psutil.process_iter():
            if proc.name() == "Calculator.exe":  # Change if different on your system
                proc.kill()
        speak("Closing Calculator")
    elif 'stop rabbit' in command:
        speak("Okay, I am stopping listening.")
        listening = False
    else:
        search_query = command.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"I found some information for {command} on Google")

if __name__ == "__main__":
    wish_me()
    speak(f"I am your {aname}, How can I help you?")
    
    while True:
        if listening:
            command = take_command()
            if command == "none":
                continue
            execute_command(command)
        else:
            with sr.Microphone() as source:
                print("Waiting for activation command...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                query = recognizer.recognize_google(audio, language='en-in')
                if 'hello rabbit' in query.lower():
                    listening = True
                    speak("Hello Raja, How may I help you?")
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
