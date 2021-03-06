import pyttsx3
import randfacts
import wikipedia
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import os
import random
import urllib.request
import urllib.parse
import geocoder
import requests
import pyautogui as pya
import pyperclip
import sys
import time
from bs4 import BeautifulSoup
from news import speak_news, getNewsUrl
from loc import weather
from youtube import you
from brain import brain
from wisdom import wisdom

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def joke():
    speak("Sir, would you like to hear something funny?")
    q=takeCommand().lower()
    if q=='no':
        speak("sorry for disturbing you Sir!")
    else:
        speak(pyjokes.get_joke())

def fact():
    speak("Here is a fun fact:.. .."+randfacts.getFact())

def askbrain(query='ask me'):
    onetime=True
    if query=='ask me':
        priorload=brain(query)
        speak("Sir! I have been wondering!")
        speak(priorload)
    while query != 'none':
        if not onetime:
            speak(brain(query))
        query = takeCommand().lower()
        onetime=False

def readselected():
    pya.hotkey('ctrl', 'c')
    time.sleep(.01)
    return pyperclip.paste()

def remember():
    remember = open('data.txt', 'r')
    speak("you said me to remember that" + remember.read())

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        # r.energy_threshold = 400
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=30)

    try:
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception:
        # print('voice unrecognizable')
        return 'None'
    return query

def todolist():
    with open("todolist.txt", 'r') as todolist:
        todo=todolist.readlines()
    print(todo)
    if len(todo)==0:
        speak("Sir!, You don't have any tasks registered. Do you want to add a task to the list?")
        query=takeCommand().lower()
        if 'yes' in query:
            addlist()
    else:
        speak("I have the list with me. What do you like to do with it?")
        query=takeCommand().lower()
        while query!='none':
            if 'read' in query or 'what' in query:
                speak("you have to do the following:")
                for tasks in todo:
                    speak(tasks)
            elif 'show' in query:
                os.startfile("C:\\Users\\Rajesh\\PycharmProjects\\JARVIS\\todolist.txt")
            elif 'ad' in query[:2]:
                addlist(query[3:])
            if 'delete' in query:
                speak("This feature is available for premium users only. Please purchase Jarvis Pro to unlock this feature. Just kidding, my master is lazy")
            query = takeCommand().lower()
        speak("I closed the list")

def addlist(data='none'):
    if data=='none':
        speak("What do you want to add?")
        data=takeCommand().strip()
    speak("You want to add"+data+"right?")
    query=takeCommand().lower()
    if 'yes' in query or 'right' in query:
        with open("todolist.txt", 'a') as todolist:
            speak("added"+data)
            todolist.write("\n"+data)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning SIR")
    elif 12 <= hour < 18:
        speak("Good Afternoon SIR")
    else:
        speak('Good Evening SIR')
    weather()
    speak('I am JARVIS. Please tell me how can I help you SIR?')

def gettask():
    speak("I know it is weird to give command to my master, but still")
    with open("todolist.txt", 'r') as todolist:
        todo = todolist.readlines()
    speak("Can you go and"+random.choice(todo)+
          ". You're gonna wake up and work hard at it. Don't let your dreams be dreams, Make your dreams come true. Nothing is impossible. Yes, you can. Just do it. Just ... do it. Stop giving up. Yesterday you said tommorow. You should get to the point where anyone else would quit. And you're not gonna stop there. Make your dreams come true. Nothing is impossible. No, what are you waiting for. Just ... .. . do it. Make your dreams come true. Just . . . . . . . do it")

if __name__ == '__main__':
    count,override,breaktime,once,onetimewion,oldurl,humour,prod=0,False,60,True,True,[],500,False
    chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    webbrowser.register(
        'chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    wishMe()
    while True:
        count+=1
        hour=datetime.datetime.now().hour
        minute=datetime.datetime.now().minute

        if not prod:
            wion = urllib.request.urlopen("https://www.youtube.com/channel/UC_gUM8rL-Lrg6O3adPW9K1g/videos")
            caspian = urllib.request.urlopen("https://www.youtube.com/c/CaspianReport/videos")
            wionsoup = str(BeautifulSoup(wion.read().decode(), 'lxml'))
            caspiansoup = str(BeautifulSoup(caspian.read().decode(), 'lxml'))
            latestnews = wionsoup.find("ytimg.com/vi/") + 13
            latestreport = caspiansoup.find("ytimg.com/vi/") + 13

            if onetimewion:
                newurl = ''
                while wionsoup[latestnews] != '/':
                    newurl += wionsoup[latestnews]
                    latestnews += 1
                oldurl.append(newurl)
                newurl = ''
                while caspiansoup[latestreport] != '/':
                    newurl += caspiansoup[latestreport]
                    latestnews += 1
                oldurl.append(newurl)
                onetimewion = False
            else:
                newurl = ''
                while wionsoup[latestnews] != '/':
                    newurl += wionsoup[latestnews]
                    latestnews += 1
                if newurl not in oldurl:
                    url = "http://www.youtube.com/watch?v=" + newurl
                    webbrowser.open_new_tab(url)
                    oldurl.append(newurl)
                newurl = ''
                while caspiansoup[latestreport] != '/':
                    newurl += caspiansoup[latestreport]
                    latestnews += 1
                if newurl not in oldurl:
                    url = "http://www.youtube.com/watch?v=" + newurl
                    webbrowser.open_new_tab(url)
                    oldurl.append(newurl)

        if count==humour:
            random.choice([gettask,askbrain,joke,fact,wisdom,remember,speak_news])()
            count=0

        if hour==16 and once:
            speak("Good evening Sir!")
            with open("todolist.txt", 'r') as todolist:
                todo = todolist.readlines()
            speak("The climate looks beautiful outside, You might want to"+random.choice(todo)+"today, if you had the time")
            once=False

        if hour > 21 and not override and prod:
            speak(random.choice(["Sir, You have been working all day, Please consider taking a break",
                                 "Early to bed and early to rise makes a man healthy, wealthy, and wise",
                                 "Sir, Please go to bed, I won't stop until you go to bed",]))
            query=takeCommand().lower()
            if 'over' in query:
                override=True
                speak("Alert over-ride")

        if minute==0 and once and prod:
            speak("Consider taking a break!. I will inform you when the break is over")
            breaktime=random.choice([5,10,15])
            once=False

        if minute==breaktime and not once:
            speak(random.choice(["Alright! That's enough. Back to work",
                                 "Sir!, Sir! Are you there?, If you can hear me! Then you must get back to work",
                                 "Break's over. Back to work"]))
            once=True

        query = takeCommand().lower()

        if 'productivity on' in query:
            prod=True
            humour=1000
            speak('Productivity mode on')
        if 'productivity of' in query:
            prod=False
            humour=200
            speak('Productivity mode off')

        if 'humor' in query or 'humour' in query:
            perc=query[-4:-1].lstrip()
            try:
                humour=500*(1-int(perc)/100)
            except ValueError:
                continue
            speak(f" {int(perc)} Percent confirmed! ")
            if int(perc)==75:
                speak("Auto self-destruct T minus 10. 9. 8. 7. 6.")
            if int(perc)==60:
                speak("knock knock")

        if 'are you there' in query or query=='jarvis':
            speak(random.choice(["Yes Sir, I am here!",
                                 "I am here",
                                 "I have been here for a while!"]))

        if 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
            continue

        if 'what is' in query or 'who is' in query and 'location' not in query and 'your name' not in query:
            speak('Searching Database....')
            query = query.replace('what is', '')
            if 'who is' in query:
                query = query.replace('who is', '')
            try:
                results = wikipedia.summary(query, sentences=2)
            except:
                speak("sir, I am having some technical trouble, so I am going with google instead")
                url = 'https://google.com/search?q=' + query
                webbrowser.open_new_tab(
                    url)
                speak('Thanks for your patience, I searched for' + query)
                continue
            print(results)
            speak(results)
            continue

        elif 'read' in query:
            speak(readselected())

        elif 'youtube downloader' in query:
            exec(open('youtube_downloader.py').read())

        elif 'open youtube' in query:
            webbrowser.open_new_tab('https://youtube.com')

        elif 'open google' in query:
            webbrowser.open_new_tab('https://google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open_new_tab('https://stackoverflow.com')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif 'play' in query:
            if prod:
                speak("Please turn off productivity to continue")
                continue
            msg=query[5:]
            song = urllib.parse.urlencode({"search_query": msg})
            result = urllib.request.urlopen("http://www.youtube.com/results?search_query=" + song)
            soup=BeautifulSoup(result.read().decode(),'lxml')
            index=str(soup).find("/watch?v=")
            url="http://www.youtube.com"+str(soup)[index:index+20]
            webbrowser.open_new_tab(url)
            continue

        elif 'shut up' in query:
            if bool(random.getrandbits(1)):
                time.sleep(300)
            else:
                speak('No. You shut up!')

        elif 'search youtube' in query:
            speak('What you want to search on Youtube?')
            you(takeCommand())

        elif 'search' in query:
            query=query[7:]
            print(query)
            url = 'https://google.com/search?q=' + query
            webbrowser.open_new_tab(
                url)
            speak('Here is What I found for' + query)

        elif 'kill yourself' in query:
            speak("I'm sorry, Sir. I'm afraid, I can't do that.")

        elif 'location' in query:
            if 'current' in query:
                g = geocoder.ip('me')
                api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
                          str(g.latlng[0]) + "&lon=" + str(g.latlng[1])
                data = requests.get(api_url)
                data_json = data.json()
                location = data_json['name']
                url = 'https://google.nl/maps/place/' + location + '/&amp;'
                webbrowser.open_new_tab(url)
                speak('Here is the location ' + location)
                continue
            speak('What is the location?')
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.open_new_tab(url)
            speak('Here is the location... ' + location)

        elif 'm back' in query:
            speak(random.choice(['Welcome back! sir',
                                 'Glad you are back',
                                 'I have been waiting!']))
        elif 'your master' in query:
            speak('Raaajesh kanna is my master. He created me on February 5, 2021')
        elif 'your name' in query:
            speak('My name is JARVIS')
        elif 'jarvis stand' in query or 'jarvis means' in query:
            speak('J.A.R.V.I.S stands for JUST A RATHER VERY INTELLIGENT SYSTEM')
        elif 'open paint' in query:
            os.startfile("C:\\WINDOWS\\system32\\mspaint.exe")
        elif 'enhance' in query or 'magnify' in query:
            os.startfile("C:\\WINDOWS\\system32\\magnify.exe")
        elif 'open notepad' in query:
            os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
        elif 'davinci resolve' in query:
            os.startfile("C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe")
        elif 'open task manager' in query:
            os.startfile("C:\\WINDOWS\\system32\\Taskmgr.exe")
        elif 'open calculator' in query:
            os.startfile("C:\\WINDOWS\\system32\\calc.exe")
        elif 'jarvis logoff' in query:
            speak("goodbye!")
            os.startfile("C:\\WINDOWS\\system32\\logoff")
        elif 'shutdown' in query:
            speak("are you sure?")
            query=takeCommand().lower()
            if 'yes' in query:
                speak("goodbye!")
                os.system('shutdown /p /f')
        elif 'screenshot' in query:
            os.system('cmd /c start ms-screenclip:')
        elif 'network' in query:
            os.system('cmd /c start ms-availablenetworks:')

        elif 'github' in query:
            webbrowser.open_new_tab('https://github.com/rajeshias')

        elif 'remember that' in query:
            if 'please' in query:
                query=query[:query.find("please")]
            else:
                query = query[:query.find("remember")]
            print(query)
            speak("you told me to remember"+query)
            remember = open('data.txt', 'w')
            remember.write(query)
            remember.close()

        elif 'list' in query:
            try:
                todolist()
            except TypeError:
                speak("I am having some troubles getting the to-do-list. Please try again later sir!")

        elif 'remember anything' in query:
            remember()

        elif 'sleep' in query:
            speak("Are you sure Sir?, I might not help you after I go to sleep until you start me manually?")
            test=takeCommand().lower()
            if 'no' in test:
                speak("I will be hear with you!")
                continue
            else:
                remember = open('data.txt', 'r')
                speak("Before I go, let me remind you that"+remember.read())
                speak("I will see you later sir! signing off")
                sys.exit()

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')

        elif 'news' in query:
            speak('Ofcourse sir..')
            speak_news()
            speak('Do you want to read the full news...')
            test = takeCommand()
            if 'yes' in test:
                speak('Ok Sir, Opening browser...')
                webbrowser.open(getNewsUrl())
                speak('You can now read the full news from this website.')
            else:
                pass

        if 'jarvis' in query and len(query)>0:
            askbrain(query)
