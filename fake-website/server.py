from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from forms.standard_login import StandardLogin

app = Flask(__name__) # Init app
pages = [
    '/standard'
]

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html', pages = pages)

@app.route('/standard', methods = ['GET', 'POST'])
def standard():
    form = StandardLogin(request.form)
    if request.method == 'POST':
        print(form.email)
        if form.email.data == 'admin@kumo.io' and form.password.data == 'admin':
            print('test')
            return redirect('/success')
        return render_template('login-standard.html', form = StandardLogin(), error = 'Invalid credentials.')

    return render_template('login-standard.html', form = StandardLogin())

@app.route('/success', methods = ['GET'])
def success():
    return render_template('success.html', pages = pages)

if __name__ == '__main__':
    app.run(debug = True)