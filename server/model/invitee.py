from config.dbconfig import pg_config
import psycopg2

class InviteeDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllInvitees(self):
        cursor = self.conn.cursor()
        query = "select invitee_id, user_id, schedule_id from invitee;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteeById(self, invitee_id):
        cursor = self.conn.cursor()
        query = "select invitee_id, user_id, schedule_id from invitee where invitee_id = %s;"
        cursor.execute(query, (invitee_id,))
        result = cursor.fetchone()
        return result

    def updateInvitee(self, invitee_id, user_id, schedule_id):
        cursor = self.conn.cursor()
        query = "update invitee set user_id=%s, schedule_id=%s where invitee_id=%s;"
        cursor.execute(query, (user_id, schedule_id, invitee_id,))
        self.conn.commit()
        return True

    def insertInvitee(self, user_id, schedule_id):
        cursor = self.conn.cursor()
        query = "insert into invitee (user_id, schedule_id) values (%s, %s) returning invitee_id;"
        cursor.execute(query, (user_id, schedule_id,))
        invitee_id = cursor.fetchone()[0]
        self.conn.commit()
        return invitee_id

    def deleteInvitee(self, invitee_id):
        cursor = self.conn.cursor()
        query = "delete from invitee where invitee_id=%s"
        cursor.execute(query, (invitee_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
        
