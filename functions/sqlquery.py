import os
import sqlite3
import pandas as pd

headers = ['email','username','password']
data_url = 'users.csv'
data_table = pd.read_csv(data_url, header=None, names=headers, converters={'zip': str})

# Create a database
conn = sqlite3.connect('sqlite.db', check_same_thread=False)

conn.row_factory = sqlite3.Row

# Make a convenience function for running SQL queries
def sql_query(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def sql_edit_insert(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()

def sql_delete(query,var):
    cur = conn.cursor()
    cur.execute(query,var)

def sql_query2(query,var):
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    return rows