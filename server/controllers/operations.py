from flask import jsonify
from model.operations import OperationsDAO
from model.rooms import RoomsDAO
from model.users import UsersDAO
from model.schedule import ScheduleDAO

def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        dao = OperationsDAO()
        tuples = dao.getAllAvailableRooms()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

def whoAppointedRoom(self, room_start_time):
    dao = UsersDAO()
    tuples = dao.getUserById()
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)


def getRoomAllDaySchedule(self, room_id):
    dao = ScheduleDAO()
    tuples = dao.getAllSchedules()
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)


def getAllDayScheduleforUser(self, user_id):
    dao = ScheduleDAO()
    tuples = dao.getAllSchedules()
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)

def getBusiestHours(self):
        dao = OperationsDAO()
        tuples = dao.getBusiestHours()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)
    
def getMostBookedUsers(self):
        dao = OperationsDAO()
        tuples = dao.getMostBookedUsers()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

def getMostBookedRooms(self):
        dao = OperationsDAO()
        tuples = dao.getMostBookedRooms()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)