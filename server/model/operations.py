from config.dbconfig import pg_config
import psycopg2

class OperationsDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
    
    #Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "select room_id from rooms where 0 = (select count(*) from room_unavailability where room_unavailability.room_id = rooms.room_id and room_unavail_date = %s and (room_start_time between %s and %s or room_end_time between %s and %s))"
        cursor.execute(query, (room_unavail_date, room_start_time, room_end_time, room_start_time, room_end_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Find who appointed a room at a certain time
    def whoAppointedRoom(self, room_id, user_id, date, time):
        cursor = self.conn.cursor()
        query = "select user_id from schedule as s where room_id = %s and schedule_date = %s and %s between schedule_start_time and schedule_end_time and (select authorization_level from users as u where u.user_id = %s) >= (select authorization_level from rooms as r where r.room_id = %s)"
        cursor.execute(query, (room_id, date, time, user_id, room_id,))
        uid = cursor.fetchone()
        if not uid:
            return 'error'
        else:
            uid = uid[0]
        return uid

    #Give an all-day schedule for a room
    def getRoomAllDaySchedule(self, room_id, user_id, room_unavail_date):
        cursor = self.conn.cursor()
        query = "select room_start_time, room_end_time from room_unavailability where room_id=%s and room_unavail_date=%s and (select authorization_level from users as u where u.user_id = %s) >= (select authorization_level from rooms as r where r.room_id = %s) group by room_unavail_date, room_start_time, room_end_time order by room_start_time, room_end_time"
        cursor.execute(query, (room_id, room_unavail_date, user_id, room_id))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Give an all-day schedule for a user
    def getAllDayScheduleforUser(self, user_id, user_date):
        cursor = self.conn.cursor()
        query = "select user_start_time, user_end_time from user_unavailability where user_id=%s and user_date=%s group by user_date, user_start_time, user_end_time order by user_start_time, user_end_time"
        cursor.execute(query, (user_id, user_date,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Find a time that is free for everyone in the meeting
    def findAvailableTimeSlot(self, schedule_start_time, schedule_end_time):
        cursor = self.conn.cursor()
        query = "select s.schedule_start_time, s.schedule_end_time from user_unavailability as u natural inner join schedule as s where s.schedule_start_time not between %s and %s and s.schedule_end_time not between %s and %s"
        cursor.execute(query,(schedule_start_time, schedule_end_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result


    #########12. User Statistic########

    #a. Most used Room
    def getMostUsedRoom(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT room_id FROM schedule where user_id=%s GROUP BY room_id Order BY COUNT (user_id) desc limit 1"
        cursor.execute(query,(user_id),)
        result = []
        for row in cursor:
            result.append(row)
        return result
    #b. User logged in user has been most booked with
    def getMostBookedWithUser(self, user_id):
        cursor = self.conn.cursor()
        query = "select i2.user_id, count(*) from invitee as i1 inner join invitee as i2 on i1.schedule_id = i2.schedule_id where i1.user_id = %s and i1.user_id <> i2.user_id group by i2.user_id order by count(*) desc limit 1"
        cursor.execute(query,(user_id),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #########13. Global Statistic########
    
    #a. Find busiest hours (Find top 5)
    def getBusiestHours(self):
        cursor = self.conn.cursor()
        query = "SELECT schedule_start_time, COUNT (schedule_start_time) FROM schedule GROUP BY schedule_start_time Order BY COUNT (schedule_start_time) desc fetch first 5 rows only"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #b. Find most booked users (Find top 10)
    def getMostBookedUsers(self):
        cursor = self.conn.cursor()
        query = "SELECT user_id, COUNT (user_id) FROM invitee GROUP BY user_id Order BY COUNT (user_id) desc fetch first 10 rows only"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #c. Find most booked rooms (Find top 10)
    def getMostBookedRooms(self):
        cursor = self.conn.cursor()
        query = "SELECT room_id, COUNT (room_id) FROM schedule GROUP BY room_id Order BY COUNT (room_id) desc fetch first 10 rows only"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result