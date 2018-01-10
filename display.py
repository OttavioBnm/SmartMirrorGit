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

ROOT = tk.Tk()

if ROOT.winfo_screenwidth() > ROOT.winfo_screenheight():
	timeTopSpace = 40
	fontSize = 100
	xClock= 190
	spacing =230
else :
	timeTopSpace = 100
	fontSize = 100
	xClock= 200
	spacing =230

frame = tk.Frame(ROOT, bg='black')
frame.pack(fill='both', expand='yes')

timeText = tk.Label(frame,text ="", font=("Arial", fontSize, "bold"), fg='white', bg='black')
dateText = tk.Label(frame, text="", font=("Arial", int(fontSize/4)), fg = 'white', bg='black')
cityText = tk.Label(frame, text="", font=("Arial", int(fontSize/4.83)), fg = 'gray', bg='black')
tempText = tk.Label(frame, text="", font=("Arial", int(fontSize/1.815), "bold"), fg = 'white', bg='black')
skyText = tk.Label(frame, text="", font=("Arial", int(fontSize/2.41)), fg = 'gray', bg='black')
maxminText = tk.Label(frame, text="", font=("Arial", int(fontSize/4.83)), fg = 'gray', bg='black')
moodText = tk.Label(frame, text="", fg = 'white', bg='black', font=("Arial", fontSize-20))
rssTextTitle = tk.Label(frame, text="No internet", fg = 'gray', bg='black', font=("Arial", int(fontSize/8)))
rssText = tk.Label(frame, text="", fg = 'white', bg='black', font=("Arial", int(fontSize/4.5)))

i1 = 0
i2 = 0
i3 = 0

def updateTime(time):
	timeText.configure(text = time)

def updateWeather(location, minAndMax, actual, sky):
	cityText.configure(text = location)
	tempText.configure(text = actual)
	skyText.configure(text = str(sky))
	maxminText.configure(text=minAndMax)

def updateDate(date):
	dateText.configure(text = date)

def updateRSSData():
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

def updateRSSView():
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

def display_RSS(rss, i):
	rssText.configure(text = str(rss['entries'][i]['title']))
	article = rss['entries'][i]['published_parsed']
	s_date = str(article[2]) +"/"+ str(article[1]) +"/"+ str(article[0])
	s_Time=str(article[3]) + ":" + str(article[4]) + ":" + str(article[5])
	rssTextTitle.configure(text =  str(rss['feed']['title']) + " - Publié le " +s_date +" à "+s_Time)

def updateMood(text):
	moodText.configure(text=text)

def UpdateView():
	ROOT.update()

def init():
	ROOT.title("Smart Miror")

	ROOT.configure(background='white', cursor="none")
	ROOT.attributes('-fullscreen', True)

	#Affiche l'heure et les minutes	
	timeText.place(x=xClock+50, y=timeTopSpace + 50,anchor="center")

	#Affiche la date	
	dateText.place(x=xClock + 50, y = timeTopSpace-10, anchor="center")

	#Affiche la ville
	cityText.place(x= ROOT.winfo_screenwidth() - 200, y=timeTopSpace-20,anchor="center")

	#Affiche la température	
	tempText.place(x= ROOT.winfo_screenwidth() - 250, y=timeTopSpace + 40,anchor="center")

	#Affiche l'état du ciel	
	skyText.place(x= ROOT.winfo_screenwidth() - 200, y=timeTopSpace + 110,anchor="center")

	#Affiche la température max et min	
	maxminText.place(x= ROOT.winfo_screenwidth() - 160, y=timeTopSpace + 40, anchor="w")

	if ROOT.winfo_screenwidth() > ROOT.winfo_screenheight():
		moodText.place(x= 30, y= int(ROOT.winfo_screenheight()-150), anchor="w")
		rssText.place(x= int(ROOT.winfo_screenwidth() - 10), y= int(ROOT.winfo_screenheight()-170), anchor="e")
		rssTextTitle.place(x= int(ROOT.winfo_screenwidth()-10), y= int(ROOT.winfo_screenheight()-200), anchor="e")
	else:
		moodText.place(x= int(ROOT.winfo_screenwidth()/2), y= int(ROOT.winfo_screenheight()-300), anchor="center")
		rssText.place(x= int(ROOT.winfo_screenwidth()/2), y= int(ROOT.winfo_screenheight()-150), anchor="center")
		rssTextTitle.place(x= int(ROOT.winfo_screenwidth()/2), y= int(ROOT.winfo_screenheight()-180), anchor="center")

def destroy(self):
	ROOT.destroy()
