import sqlite3

class DB:

    db_name = "odoox.db"

    def __init__(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS odoox(pg_id TEXT, odoo_id TEXT)")
        con.commit()

    def get(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM odoox")
        return res.fetchone()

    def save(self, pg_id, odoo_id):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"DELETE FROM odoox")
        cur.execute(f"INSERT INTO odoox(pg_id, odoo_id) VALUES (?, ?)", (pg_id, odoo_id))
        con.commit()

    def update(self, pg_id=None, odoo_id=None):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        if pg_id:
            cur.execute(f"UPDATE odoox SET pg_id = ?", (pg_id,))
        if odoo_id:
            cur.execute(f"UPDATE odoox SET odoo_id = ?", (odoo_id,))
        con.commit()

    def remove(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(f"DELETE FROM odoox")
        con.commit()

if __name__ == '__main__':
    db = DB()
    # db.save('5a3fb9ca5ce5', '0cd5e46c7fea')
    # db.update('d4klfja')
    # db.update(odoo_id='od4klfja')
    # db.remove()
    print(db.get())
