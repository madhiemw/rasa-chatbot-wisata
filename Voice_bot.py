## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
# sender = input("What is your name?\n")
import pyttsx3
bot_message = ""
message=""

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

# myobj = gTTS(text=bot_message)
# myobj.save("welcome.mp3")
# print('saved')
# # Playing the converted file
# file = "welcome.mp3"
# subprocess.call(['mpg123', file , '--play-and-exit'])
engine = pyttsx3.init()
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id) #female voice
engine.say(bot_message)
engine.runAndWait()
r = sr.Recognizer()  # initialize recognizer

while(True):#bot_message != "Bye" or bot_message!='thanks':
    try: 
        with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        
            print("Speak Anything :")
            r.adjust_for_ambient_noise(source, duration=0.2)

            audio = r.listen(source)  # listen to the source
     
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

    except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")

    myobj = gTTS(text=bot_message)
    myobj.save("welcome.mp3")
    print('saved')
                  # Playing the converted file
    subprocess.call(['mpg123', "welcome.mp3", '--play-and-exit'])
