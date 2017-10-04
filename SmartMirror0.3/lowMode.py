#   Author : Constantin Herrmann & Ottavio Buonomo
#   Project : SmartMirror CFPT

#Import section
import tkinter as tk
import time
import locale

import datetime


#Local language
locale.setlocale(locale.LC_ALL, 'fr_FR')

#Time
def update_timeText():
    current = time.strftime("%H:%M")
    timeText.configure(text = current)
    app.after(1000, update_timeText)  


#Application
app = tk.Tk()
app.title("Smart Miror")

app.configure(background='white', cursor="none")
app.attributes('-fullscreen', True)
	
frame = tk.Frame(app, bg='black')
frame.pack(fill='both', expand='yes')

#Affiche l'heure et les minutes
timeText = tk.Label(frame,text ="", font=("Arial", 100, "bold"), fg='white', bg='black')
timeText.place(x=app.winfo_screenwidth()/2, y=app.winfo_screenheight()/2,anchor="center")

update_timeText()
app.mainloop()