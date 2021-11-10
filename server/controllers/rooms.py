from flask import jsonify
from model.rooms import RoomsDAO

class Rooms:

    def build_row_dict(self, row):
        if row:
            result = {
                "room_id": row[0],
                "room_capacity": row[1],
                "authorization_level": row[2],
                "building_id": row[3],
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result

    def build_auth_row_dict(self, tuples: tuple):
        result = {}
        result['room_id'] = tuples[0][0]
        result['room_capacity'] = tuples[0][1]
        result['authorization_level'] = tuples[0][2]
        result['building_id'] = tuples[0][3]

        schedule = []
        for idx in range(0, len(tuples)):
            schedule.append({
                'room_unavail_date': str(tuples[idx][5]),
                'room_start_time': str(tuples[idx][6]),
                'room_end_time': str(tuples[idx][7])
            })
        
        result['schedule'] = schedule
        return result


    def build_attr_dict(self, room_id, room_capacity, authorization_level, building_id):
        result = {}
        result['room_id'] = room_id
        result['room_capacity'] = room_capacity
        result['authorization_level'] = authorization_level
        result['building_id'] = building_id
        return result

    def getAllRooms(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = RoomsDAO()
        tuples = dao.getAllRooms()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getRoomById(self, room_id):
        dao = RoomsDAO()
        tuple = dao.getRoomById(room_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)

    def getRoomWithAuth(self, room_id, user_id):
        dao = RoomsDAO()
        tuple = dao.getRoomWithAuth(room_id, user_id)
        if tuple == 'error':
            return jsonify({"error": "Authorization Level required not met or Room not found."})
        result = tuple
        result = self.build_auth_row_dict(result)
        return jsonify(result)

    def updateRoom(self, json):
        room_id = json['room_id']
        room_capacity = json['room_capacity']
        authorization_level = json['authorization_level']
        building_id = json['building_id']
        dao = RoomsDAO()
        update_status = dao.updateRoom(room_id, room_capacity, authorization_level, building_id)
        result = self.build_attr_dict(room_id, room_capacity, authorization_level, building_id)
        return jsonify(result)

    def insertRoom(self, json):
        room_capacity = json['room_capacity']
        authorization_level = json['authorization_level']
        building_id = json['building_id']
        dao = RoomsDAO()
        room_id = dao.insertRoom(room_capacity, authorization_level, building_id)
        result = self.build_attr_dict(room_id, room_capacity, authorization_level, building_id)
        return jsonify(result)

    def deleteRoom(self, room_id):
        dao = RoomsDAO()
        result = dao.deleteRoom(room_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
