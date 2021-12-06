from flask import jsonify
from model.invitee import InviteeDAO

class Invitee:

    def build_row_dict(self, row):
        if row:
            result = {
                "invitee_id": row[0],
                "user_id": row[1],
                "schedule_id": row[2]
            }
        else:
            result = {
                "error": "404",
                "message": "INVITEE NOT FOUND"
            }
        return result

    def build_attr_dict(self, invitee_id, user_id, schedule_id):
        result = {}
        result['invitee_id'] = invitee_id
        result['user_id'] = user_id
        result['schedule_id'] = schedule_id
        return result

    def getAllInvitees(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = InviteeDAO()
        tuples = dao.getAllInvitees()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getInviteeById(self, invitee_id):
        dao = InviteeDAO()
        tuple = dao.getInviteeById(invitee_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)
    
    def getInviteesBySchedId(self, schedule_id):
        dao = InviteeDAO()
        tuples = dao.getInviteesBySchedId(schedule_id)
        res = []
        for t in tuples:
            res.append({
                'user_id': t[0],
                'user_email': t[1],
                'first_name': t[2],
                'last_name': t[3],
                'invitee_id': t[4]
            })
        return jsonify(res)

    def updateInvitee(self, json):
        invitee_id = json['invitee_id']
        user_id = json['user_id']
        schedule_id = json['schedule_id']
        dao = InviteeDAO()
        update_status = dao.updateInvitee(invitee_id, user_id, schedule_id)
        result = self.build_attr_dict(invitee_id, user_id, schedule_id)
        return jsonify(result)

    def insertInvitee(self, json):
        user_id = json['user_id']
        schedule_id = json['schedule_id']
        dao = InviteeDAO()
        invitee_id = dao.insertInvitee(user_id, schedule_id)
        result = self.build_attr_dict(invitee_id, user_id, schedule_id)
        return jsonify(result)

    def deleteInvitee(self, invitee_id):
        dao = InviteeDAO()
        result = dao.deleteInvitee(invitee_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")