import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class RequestedDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllRequested(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM requested"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addRequested(self, uploader):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO requested(uploader) VALUES (%s) RETURNING rid;"
        cursor.execute(query, ( uploader))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def editRequested(self, uploader, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE requested SET uploader=%s WHERE rid =%s RETURNING rid"
        cursor.execute(query, (uploader, rid))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def deleteRequested(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM requested WHERE rid=%s RETURNING rid;"
        cursor.execute(query, (rid,))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def getRequestedById(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM requested WHERE rid = %s;"
        cursor.execute(query, (rid,))

        result = cursor.fetchone()
        cursor.close()

        return result

    def getRequestedByResourceType(self, resource_type):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM requested WHERE resource_type = %s;"
        cursor.execute(query, (resource_type,))

        result = cursor.fetchone()
        cursor.close()

        return result