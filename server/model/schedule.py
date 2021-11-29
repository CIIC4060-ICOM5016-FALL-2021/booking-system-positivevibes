from config.dbconfig import pg_config
import psycopg2
import time

class ScheduleDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllSchedules(self):
        cursor = self.conn.cursor()
        query = "select schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description from schedule;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getScheduleById(self, schedule_id):
        cursor = self.conn.cursor()
        query = "select schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description from schedule where schedule_id=%s;"
        cursor.execute(query, (schedule_id,))
        result = cursor.fetchone()
        return result

    def updateSchedule(self, schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description):
        cursor = self.conn.cursor()
        query = "update schedule set schedule_start_time=%s, schedule_end_time=%s, schedule_date=%s, user_id=%s, room_id=%s, schedule_name=%s, schedule_description=%s where schedule_id=%s;"
        cursor.execute(query, (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description, schedule_id))
        self.conn.commit()
        return True

    # Helper function for insert
    def checkConflict(self, arr: list[tuple], s_time, e_time):
        conflict = False
        t_c1 = time.strptime(str(s_time), '%H:%M:%S') # curr start_time
        t_c2 = time.strptime(str(e_time), '%H:%M:%S') # curr end_time
        for cmp in arr:
            t_cmp1 = time.strptime(str(cmp[0]), '%H:%M:%S') # cmp start_time
            t_cmp2 = time.strptime(str(cmp[1]), '%H:%M:%S') # cmp end_time
            if (t_c1 >= t_cmp1 and t_c1 < t_cmp2) or (t_c2 > t_cmp1 and t_c2 <= t_cmp2):
                conflict = True
                break
        return conflict

    def insertSchedule(self, schedule_start_time, schedule_end_time, schedule_date, invitees, user_id, room_id, schedule_name, schedule_description):
        cursor = self.conn.cursor()

        # Verify if scheduler is in invitees
        if user_id not in invitees or len(invitees) == 0:
            return 'missing_invitees'

        # Verify auth level
        query = "select count(*) from rooms where room_id=%s and rooms.authorization_level <= (select authorization_level from users where user_id=%s);"
        cursor.execute(query, (room_id, user_id,))
        count = cursor.fetchone()[0]
        if count == 0: # unauthorized access
            return "unauthorized_access"
        
        # Verify if time slot is available
        query = "select count(*) from room_unavailability where (room_start_time between %s and %s or room_end_time between %s and %s) and room_unavail_date = %s and room_id=%s;"
        cursor.execute(query, (schedule_start_time, schedule_end_time, schedule_start_time, schedule_end_time, schedule_date, room_id,))
        count = cursor.fetchone()[0]
        if count > 0: # time-slot is taken
            return "unavailable_timeslot_room"        

        # Verify if time slot is available for users
        query = "select user_start_time, user_end_time from user_unavailability where user_date = %s and ("
        for idx in range(0, len(invitees)):
            if idx > 0:
                query += " or user_id = {}".format(invitees[idx])
            else:
                query += "user_id = {}".format(invitees[idx])
        query += ") group by user_start_time, user_end_time"
        cursor.execute(query, (schedule_date,))
        unavail_timeslots = []
        for row in cursor:
            unavail_timeslots.append(row)
        if self.checkConflict(unavail_timeslots, schedule_start_time, schedule_end_time):
            return "unavailable_timeslot_user"

        # All good
        query = "insert into schedule (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description) values (%s, %s, %s, %s, %s, %s, %s) returning schedule_id;"
        cursor.execute(query, (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_name, schedule_description,))
        schedule_id = cursor.fetchone()[0]

        inv_arr = ""
        for x in invitees:
            inv_arr += "insert into invitee (schedule_id, user_id) values ({}, {}); ".format(schedule_id, x)
            inv_arr += "insert into user_unavailability (user_id, user_start_time, user_end_time, user_date) values ({}, '{}', '{}', '{}'); ".format(x, schedule_start_time, schedule_end_time, schedule_date)
        add_room_unav = "insert into room_unavailability (room_id, room_unavail_date, room_start_time, room_end_time) values ({}, '{}', '{}', '{}');".format(room_id, schedule_date, schedule_start_time, schedule_end_time)
        query = inv_arr + add_room_unav
        cursor.execute(query)

        self.conn.commit()
        return schedule_id

    def deleteSchedule(self, schedule_id):
        cursor = self.conn.cursor()
        query = "delete from schedule where schedule_id=%s"
        cursor.execute(query, (schedule_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
