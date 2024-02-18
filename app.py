from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed passwords
    phone = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            return redirect(url_for('home'))
        else:
            message = "Invalid credentials. Please try again."

    return render_template('login.html', message=message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(phone):
            return render_template('signup.html', error='Invalid phone number')

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password, phone=phone)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
