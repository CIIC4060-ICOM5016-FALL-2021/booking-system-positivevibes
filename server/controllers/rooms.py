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
