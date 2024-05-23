#!/usr/bin/python3
"""
A script that starts a Flask web application:
    Your web application must be listening on 0.0.0.0, port 5000
    You must use storage for fetching data from the storage engine
        (FileStorage or DBStorage) => from models import storage
        and storage.all(...)
    To load all cities of a State:
        If your storage engine is DBStorage, you must use cities relationship
        Otherwise, use the public getter method cities
    After each request you must remove the current SQLAlchemy Session:
        Declare a method to handle @app.teardown_appcontext
        Call in this method storage.close()
    Routes:
        /cities_by_states: display a HTML page: (inside the tag BODY)
            H1 tag: “States”
            UL tag: with the list of all State objects present in DBStorage
            sorted by name (A->Z) tip
                LI tag: description of one State:
                <state.id>: <B><state.name></B> + UL tag: with the list of
                City objects linked to the State sorted by name (A->Z)
                    LI tag: description of one City:
                    <city.id>: <B><city.name></B>
    Import this 7-dump to have some data
    You must use the option strict_slashes=False in your route definition
"""
from os import getenv
from flask import Flask, render_template

from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def remove_current_session(exception):
    """ delete current sqlalchemy session. """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """ render a page with all states from the database. """
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ render a page with all cities by states from the database."""
    states = storage.all('State')
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
