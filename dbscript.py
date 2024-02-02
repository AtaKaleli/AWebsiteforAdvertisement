import sqlite3


def createTable(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS USER("
              "username TEXT PRIMARY KEY,"
              "password TEXT,"
              "fullname TEXT,"
              "email TEXT,"
              "telno TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS ADVERTISEMENT("
              "aid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "title TEXT,"
              "description TEXT,"
              "isactive INTEGER,"
              "cid INTEGER,"
              "username TEXT,"
              "FOREIGN KEY (cid) REFERENCES CATEGORY(cid),"
              "FOREIGN KEY (username) REFERENCES USER(usename))")


    c.execute("CREATE TABLE IF NOT EXISTS CATEGORY("
              "cid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "cname TEXT)")

    conn.commit()
    conn.close()


def insertData(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    #those are mock data of user and advertisements

    # users = [
    #     ("akaleli", "a123", "ata kaleli", "ata@example.com", "0532-123-45-67"),
    #     ("fcelik", "f123", "fatih çelik", "fatih@example.com", "0532-456-78-90")
    # ]
    #
    # advertisements = [
    #     ("tshirt", "great tshirt", 1, 1, "akaleli"),
    #     ("laptop", "great laptop", 1, 2, "akaleli"),
    #     ("tshirt", "bad  tshirt", 1, 1, "fcelik"),
    #     ("jacket", "medium jacket", 1, 1, "fcelik"),
    #     ("burger", "medium burger", 1, 3, "fcelik")
    # ]

    categories = [
        ("Clothes", ),
        ("Technology", ),
        ("Cars", ),
        ("Food", ),
        ("Drink", )
    ]


    c.executemany("INSERT INTO CATEGORY(cname) VALUES(?)", categories)
    c.executemany("INSERT INTO ADVERTISEMENT(title, description, isactive, cid, username) VALUES(?,?,?,?,?)", advertisements)
    c.executemany("INSERT INTO USER VALUES(?,?,?,?,?)", users)
    conn.commit()
    conn.close()



if __name__ =="__main__":
    createTable("advertisements.db")
    insertData("advertisements.db")








