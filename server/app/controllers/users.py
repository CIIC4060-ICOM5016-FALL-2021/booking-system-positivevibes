from flask import jsonify

class Users:

    def getAllUsers():
        user = {"pid": 1, "first_name": "Hector", "last_name": "Miranda", "auth_lvl": 0}
        return jsonify(user)