import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import pywhatkit
import pyjokes
import requests
import time

engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Replace with your actual OpenWeatherMap API key
OPENWEATHER_API_KEY = 'yousk-proj-3PuH-djTrKoaFbJ0OyvgZi2Bu7SeNr40JasFm8ZOqalQ_OxHVKrkqotbdSnhwX-JwONZ-0GvCeT3BlbkFJVFzCiH-aMBgejP7ZTLv0R_YRhCBTnFlMalceVzv9PzUO3gkAJtWEwNcEiT35z4QFeCSK1Ap38A'

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don’t skeletons fight each other? They don’t have the guts."
]

def speak(text):
    print("🗣️ Nova:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("🧠 You said:", command)
            return command.lower()
        except:
            speak("Sorry, I didn't catch that.")
            return ""

def tell_weather():
    speak("For which city?")
    city = listen()
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {description}.")
        else:
            speak("Couldn't find the city.")

def process_command(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}")

    elif "your name" in command:
        speak("I'm Nova, your offline assistant.")

    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "search for" in command:
        query = command.replace("search for", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please tell me what to search for.")

    elif "play on youtube" in command:
        song = command.replace("play on youtube", "").strip()
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)

    elif "open notepad" in command:
        speak("Opening Notepad...")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator...")
        os.system("calc")

    elif "play music" in command:
        speak("Playing your music...")
        music_path = "C:\\Users\\moham\\downloads\\happyrock.mp3"  # Update this path
        try:
            os.startfile(music_path)
        except:
            speak("Sorry, music file not found.")

    elif "tell me a joke" in command:
        speak(random.choice(jokes))

    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "calculate" in command:
        expr = command.replace("calculate", "").strip()
        try:
            result = eval(expr)
            speak(f"The result is {result}")
        except:
            speak("Sorry, I couldn't calculate that.")

    elif "volume up" in command:
        speak("Turning volume up")
        os.system("nircmd.exe changesysvolume 2000")  # NirCmd required

    elif "volume down" in command:
        speak("Turning volume down")
        os.system("nircmd.exe changesysvolume -2000")

    elif "set reminder" in command:
        speak("What should I remind you about?")
        reminder = listen()
        speak("In how many seconds?")
        seconds = listen()
        try:
            seconds = int(seconds)
            speak(f"Okay, I will remind you in {seconds} seconds.")
            time.sleep(seconds)
            speak(f"Reminder: {reminder}")
        except:
            speak("Sorry, I couldn't set the reminder.")

    elif "note" in command:
        speak("What should I write?")
        note = listen()
        with open("note.txt", "a") as file:
            file.write(f"{datetime.datetime.now()}: {note}\n")
        speak("Note saved.")

    elif "weather" in command:
        tell_weather()

    elif "send whatsapp" in command:
        speak("Tell me the number with country code.")
        number = listen().replace(" ", "")
        speak("What should I say?")
        message = listen()
        try:
            pywhatkit.sendwhatmsg_instantly(f"+{number}", message)
            speak("Message sent.")
        except:
            speak("Failed to send message.")

    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")

    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")

    elif "exit" in command or "stop" in command:
        speak("Goodbye Rizzy!")
        exit()

    else:
        speak("Sorry, I can't do that yet.")

def main():
    speak("Hi Rizzy, I'm Nova. How can I help you today?")
    while True:
        command = listen()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
