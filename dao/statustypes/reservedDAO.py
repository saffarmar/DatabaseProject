from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class ReservedDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllReserved(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM reserved"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addReserved(self, uid, rid, buyer):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO reserved(uid, rid, buyer) VALUES (%s, %s, %s) RETURNING pid;"
        cursor.execute(query, (uid, rid, buyer))
        pid = cursor.fetchone()['pid']
        self.conn.commit()
        cursor.close()

        return pid

    def editReserved(self, uid, rid, buyer, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE reserved SET uid=%s, rid=%s, buyer=%s pid=%s WHERE pid =%s RETURNING pid"
        cursor.execute(query, (uid, rid, buyer, pid))
        pid = cursor.fetchone()['pid']
        self.conn.commit()
        cursor.close()

        return pid

    def deleteReserved(self, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM reserved WHERE pid=%s RETURNING pid;"
        cursor.execute(query, (pid,))
        pid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return pid

    def getReservedById(self, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM reserved WHERE pid = %s;"
        cursor.execute(query, (pid,))

        result = cursor.fetchone()
        cursor.close()

        return result


