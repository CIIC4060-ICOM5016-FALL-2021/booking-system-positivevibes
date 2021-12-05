from flask import jsonify
from model.operations import OperationsDAO

class Operations():

    #2. Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, json):
        dao = OperationsDAO()
        room_unavail_date = json['date']
        room_start_time = json['start_time']
        room_end_time = json['end_time']
        tuples = dao.getAllAvailableRooms(room_unavail_date, room_start_time, room_end_time)
        result = []
        for t in tuples:
            result.append({
                'room_id': t[0],
                'room_name': t[1]
                })
        return jsonify(result)

    #3. Find who appointed a room at a certain time
    def whoAppointedRoom(self, json):
        dao = OperationsDAO()
        room_id = json['room_id']
        user_id = json['user_id']
        date = json['date']
        time = json['time']
        user = dao.whoAppointedRoom(room_id, user_id, date, time)
        if user == 'error':
            return jsonify({"error": "Authorization level not met or no user found for appointment during that time frame at room {}".format(room_id)})
        result = {
            "user_id": user[0],
            "user_email": user[1],
            "user_first_name": user[2],
            "user_last_name": user[3]
        }
        return jsonify(result)

    #4. Give an all-day schedule for a room
    def getRoomAllDaySchedule(self, json):
        dao = OperationsDAO()
        room_id = json['room_id']
        user_id = json['user_id']
        date = json['date']
        tuples_ns, tuples_s = dao.getRoomAllDaySchedule(room_id, user_id, date)
        result = {}
        non_scheduled = []
        scheduled = []
        for t in tuples_ns:
            non_scheduled.append({
                'room_start_time' : str(t[0]),
                'room_end_time' : str(t[1]),
                'room_date' : str(t[2]),
                'slot_name' : t[3],
                'slot_description': t[4]
            })
        for t in tuples_s:
            scheduled.append({
                'room_start_time' : str(t[0]),
                'room_end_time' : str(t[1]),
                'room_date' : str(t[2]),
                'slot_name' : t[3],
                'slot_description': t[4]
            })
        result['Non-Scheduled'] = non_scheduled
        result['Scheduled'] = scheduled
        return jsonify(result)

    #5. Give an all-day schedule for a user
    def getAllDayScheduleforUser(self, json):
        dao = OperationsDAO()
        user_id = json['user_id']
        date = json['date']      
        tuples_ns, tuples_s = dao.getAllDayScheduleforUser(user_id, date)
        result = {}
        non_scheduled = []
        scheduled = []
        for t in tuples_ns:
            non_scheduled.append({
                'user_start_time' : str(t[0]),
                'user_end_time': str(t[1]),
                'user_date': str(t[2]),
                'slot_name': t[3],
                'slot_description': t[4]
            })
        for t in tuples_s:
            scheduled.append({
                'user_start_time' : str(t[0]),
                'user_end_time': str(t[1]),
                'user_date': str(t[2]),
                'slot_name': t[3],
                'slot_description': t[4]
            })
        result['Non-Scheduled'] = non_scheduled
        result['Scheduled'] = scheduled
        return jsonify(result)

    #8. Find a time that is free for everyone in the meeting
    def findAvailableTimeSlot(self, json):
        dao = OperationsDAO()
        date = json['date']
        invitees = json['invitees'].split(',')
        intervals = dao.findAvailableTimeSlot(date, invitees)
        if intervals == 'missing_invitees':
            return jsonify({"error": "Missing invitees, please specify which invitees are in the meeting."})
        if intervals == 'all_free':
            return jsonify({"available_time_slots": "00:00:00-23:59:59"})
        result = {"available_time_slots": intervals}
        return jsonify(result)

    #12.a Most used Room
    def getMostUsedRoom(self, user_id):
        dao = OperationsDAO()
        res = dao.getMostUsedRoom(user_id)
        if res == 'error':
            return jsonify({"error": "User not found or User has not been in booked rooms."})
        return jsonify({"most_booked_room": res[0],
                        "count": res[1],
                        "room_name": res[2]})

    #12b. User logged in user has been most booked with
    def getMostBookedWithUser(self, user_id):
        dao = OperationsDAO()
        res = dao.getMostBookedWithUser(user_id)
        if res == 'error':
            return jsonify({"error": "User not found or User has not been booked with other users."})
        ret = {}
        ret['most_booked_user_id'] = res[0]
        ret['count'] = res[1]
        ret['most_booked_user_name'] = res[2] + ' ' + res[3]
        return jsonify(ret)

    #13a. Find busiest hours (Find top 5)
    def getBusiestHours(self):
        dao = OperationsDAO()
        tuples = dao.getBusiestHours()
        result = {}
        intervals = []
        for t in tuples:
            intervals.append({
                "schedule_start_time" : str(t[0]),
                "schedule_end_time" : str(t[1]),
                "count" : t[2]
            })
        result['busiest_hours'] = intervals
        return jsonify(result)
        
    #13b. Find most booked users (Find top 10)
    def getMostBookedUsers(self):
        dao = OperationsDAO()
        tuples = dao.getMostBookedUsers()
        result = {}
        booked_users = []
        for t in tuples:
            booked_users.append({"user_id": t[0],
                                "count": t[1],
                                "user_name": t[2] + ' ' + t[3]})
        result['most_booked_users'] = booked_users
        return jsonify(result)

    #13c. Find most booked rooms (Find top 10)
    def getMostBookedRooms(self):
        dao = OperationsDAO()
        tuples = dao.getMostBookedRooms()
        result = {}
        rooms = []
        for t in tuples:
            rooms.append({"room_id": t[0],
                          "count": t[1],
                          "room_name": t[2]})
        result['most_booked_rooms'] = rooms
        return jsonify(result)
