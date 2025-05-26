import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes


def add_item(title, description, participants, user_id, classes):
    sql = "INSERT INTO items (title, description, participants, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, participants, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_sign_up(item_id, user_id, application):
    sql = "INSERT INTO sign_ups (item_id, user_id, application) VALUES (?, ?, ?)"
    db.execute(sql, [item_id, user_id, application])

    item_id = db.last_insert_id()

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_sign_ups(item_id):
    sql = """SELECT sign_ups.id, sign_ups.application, users.id user_id, users.username
        FROM sign_ups, users
        WHERE sign_ups.item_id = ? AND sign_ups.user_id = users.id
        ORDER BY sign_ups.id"""
    return db.query(sql, [item_id])

def get_maximum_participants(item_id):
    sql = "SELECT participants FROM items WHERE id = ?"
    return int(db.query(sql, [item_id])[0][0])

def remove_sign_up(sign_up_id):
    sql = "DELETE FROM sign_ups WHERE id = ?"
    db.execute(sql, [sign_up_id])

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.participants,
                    users.username,
                    users.id user_id
                FROM items, users
                WHERE items.user_id = users.id
                AND items.id =?
            """
    result = db.query(sql, [item_id])
    return result[0] if result else None

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def update_item(item_id, title, description, classes):
    sql = """UPDATE items SET title = ?,
                            description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def remove_item(item_id):
    sql = "DELETE FROM sign_ups WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
            FROM items
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])