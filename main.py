from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
local_server = True
'''
from flask_mail import Mail
'''
with open('config.json', 'r') as c:
    parameter = json.load(c)["parameter"]
    
app = Flask(__name__)
app.secret_key = " secret-key-random "
'''app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    mail_username= parameter["gmail"],
    mail_pass= parameter["password"]
)
mail = Mail(app)'''
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']

db = SQLAlchemy(app)

'''app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'mydb'
db = MYSQL(app)'''


class AdminLogin(db.Model):
    __tablename__ = 'adminlogin'

    idAdminLogin = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_passwords(self, username, password):
        return self.username == username and self.password == password


@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminLogin.query.filter_by(username=username,password=password).first()

        if user and user.check_passwords(username, password):
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/edit_about')
        else:
            return render_template("admin_login.html", error="Username and password cannot be empty.")
    return render_template('admin_login.html')





@app.route("/edit_about", methods=['GET', 'POST'])
def edit_about():
    if 'username' and 'password' in session:

        return render_template('edit_about.html')
    else:
        return render_template('admin_login.html')
    
    

        





    


    

class EditProgramDatabase(db.Model):
    __tablename__ = 'edit_programs'
    
    sno = db.Column(db.Integer, primary_key=True, nullable=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200), nullable=False)


@app.route("/edit_programs", methods=['GET', 'POST'])
def edit_programs():
    if 'username' in session:
        program = EditProgramDatabase.query.all()
        return render_template('edit_programs.html', edit_programs=program)
    else:
        return render_template('login.html')


@app.route("/add_programs", methods=['GET', 'POST'])
def add_programs():
    if 'username' in session:
        if request.method == "POST":
            title = request.form.get('title')
            description = request.form.get('description')
            entry3 = EditProgramDatabase(title=title, description=description)
            db.session.add(entry3)
            db.session.commit()
        test = EditProgramDatabase.query.all()
        return render_template('add_programs.html', edit_programs=test)
    return render_template('login.html')


'''@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'username' in session:
        dlt = EditProgramDatabase.query.filter_by(sno=sno).first()
        if dlt:
            db.session.delete(dlt)
            db.session.commit()
        return render_template("edit_programs.html")
    else:
        return render_template('login.html')'''

class EditStoreDatabase(db.Model):
    __tablename__="edit_store"
    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    equp = db.Column(db.String(45),  nullable=False)
    image = db.Column(db.String(45), nullable=False)
    link = db.Column(db.String(45), nullable=False)


@app.route("/add_store", methods=['GET', 'POST'])
def add_store():
    if 'username' in session:
        if request.method == 'POST':
            equp = request.form.get('equp')
            image = request.form.get('image')
            link = request.form.get('link')
            
            entry4 = EditStoreDatabase(equp=equp, image=image, link=link)
            db.session.add(entry4)
            db.session.commit()
            
        store_items = EditStoreDatabase.query.all()
        return render_template('add_store.html', items=store_items)
    else:
        return render_template('login.html')



@app.route("/edit_store",methods=['GET', 'POST'])
def edit_store():
    if 'username' in session:
        store_items = EditStoreDatabase.query.all()

        return render_template('edit_store.html', items=store_items)
    else:
        return render_template('login.html')


class RegisterLogin(db.Model):
    __tablename__ = 'register'
    sno = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(25),  nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, username, password):
        return (password, self.password) and (username, self.username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        entry2 = RegisterLogin(username=username, password=password)
        db.session.add(entry2)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = RegisterLogin.query.filter_by(username=username, password=password).first()

        if user and user.check_password(username, password):
            session['username'] = user.username
            session['password'] = user.password
            return redirect('/index')
        else:
            return render_template("login.html", error="Username and password cannot be empty.")
    return render_template("login.html", error="Username and password cannot be empty.")


class ContactDatabase(db.Model):
    __tablename__ = 'contact'
    serial_no = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    msg = db.Column(db.String(50), nullable=False)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if 'username' in session:
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            msg = request.form.get('message')
            entry = ContactDatabase(name=name, email=email, msg=msg)
            db.session.add(entry)
            db.session.commit()
        return render_template('contact.html')
    else:
        return render_template('login.html')


''' mail.send_message(
        f'New message from {name}',
        sender=email,
        recipients=[parameter["gmail"]],
        body=f'{msg}\n{email}')
    '''


@app.route("/index")
def index():
    if 'username' in session:
        return render_template('index.html', parameter=parameter)
    else:
        return render_template('login.html')


@app.route("/about")
def about():
    if 'username' in session:
        return render_template('about.html')
    else:
        return render_template('login.html')


@app.route("/blog")
def blog():
    if 'username' in session:
        return render_template('blog.html')
    else:
        return render_template('login.html')


@app.route("/programs")
def programs():
    if 'username' in session:
        program = EditProgramDatabase.query.all()
        return render_template('programs.html', edit_programs=program)
    else:
        return render_template('login.html')


@app.route("/store")
def store():
    if 'username' in session:
        return render_template('store.html')
    else:
        return redirect('/login')


class TestDatabase(db.Model):
    __tablename__ = 'testimonials'
    serial_num = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    tests = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


@app.route("/testimonials", methods=["GET", "POST"])
def testimonials():
    if session['username']:
        if request.method == "POST":
            name = request.form.get('name')
            tests = request.form.get('tests')
            dates = datetime.now()
            entry1 = TestDatabase(name=name, tests=tests, date=dates)
            db.session.add(entry1)
            db.session.commit()
        test = TestDatabase.query.all()
        return render_template('testimonials.html', testimonials=test)
    return render_template('login.html')


@app.route("/test", methods=['GET', 'POST'])
def taking_testimonials():
    if 'username' in session:
        test = TestDatabase.query.all()
        return render_template('test.html', testimonials=test)
    else:
        return render_template('login.html')


@app.route("/faq")
def faq():
    if 'username' in session:
        return render_template('faq.html')
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
