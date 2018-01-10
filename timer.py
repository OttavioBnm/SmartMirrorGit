import schedule
import time

import display as d

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

print("Loading")

d.init()

def checkinternetConnection():
	try:
		response = requests.get("http://www.google.com")
		print("Connected to internet")
		return True
	except requests.ConnectionError:
		print("Not connected to internet")
		return False

def update_time():
    current = time.strftime("%H:%M")
    seconds = time.strftime("%S")
    d.updateTime(current + ":" + seconds)

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
    	'light rain' : 'petites averses',
    	'overcast clouds' : 'gros nuages',
        'light intensity shower rain' : 'pluie légère'
    }

    m_symbol = '\xb0' + 'C'

    txtcityName = data['city']+ ", " +data['country']
    txtTemp = str(int(data['temp'])) + m_symbol   
    txtSky = skyName[str(data['sky'])]
    #txtSky = str(data['sky'])
    maxmin = '  Max {} \nMin {}'.format(data['temp_max'], data['temp_min'])

    d.updateWeather(txtcityName, maxmin, txtTemp, txtSky)
    
def update_date():
	date = time.strftime("%A, %d  %B  %Y")
	d.updateDate(date)

def update_rss():
	d.updateRSSView()

def loadRssData():
	d.updateRSSData()

def update_mood():
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

	d.updateMood(mymoodText)

def update_display():
	d.UpdateView()


schedule.every(5).seconds.do(update_rss)

schedule.every(1).hour.do(update_weather)
#schedule.every(1).seconds.do(loadRssData)

schedule.every().day.at("00:00").do(update_date)

update_mood()
update_weather()
update_date()
loadRssData()
update_rss()


schedule.every(1).seconds.do(update_time)
schedule.every(1).seconds.do(update_display)
schedule.every(5).minutes.do(update_mood)

print("Running")
while True:
    schedule.run_pending()
    time.sleep(1)
