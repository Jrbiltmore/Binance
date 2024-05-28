
from flask import Flask, render_template
from .authentication import app

@app.route('/')
def home():
    return render_template('index.html')

def start():
    app.run(debug=True)
