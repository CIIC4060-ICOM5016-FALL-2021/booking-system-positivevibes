from config.dbconfig import pg_config
import psycopg2

class RoomsDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = "select room_id, room_capacity, authorization_level, building_id from rooms;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = "select room_id, room_capacity, authorization_level, building_id from rooms where room_id=%s;"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def getRoomWithAuth(self, room_id, user_id):
        cursor = self.conn.cursor()
        # Verify auth and if room exists
        query = "select * from rooms where room_id = %s and rooms.authorization_level <= (select authorization_level from users where user_id=%s);"
        cursor.execute(query, (room_id, user_id,))
        auth_tuple = cursor.fetchone()
        if not auth_tuple:
            return 'error', 'error'
        
        # Get room's appointments if any
        query = "select * from room_unavailability where room_id = %s;"
        cursor.execute(query, (room_id,))
        sched_tuples = []
        for r in cursor:
            sched_tuples.append(r)
        
        return auth_tuple, sched_tuples
        
        # cursor = self.conn.cursor()
        # query = "select room_id, room_capacity, authorization_level, building_id, room_unavail_id, room_unavail_date, room_start_time, room_end_time from rooms natural inner join room_unavailability where rooms.room_id = %s and rooms.authorization_level <= ( select authorization_level from users where user_id=%s ) group by room_id, room_unavail_id"
        # cursor.execute(query, (room_id, user_id,))
        # result = []
        # for row in cursor:
        #     result.append(row)
        # if len(result) == 0:
        #     return 'error'
        # return result        

    def updateRoom(self, room_id, room_capacity, authorization_level, building_id):
        cursor = self.conn.cursor()
        query = "update rooms set room_capacity=%s, authorization_level=%s, building_id=%s where room_id=%s;"
        cursor.execute(query, (room_capacity, authorization_level, building_id, room_id))
        self.conn.commit()
        return True

    def insertRoom(self, room_capacity, authorization_level, building_id):
        cursor = self.conn.cursor()
        query = "insert into rooms (room_capacity, authorization_level, building_id) values (%s, %s, %s) returning room_id;"
        cursor.execute(query, (room_capacity, authorization_level, building_id,))
        room_id = cursor.fetchone()[0]
        self.conn.commit()
        return room_id

    def deleteRoom(self, room_id):
        cursor = self.conn.cursor()
        query = "delete from rooms where room_id=%s"
        cursor.execute(query, (room_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
