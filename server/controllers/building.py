from flask import jsonify
from model.building import BuildingDAO

class Building:

    def build_row_dict(self, row):
        if row:
            result = {
                "building_id": row[0],
                "building_abbreviation": row[1],
                "building_name": row[2],
                "total_rooms": row[3]
            }
        else:
            result = {
                "error": "404",
                "message": "BUILDING NOT FOUND"
            }
        return result

    def build_attr_dict(self, building_id, building_abbreviation, building_name, total_rooms):
        result = {}
        result['building_id'] = building_id
        result['building_abbreviation'] = building_abbreviation
        result['building_name'] = building_name
        result['total_rooms'] = total_rooms
        return result

    def getAllBuildings(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = BuildingDAO()
        tuples = dao.getAllBuildings()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getBuildingById(self, building_id):
        dao = BuildingDAO()
        tuple = dao.getBuildingById(building_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)
    
    def updateBuilding(self, json):
        building_id = json['building_id']
        building_abbreviation = json['building_abbreviation']
        building_name = json['building_name']
        total_rooms = json['total_rooms']
        dao = BuildingDAO()
        updated_building = dao.updateBuilding(building_id, building_abbreviation, building_name, total_rooms)
        result = self.build_attr_dict(building_id, building_abbreviation, building_name, total_rooms)
        return jsonify(result)

    def insertBuilding(self, json):
        building_abbreviation = json['building_abbreviation']
        building_name = json['building_name']
        total_rooms= json['total_rooms']
        dao = BuildingDAO()
        building_id = dao.insertBuilding(building_abbreviation, building_name, total_rooms)
        result = self.build_attr_dict(building_id, building_abbreviation, building_name, total_rooms)
        return jsonify(result)

    def deleteBuilding(self, building_id):
        dao = BuildingDAO()
        result = dao.deleteBuilding(building_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")
