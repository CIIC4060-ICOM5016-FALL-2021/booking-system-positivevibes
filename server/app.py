from flask import Flask, request
from controllers.users import Users

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/users', methods=['GET'])
def user_route():
    if request.method == 'GET':
        return Users().getAllUsers()
    else:
        return {
            "error": "No such route"
        }

@app.route('/users/<int:user_id>', methods=['GET'])
def user_byid_route(user_id):
    if request.method == 'GET':
        return Users().getUserById(user_id)
    else:
        return {
            "error": "404"
        }

if __name__ == '__main__':
    app.run()
