from datetime import datetime


from flask import Flask, render_template, request, redirect, session, make_response, send_file, jsonify
from mysql.connector import connect
from flask_mail import Mail, Message
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask (__name__)

app.config.update (
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='nehasharma23156@gmail.com',
    MAIL_PASSWORD='knightsnake1234'
)

app.secret_key = 'ghjhjhq/213763fbf'

mail = Mail (app)



@app.route ('/')
def hello_world():
    return render_template ('index.html')


@app.route ("/signup")
def signup():
    return render_template ('signUp.html')



@app.route ("/log")
def login():
    return render_template ('login.html')


@app.route ("/google")
def google():
    return render_template ('google.html')

@app.route ("/player")
def player():
    return render_template ('player.html')


@app.route ("/gaana")
def lyrics():
    return render_template ('Lyrics.html')

@app.route ('/checkLoginIn')
def checkLogIn():
    email = request.args.get ('email')
    password = request.args.get ('pwd')
    connection = connect (host="localhost", port='3306', database="music", user="root", password="123456789")
    cur = connection.cursor ()
    query1 = "select * from player_id where emailId='{}'".format (email)
    cur.execute (query1)
    xyz = cur.fetchone ()
    print (xyz)
    if xyz == None:
        return render_template ('Login.html', xyz='you are not registered')
    else:
        if password == xyz [ 3 ]:
            session [ 'email' ] = email
            session [ 'userid' ] = xyz [ 0 ]
            # return render_template('UserHome.html')
            return redirect ('/home')
        else:
            return render_template ('Login.html', xyz='your password is not correct')

@app.route ('/home')
def home():
    return 'You have sucessufully log in '

@app.route ('/logout')
def logout():
    session.pop ('emailId', None)
    return render_template ('login.html')


@app.route ('/register', methods=['post'])
def register():
    email = request.form.get ('email')
    username = request.form.get ('uname')
    password = request.form.get ('pwd')
    connection = connect (host='localhost', port='3306', database='music', user='root', password='123456789')
    cur = connection.cursor ()
    query1 = "select * from player_id where emailId='{}'".format (email)
    cur.execute (query1)
    xyz = cur.fetchone ()
    if xyz == None:
        query = "insert into player_id (emailId,username,password,is_active,created_date) values('{}','{}','{}',1,now())".format (
            email, username, password)
        cur = connection.cursor ()
        cur.execute (query)
        connection.commit ()
        return 'you are successfully registered'
    else:
        return 'already register'

@app.route ('/mailbhejo')
def mailbhejo():
    msg = Message (subject='mail sender', sender='nehasharma23156@gmail.com',
                   recipients=[ 'lakshyamishra748@gmail.com' ],
                   body="this is my first email through python")
    msg.cc = [ 'lakshya.mishra56@gmail.com' ]
    msg.html = render_template ('mail.html')
    with app.open_resource ("D:/ZERO.png") as f:
        msg.attach ("ZERO.png", "image/png", f.read ())
    mail.send (msg)
    return "mail send!!"


if __name__ == "__main__":
    app.run ()
