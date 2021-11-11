from flask import jsonify
from model.operations import OperationsDAO

class Operations():

    #Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, json):
        dao = OperationsDAO()
        room_unavail_date = json['date']
        room_start_time = json['start_time']
        room_end_time = json['end_time']
        tuples = dao.getAllAvailableRooms(room_unavail_date, room_start_time, room_end_time)
        result = []
        for t in tuples:
            result.append({'room_id': t[0]})
        return jsonify(result)

    #Find who appointed a room at a certain time
    def whoAppointedRoom(self, json):
        dao = OperationsDAO()
        room_id = json['room_id']
        user_id = json['user_id']
        date = json['date']
        time = json['time']
        user_id = dao.whoAppointedRoom(room_id, user_id, date, time)
        if user_id == 'error':
            return jsonify({"error": "Authorization level not met or no user found for appointment during that time frame at room {}".format(room_id)})
        return jsonify({"user_id": user_id})

    #Give an all-day schedule for a room
    def getRoomAllDaySchedule(self, json):
        dao = OperationsDAO()
        room_id = json['room_id']
        user_id = json['user_id']
        date = json['date']
        tuples = dao.getRoomAllDaySchedule(room_id, user_id, date)
        result = {}
        schedule = []
        for t in tuples:
            schedule.append({
                'room_start_time' : str(t[0]),
                'room_end_time': str(t[1])
            })
        result['Schedule'] = schedule
        return jsonify(result)

    #Give an all-day schedule for a user
    def getAllDayScheduleforUser(self, json):
        dao = OperationsDAO()
        user_id = json['user_id']
        date = json['date']      
        tuples = dao.getAllDayScheduleforUser(user_id, date)
        result = {}
        schedule = []
        for t in tuples:
            schedule.append({
                'user_start_time' : str(t[0]),
                'user_end_time': str(t[1])
            })
        result['Schedule'] = schedule
        return jsonify(result)

    # def getMostUsedRoom(self, user_id):
    #         dao = OperationsDAO()
    #         tuples = dao.getMostUsedRoom(self, user_id)
    #         result = []
    #         for t in tuples:
    #             result.append(self.build_row_dict(t))
    #         return jsonify(result)

    # def getMostBookedWithUser(self, user_id):
    #         dao = OperationsDAO()
    #         tuples = dao.getMostBookedWithUser(self, user_id)
    #         result = []
    #         for t in tuples:
    #             result.append(self.build_row_dict(t))
    #         return jsonify(result)

    # def getBusiestHours(self):
    #         dao = OperationsDAO()
    #         tuples = dao.getBusiestHours()
    #         result = []
    #         for t in tuples:
    #             result.append(self.build_row_dict(t))
    #         return jsonify(result)
        
    # def getMostBookedUsers(self):
    #         dao = OperationsDAO()
    #         tuples = dao.getMostBookedUsers()
    #         result = []
    #         for t in tuples:
    #             result.append(self.build_row_dict(t))
    #         return jsonify(result)

    # def getMostBookedRooms(self):
    #         dao = OperationsDAO()
    #         tuples = dao.getMostBookedRooms()
    #         result = []
    #         for t in tuples:
    #             result.append(self.build_row_dict(t))
    #         return jsonify(result)

    # def findAvailableTimeSlot(self, schedule_start_time, schedule_end_time):
    #     dao = OperationsDAO()
    #     tuples = dao.findAvailableTimeSlot(self, schedule_start_time, schedule_end_time)
    #     result = []
    #     for t in tuples:
    #         result.append(self.build_row_dict(t))
    #     return jsonify(result)