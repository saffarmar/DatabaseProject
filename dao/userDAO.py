import csv
from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras

class UserDao:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                pg_config['user'],
                                                pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)


    def getAllUsers(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM users"
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result

    def registerUser(self, name, email, username, password, role_type):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO users(name, email, username, password, role_type) VALUES (%s, %s, %s, %s, %s) RETURNING uid;"
        cursor.execute(query, (name, email, username, password, role_type))
        uid = cursor.fetchone()['uid']
        self.conn.commit()
        cursor.close()

        return uid

    def getUserByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from users WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getUserById(self, uid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from users WHERE uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def getUsersByFirstName(self, firstName):
        cursor = self.conn.cursor()
        query = "select * from Users where firstName = %s;"
        cursor.execute(query, (firstName,))
        result = []

        for row in cursor:
                result.append(row)

        return result

    def getUsersByLastName(self, lastName):
        cursor = self.conn.cursor()
        query = "select * from Users where lastName = %s;"
        cursor.execute(query, (lastName,))
        result = []

        for row in cursor:
                result.append(row)

        return result

    def getUsersByName(self, firstName, lastName):
        cursor = self.conn.cursor()
        query = "select * from Users where firstName = %s and lastName = %s;"
        cursor.execute(query, (firstName,lastName,))
        result = []

        for row in cursor:
                result.append(row)

        return result

    def getUserByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select * from Users where email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        return result

    def getUserCredentials(self, uid):
        cursor = self.conn.cursor()
        query = "select * from Credentials where uid = %s;"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()

        return result

    def getUsersByRoleType(self, role_type):
        cursor = self.conn.cursor()
        query = "select * from Users where role_type = %s;"
        cursor.execute(query, (role_type,))
        result = cursor.fetchone()

        return result
