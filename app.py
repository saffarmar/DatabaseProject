from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from forms import RegisterForm, LoginForm, QuoteForm
from dao.userDAO import UserDao

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'resource'


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

                flash('You are now logged in.', 'success')
                return redirect(url_for('home'))
            else:
                error = 'Invalid login.'
            return render_template('login.html', form=form, error=error)
        else:
            error = 'Username not found.'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

@app.route('/register')
def register():
    return render_template('home.html')

@app.route('/available')
def available():
    return render_template('home.html')


@app.route('/requested')
def requested():
    return render_template('home.html')


@app.route('/profile')
def profile():
    return render_template('home.html')

@app.route('/logout')
def logout():
    return render_template('home.html')



if __name__ == '__main__':
    app.run()
