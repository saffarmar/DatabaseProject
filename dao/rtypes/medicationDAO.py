import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class MedicationDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllMedications(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM medications"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addMedication(self, rid, brand, form, prescription, exdate, size):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO medications(rid, brand, form, prescription, exdate, size) VALUES (%s, %s, %s, %s, %s, %s );"
        cursor.execute(query, (rid, brand, form, prescription, exdate, size))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def editMedication(self, brand, form, prescription, exdate, size, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE medications SET brand=%s, form=%s, prescription=%s, exdate=%s, size=%s, rid=%s WHERE rid =%s RETURNING rid"
        cursor.execute(query, (rid))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def deleteMedication(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM medications WHERE rid=%s RETURNING rid;"
        cursor.execute(query, (rid,))
        rid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return rid

    def getMedicationById(self, rid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM medications WHERE rid = %s;"
        cursor.execute(query, (rid,))

        result = cursor.fetchone()
        cursor.close()

        return result