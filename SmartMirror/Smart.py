#   Author : Constantin Herrmann & Ottavio Buonomo
#   Project : SmartMirror CFPT

#Import section
import tkinter as tk
import time
import locale

import datetime
import json
import urllib.request
import socket

import random 
import feedparser
import requests
import ssl

#Local language
locale.setlocale(locale.LC_ALL, 'fr_FR')

timeTopSpace = 0
fontSize = 145
xClock= 200
i1 = 0
i2 =0
i3 = 0
spacing =240
weatherPicPath = ""
geneva = ""
sports =""
monde=""
people =""
hightech=""

#Weather
def update_weather():
    url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=7285902'+
    	'&mode=json&units=metric&APPID=dc1f4cddc447b425a6dd85d5faa6476d')
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()

    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        sky=raw_api_dict['weather'][0]['description']    
    )

    skyName = {
    	'clear sky' : 'ciel dégagé',
    	'few clouds' : 'quelques nuages',
    	'scattered clouds' : 'nuages',
    	'broken clouds' : 'très nuageux',
    	'shower rain' : 'forte pluie',
    	'rain' : 'pluie',
    	'thunderstorm' : 'orages',
    	'snow' : 'neige',
    	'mist' : 'brouillard',
    	'overcast clouds' : 'gros nuages'
    }

    m_symbol = '\xb0' + 'C'

    txtcityName = data['city']+ ", " +data['country']
    cityText.configure(text = txtcityName)

    txtTemp = str(int(data['temp'])) + m_symbol
    tempText.configure(text = txtTemp)
    
    txtSky = skyName[str(data['sky'])]
    skyText.configure(text = str(txtSky))

    maxmin = '  Max {} \nMin {}'.format(data['temp_max'], data['temp_min'])
    maxminText.configure(text=maxmin)

    win.after(60000, update_weather)

#Time
def update_timeText():
    current = time.strftime("%H:%M")
    seconds = time.strftime("%S")

    timeText.configure(text = current)
    secondText.configure(text = seconds)
    win.after(1000, update_timeText)

#Date
def update_dateText():
	date = time.strftime("%A, %d  %B  %Y")
	dateText.configure(text = date)

	win.after(60000, update_dateText)

#Mood
def update_moodText():
	#Morning mood texts
	moodMorning ={
		0 : "Bonjour",
		1 : "Bien dormi ?",
		2 : "bonne journée",
		3 : "Coucou <3",
		4 : "A ce soir"
	}
	#During date mood texts
	moodDay ={
		0 : "belle journée ?",
		1 : "Toujours aussi sexy",
		2 : "Sympa la tenue",
		3 : "Bonne fin de journée",
		4 : "Il est " + time.strftime("%H:%M")
	}
	#night mood texts
	moodNight ={
		0 : "Bonsoir",
		1 : "Te voila !",
		2 : "bisous",
		3 : "A demain",
		4 : "Bonne nuit"
	}

	moodMidNight = {
		0 : "Encore debout ?",
		1 : "Il faut dormir",
		2 : "Dure nuit ?",
		3 : "Essaie de dormir",
		4 : "Bonne nuit"
	}

	#Choose of time of the day
	moodDayTime ={
		#Morning
		0 : moodMorning[random.randrange(0, 5, 2)],
		#Day
		1 : moodDay[random.randrange(0, 5, 2)],
		#Night
		2 : moodNight[random.randrange(0, 5, 2)],
		#Mid night
		3 : moodMidNight[random.randrange(0, 5, 2)]
	}

	actualTime = int(time.strftime("%H"))

	#Verifie if entre 5h et 11h
	if actualTime > 5 and actualTime < 11:
		mymoodText = moodDayTime[0]
	#Verifie si entre 11h et 19h
	elif actualTime >= 11 and actualTime < 19:
		mymoodText = moodDayTime[1]
	elif actualTime >= 19 and actualTime < 23:
		mymoodText = moodDayTime[2]
	else :
		mymoodText = moodDayTime[3]

	moodText.configure(text=mymoodText)
	win.after(120000, update_moodText)

def update_display_Rss():
	global i1
	global i2
	global i3
	global geneva
	global sports
	global monde
	global people
	global hightech

	fluxrss ={ 
		0 : geneva,
		1 : people,
		2 : sports,
		3 : monde,
		4 : hightech
	}
	
	display_RSS(fluxrss[i1], i2)
	
	i2+= 1

	if i2%5==0:
		
		i1 += 1
		if i2 >= len(geneva):
			i1 += 1
			i2 = 0
		if i1 >= len(fluxrss):
			i1 = 0
			i3 += 1
		if i3 * 5 >= len(geneva):
			i3 = 0
		i2 = i3 * 5

	win.after(5000, update_display_Rss)

def display_RSS(rss, i):
	rssText.configure(text = str(rss['entries'][i]['title']))
	article = rss['entries'][i]['published_parsed']
	s_date = str(article[2]) +"/"+ str(article[1]) +"/"+ str(article[0])
	s_Time=str(article[3]) + ":" + str(article[4]) + ":" + str(article[5])
	rssTextTitle.configure(text =  str(rss['feed']['title']) + " - Publié le " +s_date +" à "+s_Time)
	
def update_RSS():
	global geneva
	global sports
	global monde
	global people
	global hightech

	ssl._create_default_https_context = ssl._create_unverified_context
	url_Gnv  = urllib.request.urlopen("https://www.tdg.ch/geneve/rss.html")
	url_Sports = urllib.request.urlopen("https://www.tdg.ch/sports/rss.html")
	url_Monde = urllib.request.urlopen("https://www.tdg.ch/monde/rss.html")
	url_People = urllib.request.urlopen("https://www.tdg.ch/people/rss.html")
	url_hh = urllib.request.urlopen("https://www.tdg.ch/high-tech/rss.html")
	
	geneva = feedparser.parse(url_Gnv)
	sports =feedparser.parse(url_Sports)
	monde = feedparser.parse(url_Monde)
	people = feedparser.parse(url_People)
	hightech = feedparser.parse(url_hh)

	win.after(120000, update_RSS)

#Application
win = tk.Tk()
win.title("Smart Miror")

win.configure(background='white', cursor="none")
win.attributes('-fullscreen', True)

if win.winfo_screenwidth() > win.winfo_screenheight():
	timeTopSpace = 40
	fontSize = 100
	xClock= 190
	spacing =230
else :
	timeTopSpace = 100
	fontSize = 100
	xClock= 200
	spacing =230

frame = tk.Frame(win, bg='black')
frame.pack(fill='both', expand='yes')

#Affiche l'heure et les minutes
timeText = tk.Label(frame,text ="", font=("Arial", fontSize, "bold"), fg='white', bg='black')
timeText.place(x=xClock, y=timeTopSpace + 80,anchor="center")

#Affiche les secondes
secondText = tk.Label(frame, text="", font=("Arial", int(fontSize/2)), fg = 'gray', bg='black')
secondText.place(x=xClock+spacing, y=timeTopSpace+55,anchor="center")

#Affiche la date
dateText = tk.Label(frame, text="", font=("Arial", int(fontSize/4)), fg = 'white', bg='black')
dateText.place(x=xClock + 50, y = timeTopSpace-10, anchor="center")

#Affiche la ville
cityText = tk.Label(frame, text="", font=("Arial", int(fontSize/4.83)), fg = 'gray', bg='black')
cityText.place(x= win.winfo_screenwidth() - 200, y=timeTopSpace-20,anchor="center")

#Affiche la température
tempText = tk.Label(frame, text="---", font=("Arial", int(fontSize/1.815), "bold"), fg = 'white', bg='black')
tempText.place(x= win.winfo_screenwidth() - 250, y=timeTopSpace + 40,anchor="center")

#Affiche l'état du ciel
skyText = tk.Label(frame, text="", font=("Arial", int(fontSize/2.41)), fg = 'gray', bg='black')
skyText.place(x= win.winfo_screenwidth() - 200, y=timeTopSpace + 110,anchor="center")

#Affiche la température max et min
maxminText = tk.Label(frame, text="", font=("Arial", int(fontSize/4.83)), fg = 'gray', bg='black')
maxminText.place(x= win.winfo_screenwidth() - 160, y=timeTopSpace + 40, anchor="w")

#Affiche le texte de motivation
moodText = tk.Label(frame, text="", fg = 'white', bg='black', font=("Arial", fontSize-20))
#Affiche le RSS

rssTextTitle = tk.Label(frame, text="No internet", fg = 'gray', bg='black', font=("Arial", int(fontSize/8)))

rssText = tk.Label(frame, text="", fg = 'white', bg='black', font=("Arial", int(fontSize/4.5)))

if win.winfo_screenwidth() > win.winfo_screenheight():
    moodText.place(x= 30, y= int(win.winfo_screenheight()-150), anchor="w")
    rssText.place(x= int(win.winfo_screenwidth() - 10), y= int(win.winfo_screenheight()-170), anchor="e")
    rssTextTitle.place(x= int(win.winfo_screenwidth()-10), y= int(win.winfo_screenheight()-200), anchor="e")
else:
    moodText.place(x= int(win.winfo_screenwidth()/2), y= int(win.winfo_screenheight()-300), anchor="center")
    rssText.place(x= int(win.winfo_screenwidth()/2), y= int(win.winfo_screenheight()-150), anchor="center")
    rssTextTitle.place(x= int(win.winfo_screenwidth()/2), y= int(win.winfo_screenheight()-180), anchor="center")

#print (d['entries'][0]['title'])
#print (d['entries'][0]['published'])

#Actualise
update_dateText()
update_timeText()
update_moodText()
REMOTE_SERVER = "www.google.com"

def is_connected():
    try:
        myhost = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((myhost, 80),2)
        print ("connected to internet")
        return True
    except requests.ConnectionError:
        print ("Not connected")
        return False

if(is_connected()):
	update_weather()
	update_RSS()
	update_display_Rss()
    
win.mainloop()

