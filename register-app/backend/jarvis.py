import speech_recognition as sr
import pyttsx3
import requests
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS

# ✅ Configure Logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Voice volume

# ✅ Python Dictionary for Command Recognition
COMMANDS = {
    "log me in": {"response": "Please say your email", "navigate": "voice-login"},
    "go to home": {"response": "Opening Home Page", "navigate": "home.html"},
    "go to contact": {"response": "Opening Contact Page", "navigate": "contact.html"},
    "open about": {"response": "Opening About Page", "navigate": "about.html"},
    "open profile": {"response": "Opening Profile Page", "navigate": "profile.html"},
    "open settings": {"response": "Opening Settings Page", "navigate": "settings.html"},
    "open services": {"response": "Opening Services Page", "navigate": "services.html"},
    "log out": {"response": "Logging out", "navigate": "login.html"},
    
    # Conversational Commands
    "how are you": {"response": "I am J.A.R.V.I.S, your assistant. Always ready!"},
    "who are you": {"response": "I am J.A.R.V.I.S, your voice assistant"},
    "what is your purpose": {"response": "My purpose is to assist you with navigation and tasks."},
    "tell me a joke": {"response": "Why don’t skeletons fight each other? Because they don’t have the guts!"},

    # External Website Navigation
    "search google": {"response": "Opening Google.", "navigate": "https://www.google.com"},
    "open youtube": {"response": "Opening YouTube.", "navigate": "https://www.youtube.com"},
    "open facebook": {"response": "Opening Facebook.", "navigate": "https://www.facebook.com"},
    "open twitter": {"response": "Opening Twitter.", "navigate": "https://www.twitter.com"},
    
    # System Commands (Expand for more)
    "increase volume": {"response": "Increasing volume."},
    "decrease volume": {"response": "Decreasing volume."},
    "mute sound": {"response": "Muting all sounds."},
    "unmute sound": {"response": "Unmuting sounds."},

    # Generic Error Handling
    "default": {"response": "I didn't understand that command."}
}

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    try:
        engine.runAndWait()
    except RuntimeError:
        logging.warning("run loop already started")

def listen():
    """Capture voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.debug("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            logging.debug(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            logging.error("UnknownValueError: Could not understand audio")
            return ""
        except sr.RequestError as e:
            speak("Network error.")
            logging.error(f"RequestError: {e}")
            return ""

def process_command(command):
    """Execute actions based on the voice command using a Python dictionary."""
    for key in COMMANDS.keys():
        if key in command:
            response_data = COMMANDS[key]
            speak(response_data["response"])
            if "navigate" in response_data:
                return make_response(jsonify({"navigate": response_data["navigate"]}), 200)
            else:
                return make_response(jsonify({"message": response_data["response"]}), 200)
    
    # If command not found, return default response
    speak(COMMANDS["default"]["response"])
    logging.debug(f"Unrecognized command: {command}")
    return make_response(jsonify({"message": COMMANDS["default"]["response"]}), 400)

# ✅ API to Start J.A.R.V.I.S. when triggered from the Frontend
@app.route('/start-jarvis', methods=['GET'])
def start_jarvis():
    speak("J.A.R.V.I.S is ready. Listening for commands.")
    command = listen()
    return process_command(command)

if __name__ == "__main__":
    app.run(port=5001)
