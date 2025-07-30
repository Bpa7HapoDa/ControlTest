import sqlite3

class ShopDB:
    def __init__(self, path='db/shop_list.db'):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bought INTEGER DEFAULT 0
        )'''
        self.conn.execute(query)
        self.conn.commit()

    def get_items(self):
        return self.conn.execute("SELECT id, name, bought FROM items").fetchall()

    def add_item(self, name):
        cursor = self.conn.execute("INSERT INTO items (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid

    def delete_item(self, item_id):
        self.conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()

    def update_status(self, item_id, bought):
        self.conn.execute("UPDATE items SET bought = ? WHERE id = ?", (int(bought), item_id))
        self.conn.commit()
