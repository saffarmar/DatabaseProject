import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class AvailableDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllAvailable(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM available"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result



    def addAvailable(self, rid, uploader, amount, price, restime):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO available(rid, uploader, amount, price, restime) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, (rid, uploader,amount, price, restime))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def editAvailable(self, uploader, amount, price, restime, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE available SET uploader=%s, amount=%s, price=%s, restime=%s WHERE rid =%s RETURNING rid"
        cursor.execute(query, (uploader, amount, price, restime, rid))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def deleteAvailable(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM available WHERE rid=%s RETURNING rid;"
        cursor.execute(query, (rid,))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def getAvailableById(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM available WHERE rid = %s;"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getAvailableByResourceType(self, resource_type):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM available WHERE = %s;"
        cursor.execute(query, (resource_type,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getSupplierByPartId(self, rid):
        cursor = self.conn.cursor()
        query = "select uid, name, email, username from available natural inner join supplier natural inner join supplies where rid = %s;"
        cursor.execute(query, (rid,))
        result = []
        for row in cursor:
            result.append(row)
        return result