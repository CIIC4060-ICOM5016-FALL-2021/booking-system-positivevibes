from flask import jsonify
from model.users import UsersDAO

class Users:

    def build_row_dict(self, row):
        if row:
            result = {
                "user_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "authorization_level": row[3],
                "user_email": row[4],
                "user_password": row[5]
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result

    def getAllUsers(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = UsersDAO()
        tuples = dao.getAllUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getUserById(self, user_id):
        dao = UsersDAO()
        tuple = dao.getUserById(user_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)