import sqlite3


conn = sqlite3.connect('climate.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_name TEXT,
        state TEXT,
        region TEXT,
        year INTEGER,
        min_temp REAL,
        max_rainfall REAL
    )
''')


data = [
    ('Melbourne Airport', 'VIC', 'Melbourne', 1970, 6.1, 105.3),
    ('Canberra', 'ACT', 'Canberra', 1982, -5.2, 89.7),
    ('Broome', 'WA', 'Broome', 1995, 9.9, 321.4),
    ('Sydney', 'NSW', 'Sydney Metro', 2001, 10.5, 142.2),
    ('Wagga Wagga', 'NSW', 'Riverina', 1988, 5.8, 80.1),
    ('Dubbo', 'NSW', 'Western NSW', 2000, 4.3, 92.3),
]

cursor.executemany('''
    INSERT INTO weather (station_name, state, region, year, min_temp, max_rainfall)
    VALUES (?, ?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()

print("数据库创建完成，测试数据已插入。")