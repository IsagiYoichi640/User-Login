from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash,check_password_hash
app=Flask(__name__)
app.config['SECRET_KEY']='anime'
#database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db=SQLAlchemy(app)
#Email config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='gillianmasija@gmail.com'
app.config['MAIL_PASSWORD']='sxyx xvwc dfqu lhap'
mail=Mail(app)
#login maneger
lm=LoginManager()
lm.init_app(app)
#redirect the user to login page
lm.login_view='login'
serializer=URLSafeTimedSerializer(app.config['SECRET_KEY'])
#Database for users
class User(db.Model,UserMixin):
    id=db.Column(db.Interger,primary_key=True)
    username=db.Column(db.String(100))
    email=db.Column(db.Strung(100),unique=True)
    password=db.Column(db.String(200))
#load users
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#routes
