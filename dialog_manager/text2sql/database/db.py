from dialog_manager.text2sql.database.config import db_config
import pymysql as MySQLdb

class DB():
    def __init__(self):
        self.db = MySQLdb.connect(**db_config)

    def query(self, sql_query):
        cur = self.db.cursor()
        try:
            cur.execute(sql_query)
        except Exception as e:
            return str(e)
        output = ''
        
        numrows = cur.rowcount

        # Get and display one row at a time
        if numrows < 1:
            return 'Maaf! Produk yang anda cari tidak tersedia!'
        for x in range(0, numrows):
            row = cur.fetchone()
            i = 0
            for i in range(len(cur.description)):
                output += '\n'
                output += str(str(row[i]))
                # output += str(cur.description[i][0])+ str(row[i])
        return output

    def close(self):
        self.db.close()