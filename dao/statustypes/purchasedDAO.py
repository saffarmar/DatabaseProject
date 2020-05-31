from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class PurchasedDao:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])

        self.conn = psycopg2._connect(connection_url)

    def getAllPurchased(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM purchased"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result

    def addPurchased(self, uploader, rid, buyer):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO purchased(uploader, rid, buyer) VALUES (%s, %s, %s) RETURNING pid;"
        cursor.execute(query, (uploader, rid, buyer))
        pid = cursor.fetchone()['pid']
        self.conn.commit()
        cursor.close()

        return pid

    def editPurchased(self, uploader, rid, buyer, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "UPDATE purchased SET uploader=%s, rid=%s, buyer=%s pid=%s WHERE pid =%s RETURNING pid"
        cursor.execute(query, (uploader, rid, buyer, pid))
        pid = cursor.fetchone()['pid']
        self.conn.commit()
        cursor.close()

        return pid

    def deletePurchased(self, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "DELETE FROM purchased WHERE pid=%s RETURNING pid;"
        cursor.execute(query, (pid,))
        pid = cursor.fetchone()['rid']
        self.conn.commit()
        cursor.close()

        return pid

    def getPurchasedById(self, pid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM purchased WHERE pid = %s;"
        cursor.execute(query, (pid,))

        result = cursor.fetchone()
        cursor.close()

        return result


