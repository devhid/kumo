from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from forms.standard_login import StandardLogin
from forms.register import Register

app = Flask(__name__) # Init app
pages = [
    '/login',
    '/register',
    '/funform'
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
        return login_helper(form)

    return render_template('login-standard.html', form = StandardLogin())

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = Register(request.form)
    if request.method == 'POST':
        return register_helper(form)

    return render_template('registration.html', form = Register())

@app.route('/funform', methods = ['GET', 'POST'])
def funform():
    form_login = StandardLogin(request.form)
    form_register = Register(request.form)

    # Split between two form types
    if request.method == 'POST':
        print(request.form['btn'])
        if request.form['btn'] == 'login':
            return login_helper(form_login)

        elif request.form['btn'] == 'register':
            return register_helper(form_register)


    return render_template('fun-form.html', form_login = StandardLogin(), form_register = Register())

@app.route('/success', methods = ['GET'])
def success():
    return render_template('success.html', pages = pages)

def login_helper(form):
    print(form.email.data)
    if (form.email.data in accounts.keys() and form.password.data == accounts[form.email.data]) or (form.email.data == 'admin@mizio.io' and form.password.data == 'admin'):
        return redirect('/success')
    return render_template('login-standard.html', form = StandardLogin(), error = 'Invalid credentials.')

def register_helper(form):
    if form.email.data in accounts.keys():
        return render_template('registration.html', form = Register(), error = 'User already exists. Please login instead.')

    if len(form.email.data) == 0 or len(form.password.data) == 0:
        return render_template('registration.html', form = Register(), error = 'Please enter valid credentials.')

    accounts[form.email.data] = form.password.data # Register user
    return redirect('/success')

if __name__ == '__main__':
    app.run(debug = True, threaded = True)