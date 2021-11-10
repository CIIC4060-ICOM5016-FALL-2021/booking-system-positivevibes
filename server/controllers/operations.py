from flask import jsonify

def getAllAvailableRooms(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = RoomsDAO()
        tuples = dao.getAllRooms()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)