from functools import wraps

from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from forms import RegisterForm, LoginForm
from dao.userDAO import UserDao
from dao.requestedDAO import RequestedDao
from dao.availableDAO import AvailableDao

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ciic4060'

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in.', 'danger')
            return redirect(url_for('login'))

    return wrap


def build_requested_dict(row):
    userDao = UserDao()

    # row = quote(qid, firstName, lastName, text, uploader)
    request = {}
    request['rid'] = row['rid']
    request['uploader'] = userDao.getUserById(row['uploader'])['username']
    request['uploader_id'] = row['uploader']
    request['type'] = row['type']
    request['amount'] = row['amount']
    request['restime'] = row['restime']


    return request

def build_available_dict(row):
    userDao = UserDao()

    # row = quote(qid, firstName, lastName, text, uploader)
    available = {}
    available['rid'] = row['rid']
    available['uploader'] = userDao.getUserById(row['uploader'])['username']
    available['uploader_id'] = row['uploader']
    available['type'] = row['type']
    available['amount'] = row['amount']
    available['reservable'] = row['reservable']
    available['price'] = row['price']
    available['restime'] = row['restime']


    return request

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role_type'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, not logged in as admin.', 'danger')
            return redirect(url_for('login'))

    return wrap

def is_supplier(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role_type'] == 'supplier':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, not logged in as supplier.', 'danger')
            return redirect(url_for('login'))

    return wrap

def is_requester(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role_type'] == 'requester':
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, not logged in as a requester.', 'danger')
            return redirect(url_for('login'))

    return wrap

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    dao = UserDao()
    form = LoginForm(request.form)

    if request.method == 'POST':
        # Get form fields
        username = form.username.data
        password_candidate = form.password.data

        user = dao.getUserByUsername(username)


        if user:
            # Get stored hash
            password = user['password']

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['uid'] = user['uid']
                session['role_type'] = user['role_type']

                flash('You are now logged in.', 'success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid login.'
            return render_template('login.html', form=form, error=error)
        else:
            error = 'Username not found.'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

@app.route('/admin_register')
def admin_register():
    return render_template('home.html')

@app.route('/supplier_register', methods=['GET', 'POST'])
def supplier_register():
    dao = UserDao()
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        role_type = 'supplier'
        password = sha256_crypt.encrypt(str(form.password.data))

        dao.registerUser(name, email, username, password, role_type)

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/requester_register', methods=['GET', 'POST'])
def requester_register():
    dao = UserDao()
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        role_type = 'requester'
        password = sha256_crypt.encrypt(str(form.password.data))

        dao.registerUser(name, email, username, password, role_type)

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/available')
@is_logged_in
def available():
    dao = AvailableDao()
    result = dao.getAllAvailable()
    available = []

    if result:
        for row in result:
            resource = build_available_dict(row)
            available.append(resource)

        return render_template('available.html', requested=requested)

    msg = "No Resources Found"
    return render_template('available.html', msg=msg)


@app.route('/requested')
@is_logged_in
def requested():
    dao = RequestedDao()
    result = dao.getAllRequested()
    requested = []

    if result:
        for row in result:
            request = build_requested_dict(row)
            requested.append(request)

        return render_template('requested.html', requested=requested)

    msg = "No Resources Found"
    return render_template('requested.html', msg=msg)

@app.route('/profile')
@is_logged_in
def profile():
    return render_template('home.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out.", "success")
    return redirect(url_for('login'))

@app.route('/add_request')
@is_logged_in
def add_request():
    return render_template('home.html')

@app.route('/add_resource')
@is_logged_in
def add_resource():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
