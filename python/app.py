from flask import Flask, render_template, request, redirect, url_for, flash
from routes.developer import developersRouter
from utils.db import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# models
from models.ModelUser import ModelUser

# entities
from models.entities.User import EUser

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chanelworks' #for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql:3306/chanelworks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = EUser(0, request.form['username'],
                     request.form['password'], True)
        logged_user = ModelUser.login(user=user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
                return render_template('auth/login.html')
        else:
            flash('User not found')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('developersList.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>estoy protegida </h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Pagina no encontrada </h1>"


app.register_blueprint(developersRouter)

app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)
