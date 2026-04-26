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
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(200))
#load users
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#routes
@app.route('/')
def home():
    return redirect(url_for('login'))
#register
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if password!=confirm_password:
            flash('Passwords do not match','danger')
            return redirect(url_for('register'))
        hashed=generate_password_hash(password)
        user=User(username=username,email=email,password=hashed)
        #save user details
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully",'success')
        return redirect(url_for('login'))
    return render_template('register.html')
#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password,request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')
#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#forgot password
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        user=User.query.filter_by(email=email).first()
        if user:
            token=serializer.dumps(email,salt='reset-password')
            link=url_for('reset',token=token,_external=True)
            msg=Message(
                'Password Rest Link',
                sender='arvinshrestha11@gmail.com',
                recipients=[email]
            )
            msg.body=f'Click on the link below to reset your password:{link}'
            mail.send(msg)
            flash('Reset Link sent to your email','success')
        else:
            flash('Email not found','danger')
    return render_template('forgot.html')
#reset password
@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        email=serializer.loads(token,salt='reset-password',max_age=300)
    except:
        flash('Invalid link','danger')
        return redirect(url_for('forgot'))
    if request.method=='POST':
        password=request.form['password']
        confirm=request.form['confirm']
        if password!=confirm:
            flash('password does not match','danger')
            return redirect(request.url)#reload the page
        user=User.query.filter_by(email=email).first()
        user.password=generate_password_hash(password)
        db.session.commit()
        flash('Password changed successfully','success')
        return redirect(url_for('login'))
    return render_template('reset.html')
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
