from config.dbconfig import pg_config
import psycopg2

class BuildingDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], 
        pg_config['user'], pg_config['password'],pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    def getAllBuildings(self):
        query = "select building_id, building_abbreviation, building_name, total_rooms from building;"
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBuildingById(self, building_id):
        query = "select building_id, building_abbreviation, building_name, total_rooms from building where building_id=%s;"
        cursor = self.conn.cursor()
        cursor.execute(query, (building_id,))
        result = cursor.fetchone()
        return result

    def updateBuilding(self, building_id, building_abbreviation, building_name, total_rooms):
        cursor = self.conn.cursor()
        query = "update building set building_abbreviation=%s, building_name=%s, total_rooms=%s where building_id=%s;"
        cursor.execute(query, (building_abbreviation, building_name, total_rooms, building_id))
        self.conn.commit()
        return True

    def insertBuilding(self, building_abbreviation, building_name, total_rooms):
        cursor = self.conn.cursor()
        query = "insert into building (building_abbreviation, building_name, total_rooms) values (%s, %s, %s) returning building_id;"
        cursor.execute(query, (building_abbreviation, building_name, total_rooms,))
        building_id = cursor.fetchone()[0]
        self.conn.commit()
        return building_id

    def deleteBuilding(self, building_id):
        cursor = self.conn.cursor()
        query = "delete from building where building_id=%s"
        cursor.execute(query, (building_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0


