import speech_recognition as sr
import pyttsx3
import datetime
import wikipediaapi
import webbrowser
import os
import time
import ctypes
import subprocess
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How can I help you today?")
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        speak("Sorry, I didn't catch that. Could you say it again?")
        return "None"
    return query.lower()
def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(query)
    if page.exists():
        speak("According to Wikipedia...")
        speak(page.summary[:200])  # Reading first 200 characters
    else:
        speak("Sorry, I couldn't find that on Wikipedia.")
def handle_command(query):
    if 'open google' in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    
    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "").strip()
        search_wikipedia(query)

    elif 'time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")

    elif 'shutdown' in query:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")

    elif 'restart' in query:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")

    elif 'lock' in query:
        speak("Locking the device.")
        ctypes.windll.user32.LockWorkStation()

    elif 'write a note' in query:
        speak("What should I write?")
        note = takeCommand()
        with open('note.txt', 'w') as f:
            f.write(note)
        speak("Note saved.")

    elif 'read note' in query:
        try:
            with open('note.txt', 'r') as f:
                speak("Reading your note.")
                speak(f.read())
        except FileNotFoundError:
            speak("You have no saved notes.")

    elif 'exit' in query or 'quit' in query:
        speak("Goodbye!")
        exit()

    else:
        speak("I didn't understand that command.")
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        if query != "None":
            handle_command(query)
