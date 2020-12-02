import sqlite3
import os
import csv
import re
import shutil
import pandas as pd
import hashlib
import time 
import threading
import numpy as np
import sqlite3
import os
import tkinter
from tkinter import *
os.system('cls')

# sqlite3 login and registration

with sqlite3.connect("project1_quiz_cs384.db") as db:
    cursor=db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS project1_registration(
username VARCHAR NOT NULL,
password VARCHAR NOT NULL,
name VARCHAR NOT NULL,
whatsapp number INTEGER(10) NOT NULL
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS project1_marks(
roll VARCHAR NOT NULL,
quiz_num INTEGER NOT NULL,
total_marks INTEGER NOT NULL
);
''')


def registration():
    username= input('Username: ')
    password = input('Password: ')
    name = input('Name: ')
    whatsapp = input('WhatsApp Number: ')
    h = hashlib.md5(password.encode())
    db = sqlite3.connect('project1_quiz_cs384.db')
    c = db.cursor()
    c.execute('DELETE FROM project1_registration WHERE username = (?)',(username))
    c.execute("INSERT INTO project1_registration (username,password,name,whatsapp) VALUES (?,?,?,?)",(username,h.hexdigest(),name,whatsapp))
    db.commit()
    quiz(username,0)

def login():
    user = input('Username: ')
    password = input('Password: ')
    h = hashlib.md5(password.encode())
    db = sqlite3.connect('project1_quiz_cs384.db')
    c = db.cursor()
    c.execute('SELECT * FROM project1_registration WHERE username = ? AND password = ?', (user, h.hexdigest()))
    if c.fetchall():
        quiz(user,1)
    else:
        print('Login failed. Kindly register yourself by filling in the following details')
        registration()

# Reading questions and answers of respective quiz
questions=[]
answers_choice=[]
indexes=[]
positive_marks=[]
neg_marks=[]
compulsory=[]
right_answer=[]
marked_ans=[]
time=20
ques=1
def make_list_of_q():
    cwd = os.getcwd()
    path = os.path.join(cwd,f"quiz_wise_questions")
    os.chdir(path)
    global text
    df = pd.read_csv(f"q{n}.csv")
    p=df.columns[-1]
    t=re.split('[a-b=]+',p)
    t=re.split('[m]+',t[1])
    time=int(t[0])
    text = df.values.tolist()
    i=0
    for row in text:
        li=[]
        li.append(row[2])
        li.append(row[3])
        li.append(row[4])
        li.append(row[5])
        answers_choice.append(li)
        questions.append(row[1])
        indexes.append(i)
        i+=1
        right_answer.append(row[6])
        positive_marks.append(row[7])
        neg_marks.append(row[8])
        if row[9].lower()=='y':
            compulsory.append("Yes")
        else:
            compulsory.append("No")
    os.chdir(cwd)

# taking in user answer 
def selected():
    global radiovar,user_answer
    global lblQuestion,r1,r2,r3,r4,r5,lblRules
    global ques
    x = radiovar.get()
    marked_ans.append(x)
    radiovar.set(-1)
    if ques < len(questions):
        lblQuestion.config(text= questions[indexes[ques]])
        lblRules.config(text= "Credits if Correct Option: "+str(positive_marks[ques])+"\nNegative Marking: "+str(neg_marks[ques])+"\nIs compulsory: "+compulsory[ques-1])
        r1['text'] = answers_choice[indexes[ques]][0]
        r2['text'] = answers_choice[indexes[ques]][1]
        r3['text'] = answers_choice[indexes[ques]][2]
        r4['text'] = answers_choice[indexes[ques]][3]
        ques += 1
    else:
        # calc()
        print(marked_ans)

# printing questions and options 
def startquiz():
    global lblQuestion,r1,r2,r3,r4,r5,lblRules
    lblQuestion = Label(
        root,
        text = questions[indexes[0]],
        font = ("Consolas", 16),
        width = 500,
        justify = "center",
        wraplength = 400,
        background = "#ffffff",
    )
    lblQuestion.pack(pady=(100,40))

    global radiovar
    radiovar = IntVar()
    radiovar.set(-1)

    r1 = Radiobutton(
        root,
        text = answers_choice[indexes[0]][0],
        font = ("Times", 12),
        value = 0,
        variable = radiovar,
        command = selected,
        background = "#ffffff",
    )
    r1.pack(pady=5)

    r2 = Radiobutton(
        root,
        text = answers_choice[indexes[0]][1],
        font = ("Times", 12),
        value = 1,
        variable = radiovar,
        command = selected,
        background = "#ffffff",
    )
    r2.pack(pady=5)

    r3 = Radiobutton(
        root,
        text = answers_choice[indexes[0]][2],
        font = ("Times", 12),
        value = 2,
        variable = radiovar,
        command = selected,
        background = "#ffffff",
    )
    r3.pack(pady=5)

    r4 = Radiobutton(
        root,
        text = answers_choice[indexes[0]][3],
        font = ("Times", 12),
        value = 3,
        variable = radiovar,
        command = selected,
        background = "#ffffff",
    )
    r4.pack(pady=5)

    r5 = Radiobutton(
        root,
        text = '**Skip this question**',
        font = ("Times", 12),
        value = 4,
        variable = radiovar,
        command = selected,
        background = "#ffffff",
    )
    r5.pack(pady=15)

    lblRules = Label(
        root,
        text = "Credits if Correct Option: "+str(positive_marks[ques-1])+"\nNegative Marking: "+str(neg_marks[ques-1])+"\nIs compulsory: "+compulsory[ques-1],
        width = 100,
        font = ("Times",14),
        background = "#4d4d4d",
        foreground = "#ffffff",
    )
    lblRules.pack(pady=50)
    

def startIspressed():
    labeltext.destroy()
    btnStart.destroy()
    make_list_of_q()
    startquiz()

def quiz(roll,lr):
    global n,root,labeltext,btnStart
    n=input("Kindly input the quiz set you woulld like to attempt from 1-3:")

    root = tkinter.Tk()
    root.title(f"Quiz {n}")
    root.geometry("700x600")
    root.config(background="#ffffff")
    root.resizable(0,0)

    labeltext = Label(
        root,
        text = "Click start to attempt the Quiz "+n,
        font = ("Comic sans MS",24,"bold"),
        background = "#ffffff",
    )
    labeltext.pack(pady=(200,50))
    
    img2 = PhotoImage(file="Frame.png")
    btnStart = Button(
        root,
        image = img2,
        relief = FLAT,
        border = 0,
        command = startIspressed,
    )
    btnStart.pack()
    root.mainloop()

print("Kindly login to attempt the Quiz")
login()