#!/usr/bin/python3
"""
A script that starts a Flask web application:
    - Your web application must be listening on 0.0.0.0, port 5000
    - Routes:
        - /: display “Hello HBNB!”
        - /hbnb: display “HBNB”
        - /c/<text>: display “C ”, followed by the value of the text variable
            (replace underscore _ symbols with a space )
        - /python/(<text>): display “Python ”, followed by the value of the
            text variable (replace underscore _ symbols with a space )
            - The default value of text is “is cool”
        - /number/<n>: display “n is a number” only if n is an integer
    - You must use the option strict_slashes=False in your route definition
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Return an HTTP response"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def just_hbnb():
    """Return another HTTP response"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text: str):
    """Return another HTTP response with dynamic data"""
    return f"C {text.replace('_', ' ')}"


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text: str):
    """Return another HTTP response with dynamic data"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Return another HTTP response with dynamic integer data"""
    return f"{n} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
