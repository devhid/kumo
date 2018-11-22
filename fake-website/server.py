from flask import Flask, render_template, request, jsonify, Response, url_for

app = Flask(__name__) # Init app
pages = [
    '/standard'
]

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html', pages = pages)

@app.route('/standard', methods = ['GET', 'POST'])
def standard():
    return render_template('login-standard.html')

if __name__ == '__main__':
    app.run(debug = True)