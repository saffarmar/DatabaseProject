import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class WaterDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllWater(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM water"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addWater(self, brand, exdate, size):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO water(brand, exdate, size) VALUES (%s, %s, %s) RETURNING rid;"
        cursor.execute(query, (brand, exdate, size))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def editWater(self, brand, exdate, size, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE water SET brand=%s, exdate=%s, size=%s, rid=%s WHERE rid =%s RETURNING rid"
        cursor.execute(query, (rid))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def deleteWater(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM water WHERE rid=%s RETURNING rid;"
        cursor.execute(query, (rid,))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def getWaterById(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM water WHERE rid = %s;"
        cursor.execute(query, (rid,))

        result = cursor.fetchone()
        cursor.close()

        return result