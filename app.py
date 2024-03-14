from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from funkcje import generateToken, getUserFromToken

app = Flask(__name__)
app.secret_key = 'endo534]p[532]'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


messagesL=[]
tokens={}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        login = request.form['username']
        haslo = request.form['password']
        potwierdzenie = request.form['confirm_password']
        user=User.query.filter_by(username=login).first()

        if user is None and haslo == potwierdzenie:
            user= User(username=login, password=haslo)
            db.session.add(user)
            db.session.commit()
            flash("Zarejestrowano pomyślnie! Możesz teraz się zalogować.", 'success')

        elif user is not None:
            flash("Login jest już zajęty.", 'danger')

        elif haslo != potwierdzenie:
            flash("Hasła się różnią.", 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        login = request.form['username']
        haslo = request.form['password']
        user = User.query.filter_by(username=login).first()
        
        if user is not None and user.password == haslo:
            tokens[login]=generateToken()            
            return redirect(url_for('chat', username=tokens[login]))
        
        else:
            flash("Nieprawidłowy login lub haslo", 'danger')

    return render_template('login.html')


@app.route('/chat', methods=['GET','POST'])
def chat():

    token=request.args.get('username')
    if request.method=='GET' and token == None or token not in tokens.values():
        return redirect(url_for('login'))
    
    if request.method=='POST':
        username = getUserFromToken(tokens,token)
        messagesL.append([request.form['message'], username])
        return redirect(url_for('chat', username = token))
    
    return render_template("chat.html", messages=messagesL)