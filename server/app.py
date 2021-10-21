from flask import Flask, request
from controllers.users import Users

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/users', methods=['GET'])
def user_api():
    if request.method == 'GET':
        return Users.getAllUsers()
    else:
        return {
            "error": "No such route"
        }

if __name__ == '__main__':
    app.run()
