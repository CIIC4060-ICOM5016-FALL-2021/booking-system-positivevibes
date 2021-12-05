from os import curdir

from flask.json import jsonify
from config.dbconfig import pg_config
from controllers.schedule import Schedule
import psycopg2

class RoomsUnavailDao():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllRoomsUnavail(self):
        cursor = self.conn.cursor()
        query = "select room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled from room_unavailability"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomUnavailById(self, room_unavail_id):
        cursor = self.conn.cursor()
        query = "select room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled from room_unavailability where room_unavail_id=%s"
        cursor.execute(query, (room_unavail_id,))
        result = cursor.fetchone()
        return result

    def updateRoomUnavail(self, room_unavail_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled):
        cursor = self.conn.cursor()
        query = "update room_unavailability set room_id=%s, room_unavail_date=%s, room_start_time=%s, room_end_time=%s, scheduled=%s where room_unavail_id=%s;"
        cursor.execute(query, (room_id, room_unavail_date, room_start_time, room_end_time, scheduled, room_unavail_id))
        self.conn.commit()
        return True

    def insertRoomUnavail(self, room_id, room_unavail_date, room_start_time, room_end_time, scheduled):
        cursor = self.conn.cursor()
        query = "insert into room_unavailability (room_id, room_unavail_date, room_start_time, room_end_time, scheduled) values (%s, %s, %s, %s, %s) returning room_unavail_id;"
        cursor.execute(query, (room_id, room_unavail_date, room_start_time, room_end_time, scheduled,))
        room_unavail_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_unavail_id

    def deleteRoomUnavail(self, room_unavail_id):
        cursor = self.conn.cursor()
        query = "select room_id, room_unavail_date, room_start_time, room_end_time, scheduled from room_unavailability where room_unavail_id = %s"
        cursor.execute(query, (room_unavail_id,))
        info = cursor.fetchone()
        scheduled = info[4]
        if scheduled == 0:
            query = "delete from room_unavailability where room_unavail_id=%s;"  
            cursor.execute(query, (room_unavail_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows != 0
        else:
            query = "select schedule_id from schedule where schedule_start_time=%s and schedule_end_time=%s and schedule_date=%s and room_id=%s"
            cursor.execute(query, (info[2], info[3], info[1], info[0],))
            sched_id = cursor.fetchone()[0]
            return Schedule().deleteSchedule(sched_id)

    def insertRoomUnavailAuth(self, user_id, room_id, room_unavail_date, room_start_time, room_end_time, scheduled):
        cursor = self.conn.cursor()
        # Verify auth
        query = "select count(*) from users where user_id = %s and authorization_level >= (select authorization_level from rooms where room_id = %s);" 
        cursor.execute(query, (user_id, room_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            return 'error'
        return self.insertRoomUnavail(room_id, room_unavail_date, room_start_time, room_end_time, scheduled)    

    def deleteRoomUnavailAuth(self, user_id, room_unavail_id):
        cursor = self.conn.cursor()
        # Verify auth
        query = "select count(*) from users where user_id = %s and authorization_level >= (select authorization_level from room_unavailability natural inner join rooms where room_unavail_id = %s);" 
        cursor.execute(query, (user_id, room_unavail_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            return 'error'
        return self.deleteRoomUnavail(room_unavail_id)
        