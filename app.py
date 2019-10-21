from flask import Flask, render_template, request, url_for, redirect,jsonify
from get_data import *


app = Flask(__name__)

@app.route('/')
def home():
    return(render_template('home.html'))

@app.route('/songs/<value>')
def song_search(value):
    songs = get_songs(value)
    return(jsonify(songs))

@app.route('/features/<value>')
def song_features(value):
    features = get_features(value)
    return(jsonify(features))

@app.route('/embed')
def embed():

    return(render_template('embed.html'))

if __name__ == '__main__':
    app.run()
