#!/usr/bin/python3
"""A simple Flask application"""
from os import getenv
from flask import Flask, render_template

from models import storage

# Create a Flask web application
app = Flask(__name__)


@app.teardown_appcontext
def remove_current_session(exception):
    """ delete current sqlalchemy session. """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_is_alive():
    """
    return and render all states, cities, places and availabe amenities.
    """
    states = storage.all('State').values()
    states = sorted(states, key=lambda state: state.name)
    amenities = storage.all('Amenity').values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    places = storage.all('Place').values()
    places = sorted(places, key=lambda place: place.name)
    return render_template(
        '100-hbnb.html',
        states=states,
        amenities=amenities,
        places=places
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
