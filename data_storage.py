import sqlite3 as sq
db="/home/jidu/PycharmProjects/hackus/user_database.db"
conn=sq.connect(database=db)


conn.execute("""create table if not exists user_data (
    slno INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT  NOT NULL,
    ph_no TEXT  NOT NULL,
    address TEXT,
    lat REAL,
    long REAL,
    postcode TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    img_name TEXT,
    img_blob BLOB,
    breadth REAL,
    length REAL,
    height REAL,
    status TEXT,
    datime DATETIME DEFAULT (datetime('now', '+5 hours', '30 minutes'))
) """)

conn.close()


def insert_data(email,ph_no,address,pic_name,a,breadth,height,length):

    with sq.connect(database="user_database.db") as conn:
        cursor=conn.cursor()
        cursor.execute("""
                      INSERT INTO user_data (email, ph_no, address, lat, long, postcode, city, state, country, img_name, img_blob, breadth, length, height,status)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                  """, (
        email, ph_no, address["display_name"], address["lat"], address["lon"], address["address"]["postcode"],address["address"]["city"], address["address"]["state"], address["address"]["country"], pic_name, a, breadth,
        length, height,"s"))
        conn.commit()



def get_data(col_name):
    with sq.connect(database=db,check_same_thread=False) as conn:
        cursor=conn.cursor()
        print(f"select {col_name}  from user_data where status = 's'")
        cursor.execute(f"select {col_name}  from user_data")
        return list(cursor.fetchall())





