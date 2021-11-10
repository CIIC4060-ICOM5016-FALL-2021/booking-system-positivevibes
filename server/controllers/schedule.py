from flask import jsonify
from model.schedule import ScheduleDAO

class Schedule:

    def build_row_dict(self, row):
        if row:
            result = {
                "schedule_id": row[0],
                "schedule_start_time": str(row[1]),
                "schedule_end_time": str(row[2]),
                "schedule_date": str(row[3]),
                "user_id": row[4],
                "room_id": row[5]
            }
        else:
            result = {
                "error": "404",
                "message": "USER NOT FOUND"
            }
        return result

    def build_attr_dict(self, schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id):
        result = {}
        result['schedule_id'] = schedule_id
        result['schedule_start_time'] = str(schedule_start_time)
        result['schedule_end_time'] = str(schedule_end_time)
        result['schedule_date'] = str(schedule_date)
        result['user_id'] = user_id
        result['room_id'] = room_id
        return result

    def getAllSchedules(self):
        # user = {"pid": 1, "name": "test_name"}
        # return jsonify(user)
        dao = ScheduleDAO()
        tuples = dao.getAllSchedules()
        result = []
        for t in tuples:
            result.append(self.build_row_dict(t))
        return jsonify(result)

    def getScheduleById(self, schedule_id):
        dao = ScheduleDAO()
        tuple = dao.getScheduleById(schedule_id)
        result = tuple
        result = self.build_row_dict(result)
        return jsonify(result)

    def updateSchedule(self, json):
        schedule_id = json['schedule_id']
        schedule_start_time = json['schedule_start_time']
        schedule_end_time = json['schedule_end_time']
        schedule_date = json['schedule_date']
        user_id = json['user_id']
        room_id = json['room_id']
        dao = ScheduleDAO()
        update_status = dao.updateSchedule(schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id)
        result = self.build_attr_dict(schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id)
        return jsonify(result)

    def insertSchedule(self, json):
        schedule_start_time = json['schedule_start_time']
        schedule_end_time = json['schedule_end_time']
        schedule_date = json['schedule_date']
        invitees = json['invitees']
        user_id = json['user_id']
        room_id = json['room_id']
        dao = ScheduleDAO()
        schedule_id = dao.insertSchedule(schedule_start_time, schedule_end_time, schedule_date, invitees, user_id, room_id)
        if schedule_id == 'unauthorized_access':
            return jsonify({"error": "Authorization level is not met"})
        if schedule_id == 'unavailable_timeslot':
            return jsonify({"error": "Time slot is not available in the specified time."})
        result = self.build_attr_dict(schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id)
        return jsonify(result)

    def deleteSchedule(self, schedule_id):
        dao = ScheduleDAO()
        result = dao.deleteSchedule(schedule_id)
        if result:
            return jsonify("DELETED")
        else:
            return jsonify("NOT FOUND")