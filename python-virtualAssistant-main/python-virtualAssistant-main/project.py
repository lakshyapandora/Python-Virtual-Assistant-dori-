
import requests
from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
import urllib.request
import playsound
from gtts import gTTS
from winsound import PlaySound
from requests_html import HTMLSession
import pyautogui as pt
from time import sleep
import pyperclip
import random
import re
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import eel
eel.init('web')
# it will be used for giving voice output
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 200)
r = sr.Recognizer()



def sendMessageToFrontend(str,type) :
    eel.addMessage(str,type);
    return

def errorMessage(str):
    eel.addMessage(str,1)
    speak(str)
    
    speak('Please try again')
    eel.addMessage('Please try again',1)
    return

def reminder(stringi):
    try:
        file = open("reminder.txt", 'a+')

        def write_notes(string1='Listening'):
            with sr.Microphone() as source:
                sendMessageToFrontend(string1,2)
                speak("Say now:")
                r.energy_threshold = 200
                r.pause_threshold = 1
                audio = r.listen(source)

                try:
                    Query = r.recognize_google(audio)

                except Exception as e:
                    sendMessageToFrontend(e,2)
                    sendMessageToFrontend("Say that again......",1)
                    return None

            y = datetime.datetime.now()
            h = y.hour
            m = y.minute
            sendMessageToFrontend("Your note has been saved ",1)
            speak("Your note has been saved ")
            file.write(str(h) + ":" + str(m) + ": " + Query+'\n')
            file.close()
    except Exception as e:
        errorMessage('Some error Occurred')        

    def read_file():
        try:
            file = open("reminder.txt", 'r')
            k = file.readlines()
            for i in k:
                speak(i)
                sleep(0.5)
            sendMessageToFrontend("Thats all",1)    
            speak("Thats all")

            if (stringi == 0):
                write_notes()
            else:
                read_file()
        except Exception as e :
            
            errorMessage('Some error occurred')



'''
def response(string1='Listening'):
    with sr.Microphone() as source:
        sendMessageToFrontend(string1)
        speak("Say now:")
        r.energy_threshold = 200
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            Query = r.recognize_google(audio)

        except Exception as e:
            sendMessageToFrontend(e)
            sendMessageToFrontend("Say that again......")
            return None
        return Query'''


def weather():
    try:
        speak("Tell me the city name:")
        sendMessageToFrontend("Tell me the city name",1)
        city = takeCommand()
        print(city)
        sendMessageToFrontend(city,2)
        sendMessageToFrontend("Wait a second let me find data",1)
        speak("Wait a second let me find the data.")

        url = "https://www.google.com/search?q="+"weather" + city
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        # sendMessageToFrontend(soup,1)
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        time_skyDescription = soup.find(
            'div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        data = time_skyDescription.split('\n')
        time = data[0]
        sky = data[1]

        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        pos = strd.find('Wind')
        otherData = strd[pos:]
        sendMessageToFrontend("Temperature is " + str(temp),1)
        speak("Temperature is" + str(temp))
        sendMessageToFrontend("Time is : " + str(time),1)
        speak("Time is : " + str(time))
        sendMessageToFrontend("and the Sky remains: " + str(sky),1)
        speak("and the Sky remains: " + str(sky))
    except Exception as e:
        errorMessage('Some error occured')    


def news_reader():
    try:
        str = "Wait for 1min... the top 10 news are loading."
        sendMessageToFrontend(str,1)
        speak(str)

        session = HTMLSession()
        url = 'https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en'
        r = session.get(url)
        r.html.render(sleep=1, scrolldown=5)
        articles = r.html.find('article')

        
        counter = 0
        for item in articles:
            if counter == 10:
                break
            try:
                newsitem = item.find('h3', first=True)
                sendMessageToFrontend(newsitem.text,1)
                speak(newsitem.text)
                sendMessageToFrontend("next",1)
                speak("next")
                counter += 1
            except:
                pass
    except Exception as e:
        errorMessage('Some error occured')        


def speak(str):
    engine.say(str)
    engine.runAndWait()


#  It will be used for sending email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('karanmottan2@gmail.com', 'mk7015582074')
    server.sendmail('karanmottan2@gmail.com', to, content)
    server.close()


# it will be used for wishing
def WishMe():
    
    hour = int(datetime.datetime.now().hour)
    greeting = "AYO! WHAT IS UP  my g"
    if hour >= 0 and hour < 12:
        sendMessageToFrontend("Good Morning",1)
        speak("good morning")
    elif hour >= 12 and hour < 18:
        sendMessageToFrontend("Good Afternoon",1)
        speak("good Afternoon")
    else:
        eel.greet("Good Evening")
        speak("Good Evening")

    sendMessageToFrontend(greeting,1)    
    speak(greeting)


# it will take voice input
def takeCommand():
    with sr.Microphone() as source:
        sendMessageToFrontend("Listening....",1)
        speak("listening")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        sendMessageToFrontend("Recognizing...",1)
        query = r.recognize_google(audio, language='en-in')
        
    except Exception as e:
        speak('Say that again please')
        sendMessageToFrontend("say that again please...",1)
        return "None"
    return query


# main function for all queries
@eel.expose
def entry():
    
    WishMe()  # it will be used for wishing
    a = True

    # while loop for continuous running of loop which will allows for different and continuous queries
    while (a == True):
        query = takeCommand().lower()

        # 1 it will serach in wikipedia
        sendMessageToFrontend(query,2)
        if 'wikipedia' in query:
            try :
                speak('Searching Wikipedia...')
                sendMessageToFrontend('Searching Wikipedia',1)
                query = query.replace("wikipedia", "")
                query = query.replace(" ",'')
                results = wikipedia.summary(query, sentences=3)
                sendMessageToFrontend('Accoring to Wikipedia',1)
                speak("According to Wikipedia")
                sendMessageToFrontend(results,1)
                speak(results)
            except Exception as e :
                errorMessage('Some error occured')   
                continue 

        elif 'weather' in query:
            weather()

        elif 'news' in query:
            news_reader()
        # 2 it will make new folder
        elif 'make new folder' in query:
            try:
                path = "C:\\Users"
                os.chdir(path)
                speak('what should be the name of folder?')
                a = takeCommand()
                os.makedirs(a)
                speak("folder created")
            except Exception as e:
                errorMessage('Some error occurred')    
                continue

        # 3 it will speak time when we ask for it
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir, the time is {strTime}")
        # 4 it will be used for sending emails
        elif 'add a reminder' in query:
            reminder(0)
        elif 'tell me my reminder' in query or 'reminder' in query:
            reminder(1)
        elif 'email' in query:
            try:
                speak("what should I say?")
                content = takeCommand()
                sendMessageToFrontend(content,2)
                to = "karanmottan59@gmail.com"
                sendEmail(to, content)
                speak("Email has been send!")
            except Exception as e:
                errorMessage('Sorry my friend. I am not able to send this email')
                

        # 5 it will paly music

        elif 'play' in query:
            try:
                search_keyword = ''
                v = query.split()
                if 'rama' in query:
                    v.remove("rama")
                if len(v) >= 2:
                    for i in range(len(v)-1):
                        search_keyword = search_keyword + "+" + v[i + 1]
                sendMessageToFrontend(search_keyword[1:],1)
                html = urllib.request.urlopen(
                    "https://www.youtube.com/results?search_query=" + search_keyword)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
                sleep(15)
            except Exception as e:
                errorMessage('Some error occurred')    

        # 6 it will allow us to chat using voice commands
        elif 'open whatsapp' in query.lower():
            def get_message():
                global x, y
                position = pt.locateOnScreen(
                    "whatsapp/smile_clip.jpg", confidence=.6)
                x = position[0]
                y = position[1]
                pt.moveTo(x, y, duration=.05)
                pt.moveTo(x + 85, y - 50, duration=.5)
                pt.tripleClick()
                pt.rightClick()
                pt.moveRel(17, -170)
                pt.click()
                whatsapp_message = pyperclip.paste()
                print("message reveived and it is " + whatsapp_message)
                speak(whatsapp_message)

            def post_response(message):
                global x, y
                position_ = pt.locateOnScreen(
                    "whatsapp/smile_clip.jpg", confidence=.6)
                pt.moveTo(position_[0] + 200, position_[1] + 20, duration=.5)
                pt.click()
                pt.typewrite(message, interval=0.01)
                pt.typewrite("\n", interval=0.01)

            def check_for_new_messages(query_):
                global x1, y1
                j = True
                while (j):
                    # continuously check for green dot and new messages
                    if query_[0] != "message":
                        position2 = pt.locateOnScreen(
                            "whatsapp/green_dot.jpg", confidence=.8)
                        if position2 is not None:
                            pt.moveTo(position2)
                            pt.moveRel(-100, 0)
                            pt.click()
                        else:
                            speak("no new other users with new messages located")
                    position1 = pt.locateOnScreen(
                        "whatsapp/smile_clip.jpg", confidence=.6)
                    pt.moveTo(position1)
                    while (j == True):
                        if pt.pixelMatchesColor(776, 924, (255, 255, 255), tolerance=10):
                            speak("user said")
                            get_message()
                        speak("speak, what you want to tell")
                        messa_ge = takeCommand()
                        if messa_ge.lower() == "stop":
                            j == False
                        post_response(messa_ge)
                        sleep(7)

            webbrowser.open("https://web.whatsapp.com/")
            sleep(7)
            speak("what do you want to do")
            query_ = takeCommand().split()

            if query_[0] == "message":
                search_name = query_[1]
                print(search_name)
                pt.moveTo(441, 270, duration=.05)
                sleep(2)
                pt.click()
                pt.typewrite(search_name, interval=0.5)
                sleep(5)
                pt.moveTo(382, 400, duration=.05)
                sleep(2)
                pt.click()
                v = True
                while (v):
                    check_for_new_messages(query_)
                    qui_t = takeCommand().lower()
                    if qui_t == "stop":
                        v == False
            else:
                check_for_new_messages(query_)

        # 8 it will be used for quiting the program
        elif 'quit' in query:
            a = False

eel.start('index.html');