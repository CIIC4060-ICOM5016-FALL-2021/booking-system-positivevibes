from config.dbconfig import pg_config
import psycopg2

class ScheduleDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllSchedules(self):
        cursor = self.conn.cursor()
        query = "select schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id from schedule;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getScheduleById(self, schedule_id):
        cursor = self.conn.cursor()
        query = "select schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id from schedule where schedule_id=%s;"
        cursor.execute(query, (schedule_id,))
        result = cursor.fetchone()
        return result

    def updateSchedule(self, schedule_id, schedule_start_time, schedule_end_time, schedule_date, user_id, room_id):
        cursor = self.conn.cursor()
        query = "update schedule set schedule_start_time=%s, schedule_end_time=%s, schedule_date=%s, user_id=%s, room_id=%s where schedule_id=%s;"
        cursor.execute(query, (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id, schedule_id))
        self.conn.commit()
        return True

    def insertSchedule(self, schedule_start_time, schedule_end_time, schedule_date, invitees, user_id, room_id):
        cursor = self.conn.cursor()

        # Verify auth level and if time-slot is available
        start = '{} {}'.format(schedule_date, schedule_start_time)
        end = '{} {}'.format(schedule_date, schedule_end_time)
        query = "select count(*) from rooms natural inner join room_unavailability where room_id=%s and rooms.authorization_level <= (select authorization_level from users where user_id=%s) and ( (%s < format(%s, room_unavail_date, room_start_time)) or (%s > format(%s, room_unavail_date, room_end_time)))"
        cursor.execute(query, (room_id, user_id, end, '%s %s', start, '%s %s',))
        count = cursor.fetchone()[0]

        # if count is 0, means either auth isnt met or time-slot isn't avaibale
        if count == 0:
            return 'error'
        
        query = "insert into schedule (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id) values (%s, %s, %s, %s, %s) returning schedule_id;"
        cursor.execute(query, (schedule_start_time, schedule_end_time, schedule_date, user_id, room_id,))
        schedule_id = cursor.fetchone()[0]
        self.conn.commit()

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
