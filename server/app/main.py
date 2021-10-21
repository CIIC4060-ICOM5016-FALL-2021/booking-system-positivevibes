# pip install Flask flask-cors psycopg2-binary
from flask import Flask, jsonify, request
# from controllers.users import Users

app = Flask(__name__)
app.debug = True

@app.route('/test', methods=['GET'])
def test():
    return {
        'test': 'test1'
    }

@app.route('/', methods=['GET'])
def home_view():
    return "<h1>Welcome to PosVibesDB </h1>"

# @app.route('/users', methods=['GET'])
# def user_api():
#     if request.method == 'GET':
#         return Users.getAllUsers()