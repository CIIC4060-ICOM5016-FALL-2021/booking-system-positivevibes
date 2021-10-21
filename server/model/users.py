from config.dbconfig import pg_config
import psycopg2

class UsersDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        query = "select user_id, first_name, last_name, authorization_level, user_email, user_password from users"
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, user_id):
        query = "select user_id, first_name, last_name, authorization_level, user_email, user_password from users where user_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result