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

    #12.a Most used Room
    def getMostUsedRoom(self, user_id):
        dao = OperationsDAO()
        room_id = dao.getMostUsedRoom(user_id)
        if room_id == 'error':
            return jsonify({"error": "User not found or User has not been in booked rooms."})
        return jsonify({"most_booked_room": room_id})

    #12b. User logged in user has been most booked with
    def getMostBookedWithUser(self, user_id):
        dao = OperationsDAO()
        u_id = dao.getMostBookedWithUser(user_id)
        if u_id == 'error':
            return jsonify({"error": "User not found or User has not been booked with other users."})
        return jsonify({"most_booked_user": u_id})

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