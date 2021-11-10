from config.dbconfig import pg_config
import psycopg2

class OparetionsDao():
    
    
    #Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "select room_id from rooms where (select * from room_unavailability where room_unavail_date!=%s OR (room_unavail_date!=%s AND room_start_time>%s) OR (room_unavail_date!=%s AND room_end_time<%s)"
        cursor.execute(query, (room_unavail_date, room_end_time, room_start_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Find who appointed a room at a certain time
    def whoAppointedRoom(self, user_id, room_start_time):
        cursor = self.conn.cursor()
        query = "select user_id from users natural inner join room_unavailability where room_start_time = %s"
        cursor.execute(query, (user_id, room_start_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Give an all-day schedule for a room
    def getAllDaySchedule(self, room_id):
        cursor = self.conn.cursor()
        query = "select room_start_time, room_end_time from room_unavailability where room_id=%s"
        cursor.execute(query, (room_id),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Give an all-day schedule for a user
    def getAllDayScheduleforUser(self, user_id):
        cursor = self.conn.cursor()
        query = "select schedule_id, schedule_start_time, schedule_end_time, schedule_date, room_id from users as U natural inner join schedule as S natural inner join  rooms R where user_id = %s"
        cursor.execute(query,(user_id),)
        result = []
        for row in cursor:
            result.append(row)
        return result