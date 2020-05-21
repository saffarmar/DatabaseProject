import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class HeavyEquipmentDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllHeavyEquipment(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM heavyEquipment"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addHeavyEquipment(self, erequirement, etype, weight, age, brand):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO heavyEquipment(erequirement, etype, weight, age, brand) VALUES ( %s, %s, %s, %s, %s) RETURNING rid;"
        cursor.execute(query, (erequirement, etype, weight, age, brand))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def editHeavyEquipment(self, erequirement, etype, weight, age, brand, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE heavyEquipment SET erequirement=%s, etype=%s, weight=%s, age=%s, brand=%s, rid=%s WHERE rid =%s RETURNING rid"
        cursor.execute(query, (rid))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def deleteHeavyEquipment(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM heavyEquipment WHERE rid=%s RETURNING rid;"
        cursor.execute(query, (rid,))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def getHeavyEquipmentById(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM heavyEquipment WHERE rid = %s;"
        cursor.execute(query, (rid,))

        result = cursor.fetchone()
        cursor.close()

        return result