import sqlite3

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

    db = sqlite3.connect('project1_quiz_cs384.db')
    c = db.cursor()
    c.execute("INSERT INTO project1_registration (username,password,name,whatsapp) VALUES (?,?,?,?)",(username,password,name,whatsapp))
    db.commit()

def login():
    user = input('Username: ')
    password = input('Password: ')

        # Connect to database
    db = sqlite3.connect('project1_quiz_cs384.db')
    c = db.cursor()
    c.execute('SELECT * FROM project1_registration WHERE username = ? AND password = ?', (user, password))

    if c.fetchall():
        print('Welcome')
    else:
        print('Login failed')

# registration()
login()