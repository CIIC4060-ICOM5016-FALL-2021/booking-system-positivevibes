from config.dbconfig import pg_config
from controllers.schedule import Schedule
import psycopg2

class UserUnavailabilityDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUnavailableUsers(self):
        cursor = self.conn.cursor()
        query = "select user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled from user_unavailability;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUnavailableUserById(self, user_unavail_id):
        cursor = self.conn.cursor()
        query = "select user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled from user_unavailability where user_unavail_id = %s;"
        cursor.execute(query, (user_unavail_id,))
        result = cursor.fetchone()
        return result

    def updateUserUnavailability(self, user_unavail_id, user_id, user_start_time, user_end_time, user_date, scheduled):
        cursor = self.conn.cursor()
        query = "update user_unavailability set user_id=%s, user_start_time=%s, user_end_time=%s, user_date=%s, scheduled=%s where user_unavail_id=%s;"
        cursor.execute(query, (user_id, user_start_time, user_end_time, user_date, scheduled, user_unavail_id,))
        self.conn.commit()
        return True

    def insertUnavailableUser(self, user_id, user_start_time, user_end_time, user_date, scheduled):
        cursor = self.conn.cursor()
        query = "insert into user_unavailability (user_id, user_start_time, user_end_time, user_date, scheduled) values (%s, %s, %s, %s, %s) returning user_unavail_id;"
        cursor.execute(query, (user_id, user_start_time, user_end_time, user_date, scheduled,))
        user_unavail_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_unavail_id

    def deleteUnavailableUser(self, user_unavail_id):
        cursor = self.conn.cursor()
        query = "select scheduled from user_unavailability where user_unavail_id = %s"
        cursor.execute(query, (user_unavail_id,))
        scheduled = cursor.fetchone()[0]
        if scheduled == 0:
            query = "delete from user_unavailability where user_unavail_id=%s"
            cursor.execute(query, (user_unavail_id,))
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows != 0
        else:
            query = "select schedule_id from (user_unavailability as uu natural inner join invitee) inner join schedule as s using (schedule_id) where uu.user_start_time = s.schedule_start_time and uu.user_end_time = s.schedule_end_time and uu.user_date = s.schedule_date and uu.user_unavail_id = %s"
            cursor.execute(query, (user_unavail_id,))
            sched_id = cursor.fetchone()[0]
            return Schedule().deleteSchedule(sched_id)
            