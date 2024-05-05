import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import openai
import os
import pyautogui
import time
import ctypes


current_language = "en-in"
apps = [
    ['notepad', 'notepad.exe'],
    ['calculator', 'calc.exe'],
    ['file explorer', 'explorer.exe'],
    ['cmd', 'cmd.exe'],
    ['task manager', 'taskmgr.exe'],
    ['settings', 'ms-settings:'],
    ['microsoft edge','C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe'],
    
]


sites = [
    ["youtube", "https://www.youtube.com"],
    ["facebook", "https://www.facebook.com"],
    ["instagram", "https://www.instagram.com"],
    ["google", "https://www.google.com"],
    ["Bing", "https://www.bing.com"],
    ["wikipedia", "https://www.wikipedia.com"],
    ["chatgpt", "https://chat.openai.com/"],
    ["whatsapp", "https://web.whatsapp.com/"],
    ["invertis erp", "http://erp.invertisuniversity.ac.in:81/loginForm.aspx"],
    ["gmail", "https://mail.google.com/mail/u/0/#inbox"],
    ["geekforgeeks", "https://www.geeksforgeeks.org/"],
    ["geek for geeks", "https://www.geeksforgeeks.org/"],
    ["geeks for geeks", "https://www.geeksforgeeks.org/"]
]


# def process_openai(query): 
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": query},
#                 {"role": "assistant", "content": "Hello! How can I assist you today?"}
#             ],
#             temperature=1,
#             max_tokens=256,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         print(f"OpenAI request failed: {e}")
#         return "Sorry Sir, I couldn't process your request at the moment."




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def say(text):
    engine.say(text)
    engine.runAndWait()



def check_internet():
    try:
        say('Sir i am checking the internet Connectivity')
        subprocess.run(["ping", "8.8.8.8"], capture_output=True, check=True)
        say("Sir internet is available in your device now you can gave me commands")
        return True
    except subprocess.CalledProcessError:
        return False


def takecommand():
    global current_language  

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source , phrase_time_limit=8)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language=current_language)
            print(f"User said: {query}")
            return query
        except Exception as e:
            return ""

def wish():
    hours = int(datetime.datetime.now().hour)

    introword = "I am Your Virtual Assistant"
    if hours <= 12 and hours >= 0:
        print("Good morning sir")
        say(f"Good morning sir{introword}")
    elif hours >= 12 and hours <= 15:
        say(f"good after Noon sir{introword}")
    elif hours >= 15 and hours <= 21:
        say(f"Good  Evening  sir{introword}")
    elif hours > 21 and hours <= 24:
        say(f"sir  it's being too late{introword}")
    else:
        say("")


def exitjarvis(permission):
    if "exit".lower() in permission.lower():
        say("Jarvis is exiting")
        exit()

def terminate_program(program_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", f"{program_name}.exe"], check=True)
        print(f"Successfully terminated {program_name}.")
    except subprocess.CalledProcessError:
        print(f"Failed to terminate {program_name}.")



def play_song(song_name):
    try:
        userquery = f"https://www.youtube.com/results?search_query={'+'.join(song_name.split())}"
        webbrowser.open(userquery)
    except Exception as e:
        say("sorry sir i cant able to play music plz try again")


        
if __name__ == "__main__":
    print("Welcome in assistant kernel...")
    wish()

    wakedup = True
    if check_internet():
        while True:
            
            if not wakedup :
                permission = takecommand()
                exitjarvis(permission)
                if 'wake up'.lower() in permission.lower():
                    say('Jarvis is waked up ')
                    wakedup = True

            if wakedup:

                while True:
                    
                    query = takecommand()
                    # query= "open notepad"

                    if 'jarvis sleep'.lower() in query.lower():
                        say('Jarvis sleeping now')
                        wakedup=False
                        break
                                 
                                     
                    
                    if "play" in query.lower():
                        
                        song_name = query.replace("play", "").strip()
                        play_song(song_name)
                        

                    
                    if "terminate".lower() in query:
                        
                        program_name=query.replace("terminate","").strip()
                        terminate_program(program_name)
                    
                    for app in apps:
                        if f'open {app[0]}'.lower() in query.lower():
                            try:
                                subprocess.Popen(app[1])
                                say(f'opening {app[0]}')
                            except FileNotFoundError:
                                print(f"Error: {app[0]} not found.")
                            except Exception as e:
                                print(f"An error occurred: {e}")

                    for site in sites:
                        if f'open {site[0]}'.lower() in query.lower():
                            try:
                                webbrowser.open(site[1])
                                say(f'opening {site[0]}')
                            except Exception as e:
                                say(f"Sorry sir, There was an error opening {site[0]}")
                    
                    if 'close Current Window'.lower() in query.lower():
                        pyautogui.hotkey('alt','f4')

                    if "lock the computer" in query.lower():
                        ctypes.windll.user32.LockWorkStation()

                    if "Shutdown" in query.lower():
                        say("Hold On a Sec ! Your system is on its way to shut down") 
                        subprocess.call('shutdown / p /f')   #for windows users
    else:
        say("Sorry sir, I couldn't find an active internet connection on the device. Please connect to the internet.")
