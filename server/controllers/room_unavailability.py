from flask import jsonify
from model.room_unavailability import RoomsUnavailDao

class RoomUnavailability:

    def build_row_dict(self, row):
        if row:
            result = {
                "room_unavail_id": row[0],
                "room_id": row[1],
                "room_unavail_date": str(row[2]),
                "room_start_time": str(row[3]),
                "room_end_time": str(row[4]),
                "scheduled": row[5]
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result

    def build_attr_dict(self, room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled):
        result = {}
        result['room_unavail_id'] = room_unavail_id
        result['room_id'] = room_id
        result['room_unavail_date'] = str(room_unavail_date)
        result['room_start_time'] = str(room_start_time)
        result['room_end_time'] = str(room_end_time)
        result['scheduled'] = scheduled
        return result

    def getAllRoomUnavail(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = RoomsUnavailDao()
        tuples = dao.getAllRoomsUnavail()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getRoomUnavailById(self, room_unavail_id):
        dao = RoomsUnavailDao()
        tuple = dao.getRoomUnavailById(room_unavail_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)

    def updateRoomUnavail(self, json):
        room_unavail_id = json['room_unavail_id']
        room_id = json['room_id']
        room_unavail_date = json['room_unavail_date']
        room_start_time = json['room_start_time']
        room_end_time = json['room_end_time']
        scheduled = json['scheduled']
        dao = RoomsUnavailDao()
        update_status = dao.updateRoomUnavail(room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        result = self.build_attr_dict(room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        return jsonify(result)

    def insertRoomUnavail(self, json):
        room_id = json['room_id']
        room_unavail_date = json['room_unavail_date']
        room_start_time = json['room_start_time']
        room_end_time = json['room_end_time']
        scheduled = 0
        dao = RoomsUnavailDao()
        room_unavail_id = dao.insertRoomUnavail(room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        result = self.build_attr_dict(room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        return jsonify(result)

    def deleteRoomUnavail(self, room_unavail_id):
        dao = RoomsUnavailDao()
        result = dao.deleteRoomUnavail(room_unavail_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")

    def insertRoomUnavailAuth(self, json):
        user_id = json['user_id']
        room_id = json['room_id']
        room_unavail_date = json['room_unavail_date']
        room_start_time = json['room_start_time']
        room_end_time = json['room_end_time']
        scheduled = 0
        dao = RoomsUnavailDao()
        room_unavail_id = dao.insertRoomUnavailAuth(user_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        if room_unavail_id == 'error':
            return jsonify({"error": "Authorization level required not met or could not mark time-slot."})
        result = self.build_attr_dict(room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled)
        return jsonify(result)

    def deleteRoomUnavailAuth(self, user_id, room_unavail_id):
        dao = RoomsUnavailDao()
        result = dao.deleteRoomUnavailAuth(user_id, room_unavail_id)
        if result == 'error':
            return jsonify({"error": "Authorization level required not met."})
        if result == True:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
