from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from forms.standard_login import StandardLogin
from forms.register import Register

app = Flask(__name__) # Init app
pages = [
    '/login',
    '/register'
]

# In memory record of user accounts
accounts = dict()

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html', pages = pages)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = StandardLogin(request.form)
    if request.method == 'POST':
        if (form.email.data in accounts.keys() and form.password.data == accounts[form.email.data]) or (form.email.data == 'admin@mizio.io' and form.password.data == 'admin'):
            return redirect('/success')
        return render_template('login-standard.html', form = StandardLogin(), error = 'Invalid credentials.')

    return render_template('login-standard.html', form = StandardLogin())

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = Register(request.form)
    if request.method == 'POST':
        if form.email.data in accounts.keys():
            return render_template('registration.html', form = Register(), error = 'User already exists. Please login instead.')

        if len(form.email.data) == 0 or len(form.password.data) == 0:
            return render_template('registration.html', form = Register(), error = 'Please enter valid credentials.')

        accounts[form.email.data] = form.password.data # Register user
        return redirect('/success')

    return render_template('registration.html', form = Register())

@app.route('/funform', methods = ['GET', 'POST'])
def funform():
    form_login = Login(request.form)
    register_form = Register(request.form)

    # Split between two form types
    if request.form['btn'] == 'Register':

    elif request.form['btn'] == 'Login':
        

@app.route('/success', methods = ['GET'])
def success():
    return render_template('success.html', pages = pages)

if __name__ == '__main__':
    app.run(debug = True, threaded = True)