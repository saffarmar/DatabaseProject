from config.dbconfig import pg_config
import psycopg2

class RequesterDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllRequesters(self):
        cursor = self.conn.cursor()
        query = "select * from requesters;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRequesterById(self, uid):
            cursor = self.conn.cursor()
            query = "select * from requesters where uid = %s;"
            cursor.execute(query, (uid,))
            result = cursor.fetchone()
            return result

    def getResourcesByRequesterId(self, uid):
        cursor = self.conn.cursor()
        query = "select rid, uploader, type, amount, restime from requested natural inner join requesters natural inner join requests where uid = %s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRequesterByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * from requesters WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def insert(self, name, email, username):
        cursor = self.conn.cursor()
        query = "insert into requesters(name, email, username) values (%s, %s, %s) returning uid;"
        cursor.execute(query, (name, email, username))
        uid = cursor.fetchone()[0]
        self.conn.commit()
        return uid