from flask import jsonify
from model.operations import OperationsDAO
from model.rooms import RoomsDAO
from model.users import UsersDAO
from model.schedule import ScheduleDAO

def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        dao = OperationsDAO()
        tuples = dao.getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time)
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

def whoAppointedRoom(self, room_start_time):
    dao = UsersDAO()
    tuples = dao.getUserById(self, room_start_time)
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)


def getRoomAllDaySchedule(self, room_id):
    dao = ScheduleDAO()
    tuples = dao.getAllSchedules(self, room_id)
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)


def getAllDayScheduleforUser(self, user_id):
    dao = ScheduleDAO()
    tuples = dao.getAllSchedules(self, user_id)
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)

def getMostUsedRoom(self, user_id):
        dao = OperationsDAO()
        tuples = dao.getMostUsedRoom(self, user_id)
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

def getMostBookedWithUser(self, user_id):
        dao = OperationsDAO()
        tuples = dao.getMostBookedWithUser(self, user_id)
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

def findAvailableTimeSlot(self, schedule_start_time, schedule_end_time):
    dao = OperationsDAO()
    tuples = dao.findAvailableTimeSlot(self, schedule_start_time, schedule_end_time)
    result = []
    for t in tuples:
        result.append(self.build_row_dict(t))
    return jsonify(result)