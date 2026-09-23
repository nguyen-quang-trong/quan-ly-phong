import sqlite3
from tkinter import *

conn=sqlite3.connect("data.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS thongtinmuonphong(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hoten TEXT NOT NULL,
        mssv TEXT NOT NULL,
        thoigianbd TEXT,
        thoigiankt TEXT,
        trangthai TEXT
    )
""")