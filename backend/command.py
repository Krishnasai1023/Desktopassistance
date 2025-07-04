import time
import pyttsx3
import speech_recognition as sr
import eel
import pywhatkit

# Speak Function
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)  # Set voice
    engine.setProperty('rate', 174)            # Set speech rate
    #eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    eel.receiverText(text)

# Take Voice Command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        #eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()

# Play on YouTube
def PlayYoutube(query):
    pywhatkit.playonyt(query)

# Main Function to Handle All Commands
@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()
        if not query:
            return
        eel.senderText(query)
    else:
        query = message.lower()
        eel.senderText(query)

    try:
        if query:
            if "open" in query and "youtube" in query:
                speak("Opening YouTube")
                pywhatkit.playonyt(" ")  # Just opens YouTube homepage

            elif "youtube" in query:
                # Extract the part to play
                if "play" in query:
                    search_query = query.split("play", 1)[-1].replace("on youtube", "").strip()
                elif "search" in query:
                    search_query = query.split("search", 1)[-1].replace("on youtube", "").strip()
                else:
                    search_query = query.replace("youtube", "").strip()

                if search_query:
                    speak(f"Playing {search_query} on YouTube")
                    PlayYoutube(search_query)
                else:
                    speak("Opening YouTube")
                    pywhatkit.playonyt(" ")

            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask the user for the message
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)  # Call WhatsApp function with the number

            elif "open" in query:
                from backend.feature import openCommand
                openCommand(query)

            else:
                from backend.feature import chatBot
                chatBot(query)

        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()
