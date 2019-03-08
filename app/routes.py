from flask import Flask, render_template, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Hello'