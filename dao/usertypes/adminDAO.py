import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class AdminDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllAdmin(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM admins"
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result

    def registerAdmin(self, name, email, username, password):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s) RETURNING uid;"
        cursor.execute(query, (name, email, username, password))
        uid = cursor.fetchone()['uid']
        self.conn.commit()
        cursor.close()

        return uid

    def getAdminByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from admins WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getAdminById(self, uid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from admins WHERE uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getAdminByFirstName(self, firstName):
        cursor = self.conn.cursor()
        query = "select * from admins where firstName = %s;"
        cursor.execute(query, (firstName,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getAdminByLastName(self, lastName):
        cursor = self.conn.cursor()
        query = "select * from admins where lastName = %s;"
        cursor.execute(query, (lastName,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getAdminByName(self, firstName, lastName):
        cursor = self.conn.cursor()
        query = "select * from admins where firstName = %s and lastName = %s;"
        cursor.execute(query, (firstName, lastName,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getAdminByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from admin where email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        return result

    def insert(self, name, email, username):
        cursor = self.conn.cursor()
        query = "insert into supplier(name, email, username) values (%s, %s, %s) returning uid;"
        cursor.execute(query, (name, email, username))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid
