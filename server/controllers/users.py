from flask import jsonify

class Users:

    def getAllUsers():
        user = {"pid": 1, "name": "test_name"}
        return jsonify(user)