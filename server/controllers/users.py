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

    def build_attr_dict(self, user_id, first_name, last_name, authorization_level, user_email, user_password):
        result = {}
        result['user_id'] = user_id
        result['first_name'] = first_name
        result['last_name'] = last_name
        result['authorization_level'] = authorization_level
        result['user_email'] = user_email
        result['user_password'] = user_password
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

    def updateUser(self, json):
        user_id = json['user_id']
        first_name = json['first_name']
        last_name = json['last_name']
        authorization_level = json['authorization_level']
        user_email = json['user_email']
        user_password = json['user_password']
        dao = UsersDAO()
        update_status = dao.updateUser(user_id, first_name, last_name, authorization_level, user_email, user_password)
        result = self.build_attr_dict(user_id, first_name, last_name, authorization_level, user_email, user_password)
        return jsonify(result)

    def insertUser(self, json):
        first_name = json['first_name']
        last_name = json['last_name']
        authorization_level = json['authorization_level']
        user_email = json['user_email']
        user_password = json['user_password']
        dao = UsersDAO()
        user_id = dao.insertUser(first_name, last_name, authorization_level, user_email, user_password)
        result = self.build_attr_dict(user_id, first_name, last_name, authorization_level, user_email, user_password)
        return jsonify(result)

    def deleteUser(self, user_id):
        dao = UsersDAO()
        result = dao.deleteUser(user_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")