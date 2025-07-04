import subprocess
import pyautogui
import time
from urllib.parse import quote
import eel

# Hardcoded assistant name
ASSISTANT_NAME = "Jarvis"

# Find Contact function to retrieve phone number based on the query
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)
    
    try:
        query = query.strip().lower()

        # Hardcoded names and numbers
        if "amit" in query:
            return '+919177419700', 'amit'
        elif "priya" in query:
            return '+919032704706', 'priya'

        cursor.execute(
            "SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            ('%' + query + '%', query + '%')
        )
        results = cursor.fetchall()

        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            raise ValueError("Contact not found.")
    except Exception as e:
        print(f"[CONTACT ERROR]: {e}")
        return 0, 0

# WhatsApp function for sending messages and making calls
def whatsApp(Phone, message, flag, name):
    # Hardcoded numbers for specific names
    name = name.strip().lower()
    if name == 'amit':
        Phone = '+919177419700'
    elif name == 'priya':
        Phone = '+919032704706'

    if flag == 'message':
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name.title()}"
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f"Calling {name.title()}"
    else:
        target_tab = 6
        message = ''
        jarvis_message = f"Starting video call with {name.title()}"

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    try:
        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)

        pyautogui.hotkey('ctrl', 'f')
        for _ in range(1, target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        speak(jarvis_message)

    except Exception as e:
        speak("Failed to initiate WhatsApp interaction.")
        print(f"[WHATSAPP ERROR]: {e}")
        
# Speak function to provide audio feedback (can be implemented using pyttsx3 or any other library)
def speak(message):
    print(message)  # For debugging purposes, or can use pyttsx3 for actual speech.

# Function to remove unwanted words from the query
def remove_words(query, words_to_remove):
    for word in words_to_remove:
        query = query.replace(word, '')
    return query.strip()

# Eel function exposed to the frontend for handling commands
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
                        query = takecommand()
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)

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
