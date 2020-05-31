from config.dbconfig import pg_config
import psycopg2

class SupplierDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllSuppliers(self):
        cursor = self.conn.cursor()
        query = "select * from suppliers;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierById(self, uid):
            cursor = self.conn.cursor()
            query = "select * from suppliers where uid = %s;"
            cursor.execute(query, (uid,))
            result = cursor.fetchone()
            return result

    def getResourcesBySupplierId(self, uid):
        cursor = self.conn.cursor()
        query = "select rid, uploader, type, amount, reservable, price, restime from available natural inner join suppliers natural inner join supplies where uid = %s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from suppliers WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def insert(self, name, email, username):
        cursor = self.conn.cursor()
        query = "insert into suppliers(name, email, username) values (%s, %s, %s) returning uid;"
        cursor.execute(query, (name, email, username))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid