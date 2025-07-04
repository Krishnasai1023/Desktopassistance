import os
import struct
import subprocess
import time
import webbrowser
import sqlite3
from shlex import quote

import eel
import pygame
import pyautogui
import pywhatkit as kit
import pyaudio
import pvporcupine
from hugchat import hugchat

from backend.command import speak
from backend.config import ASSISTANT_NAME
from backend.helper import extract_yt_term, remove_words

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

pygame.mixer.init()

@eel.expose
def play_assistant_sound():
    sound_file = r"C:\Users\KRISHNA SAI\OneDrive\Desktop\Jarvis-2025-master\frontend\assets\audio\start_sound.mp3"
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


# Hardcoded app and web paths
app_paths = {
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "notepad": "notepad",
    "paint": "mspaint",
    "snipping tool": "snippingtool",
    "calculator": "calc",
    "camera": "microsoft.windows.camera:",
    "control panel": "control"
}

web_links = {
    "telegram": "https://web.telegram.org/",
    "whatsapp": "https://web.whatsapp.com/",
    "linkedin": "https://www.linkedin.com/",
    "github": "https://github.com/",
    "reddit": "https://www.reddit.com/",
    "youtube": "https://www.youtube.com/",
    "facebook": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "gmail": "https://mail.google.com/"
}


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    try:
        cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            os.startfile(results[0][0])
            return

        cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (query,))
        results = cursor.fetchall()
        if results:
            speak(f"Opening {query}")
            webbrowser.open(results[0][0])
            return

        for key in web_links:
            if key in query:
                speak(f"Opening {key}")
                webbrowser.open(web_links[key])
                return

        for key in app_paths:
            if key in query:
                speak(f"Opening {key}")
                os.system(f"start {app_paths[key]}")
                return

        speak(f"Trying to open {query}")
        os.system(f"start {query}")
    except Exception as e:
        speak("Something went wrong while opening.")
        print(f"[ERROR]: {e}")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    # Keep assistant trigger words removed but preserve the actual name
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
        speak("Contact not found in your database.")
        print(f"[CONTACT ERROR]: {e}")
        return 0, 0

def whatsApp(Phone, message, flag, name):
    # Hardcoded numbers for specific names
    name = name.strip().lower()
    if name == 'amit':
        Phone = '+919177419700'
    elif name == 'priya':
        Phone = '+919032704706'

    if flag == 'message':
        # Ensure the target tab for sending messages is selected
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name.title()}"
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
    elif flag == 'call':
        # Target the call tab
        target_tab = 7
        message = ''
        jarvis_message = f"Calling {name.title()}"
        whatsapp_url = f"whatsapp://call?phone={Phone}"  # Placeholder: not actually used on desktop
    else:
        # Handle video call (desktop-specific)
        jarvis_message = f"Starting video call with {name.title()}"
        whatsapp_url = "whatsapp:"  # Just open WhatsApp
        contact_name = "Amith Klu" if name == 'amit' else name.title()

    # Open WhatsApp
    full_command = f'start "" "{whatsapp_url}"'

    try:
        subprocess.run(full_command, shell=True)
        time.sleep(5)

        if flag == 'message' or flag == 'call':
            # Simulate selecting correct tab
            pyautogui.hotkey('ctrl', 'f')  # Search bar
            for _ in range(1, target_tab):
                pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
        elif flag == 'video':
            # Simulate typing contact name and clicking video call
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1)
            pyautogui.typewrite(contact_name)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)

            # Locate and click video call icon
            video_call_button = pyautogui.locateCenterOnScreen('video_call_icon.png', confidence=0.8)
            if video_call_button:
                pyautogui.click(video_call_button)
            else:
                speak("Couldn't find video call button.")
                return

        speak(jarvis_message)

    except Exception as e:
        speak("Failed to initiate WhatsApp interaction.")
        print(f"[WHATSAPP ERROR]: {e}")
def tellJoke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why did the computer go to therapy? It had too many bytes of trauma."
    ]
    import random
    joke = random.choice(jokes)
    speak(joke)
    return joke


def playGame():
    speak("Let's play a number guessing game!")
    import random
    number = random.randint(1, 10)
    guess = None
    attempts = 3
    while attempts > 0:
        speak(f"You have {attempts} attempts left. Guess a number between 1 and 10.")
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            speak("That's not a valid number.")
            continue
        if guess == number:
            speak("Congratulations! You guessed it right.")
            return
        elif guess < number:
            speak("Too low!")
        else:
            speak("Too high!")
        attempts -= 1
    speak(f"Sorry, you lost. The correct number was {number}.")
