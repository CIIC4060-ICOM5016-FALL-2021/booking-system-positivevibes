from config.dbconfig import pg_config
import psycopg2

class OperationsDAO():
    
    
    #Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "select room_id from rooms natural inner join room_unavailability where room_id NOT IN (select room_id from room_unavailability)"
        cursor.execute(query, (room_unavail_date, room_end_time, room_start_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Find who appointed a room at a certain time
    def whoAppointedRoom(self, room_start_time):
        cursor = self.conn.cursor()
        query = "select user_id from users natural inner join schedule where schedule_start_time = %s"
        cursor.execute(query, (room_start_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #Give an all-day schedule for a room
    def getRoomAllDaySchedule(self, room_id):
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


    #########12. User Statistic########

    #a. Most used Room
    def getMostUsedRoom(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT user_id FROM invitee GROUP BY user_id where user_id=%s Order BY COUNT (user_id) desc limit 1"
        cursor.execute(query,(user_id),)
        result = []
        for row in cursor:
            result.append(row)
        return result
    #b. User logged in user has been most booked with

    #########13. Global Statistic########
    
    #a. Find busiest hours (Find top 5)
    def getBusiestHours(self):
        cursor = self.conn.cursor()
        query = "SELECT schedule_start_time, COUNT (schedule_start_time) FROM schedule GROUP BY schedule_start_time Order BY COUNT (schedule_start_time) desc fetch first 5 rows only"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #b. Find most booked users (Find top 10)
    def getMostBookedUsers(self):
        cursor = self.conn.cursor()
        query = "SELECT user_id, COUNT (user_id) FROM invitee GROUP BY user_id Order BY COUNT (user_id) desc fetch first 10 rows only"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #c. Find most booked rooms (Find top 10)
    def getMostBookedRooms(self):
        cursor = self.conn.cursor()
        query = "SELECT room_id, COUNT (room_id) FROM schedule GROUP BY room_id Order BY COUNT (room_id) desc fetch first 10 rows only"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result