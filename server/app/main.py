# pip install Flask
from flask import Flask, jsonify, request
# pip install sqlalchemy, flask_sqlalchemy
# from flask_sqlalchemy import SQLalchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ggdbuahlhppdpj:868aecec8547c09e6bf38bccf743ca92bf41ea71b2b490af20f0472a6aee8fff@ec2-54-209-187-69.compute-1.amazonaws.com:5432/d4dtc4du1mree0'
# app.debug = True
# db = SQLalchemy(app)

@app.route('/test', method=['GET'])
def test():
    return {
        'test': 'test1'
    }