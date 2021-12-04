from flask import jsonify
from model.user_unavailability import UserUnavailabilityDAO

class UserUnavailability:

    def build_row_dict(self, row):
        if row:
            result = {
                "user_unavail_id": row[0],
                "user_id": row[1],
                "user_start_time": str(row[2]),
                "user_end_time": str(row[3]),
                "user_date": str(row[4]),
                "scheduled": row[5]
            }
        else:
            result = {
                "error": "404",
                "message": "UNAVAILABLE USER NOT FOUND"
            }
        return result

    def build_attr_dict(self, user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled):
        result = {}
        result['user_unavail_id'] = user_unavail_id
        result['user_id'] = user_id
        result['user_start_time'] = str(user_start_time)
        result['user_end_time'] = str(user_end_time)
        result['user_date'] = str(user_date)
        result['scheduled'] = scheduled
        return result

    def getAllUnavailableUsers(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = UserUnavailabilityDAO()
        tuples = dao.getAllUnavailableUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getUnavailableUserById(self, user_unavail_id):
        dao = UserUnavailabilityDAO()
        tuple = dao.getUnavailableUserById(user_unavail_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)

    def updateUnavailableUser(self, json):
        user_unavail_id = json['user_unavail_id']
        user_id = json['user_id']
        user_start_time = json['user_start_time']
        user_end_time = json['user_end_time']
        user_date = json['user_date']
        scheduled = json['scheduled']
        dao = UserUnavailabilityDAO()
        update_status = dao.updateUserUnavailability(user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled)
        result = self.build_attr_dict(user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled)
        return jsonify(result)

    def insertUnavailableUser(self, json):
        user_id = json['user_id']
        user_start_time = json['user_start_time']
        user_end_time = json['user_end_time']
        user_date = json['user_date']
        scheduled = 0
        dao = UserUnavailabilityDAO()
        user_unavail_id = dao.insertUnavailableUser(user_id, user_start_time, user_end_time, user_date, scheduled)
        result = self.build_attr_dict(user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled)
        return jsonify(result)

    def deleteUnavailableUser(self, user_unavail_id):
        dao = UserUnavailabilityDAO()
        result = dao.deleteUnavailableUser(user_unavail_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")