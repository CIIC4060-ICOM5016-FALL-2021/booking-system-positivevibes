from config.dbconfig import pg_config
import psycopg2

class UsersDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, authorization_level, user_email, user_password from users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, user_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, authorization_level, user_email, user_password from users where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def updateUser(self, user_id, first_name, last_name, authorization_level, user_email, user_password):
        cursor = self.conn.cursor()
        query = "update users set first_name=%s, last_name=%s, authorization_level=%s, user_email=%s, user_password=%s where user_id=%s;"
        cursor.execute(query, (first_name, last_name, authorization_level, user_email, user_password, user_id))
        self.conn.commit()
        return True

    def insertUser(self, first_name, last_name, authorization_level, user_email, user_password):
        cursor = self.conn.cursor()
        query = "insert into users (first_name, last_name, authorization_level, user_email, user_password) values (%s, %s, %s, %s, %s) returning user_id;"
        cursor.execute(query, (first_name, last_name, authorization_level, user_email, user_password,))
        user_id = cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def deleteUser(self, user_id):
        cursor = self.conn.cursor()
        query = "delete from users where user_id=%s"
        cursor.execute(query, (user_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
