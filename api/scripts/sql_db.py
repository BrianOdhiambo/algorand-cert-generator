import pandas as pd
import json
import os 
import mysql.connector as mysql
from mysql.connector import Error

TRAINEE = "trainee.sql"

cwd = os.getcwd()

def DBConnect(dbName=None):
    """A function to connect to the local database and return the connection and cursor of the database
    
    Parameters
        Default: None
    
    Returns
        tuple
    """

    conn = mysql.connect(host='localhost', user='root', password='root', dbName=dbName, buffered=True)

    cur = conn.cursor()
    return conn, cur

def createDB(dbName:str) -> None:
    """Create a new database
    
    Parameters
        dbName: str

    Returns

    """

    conn, cur = DBConnect()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    conn.commit()
    cur.close()

def createTable(dbName:str, table_schema: str) -> None:
    """
    Parameters
        dbName: str

    Returns
    """
    conn, cur = DBConnect(dbName)
    fd = open(f"{cwd}/scripts/{table_schema}", "r")
    readSqlFile = fd.read()
    fd.close()

    sqlCommands = readSqlFile.split(";")

    for command in sqlCommands:
        try:
            res = cur.execute(command)
        except Exception as e:
            print(f"Command skipped: {command}")
            print(e)
    conn.commit()
    cur.close()

    return

def insert_to_table(dbName: str, json_stream: json, table_name: str) -> None:
    conn, cur = DBConnect(dbName)
    insert_data = json.dumps([json.loads(json_stream)])
    df = pd.read_json(insert_data)

    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} (trainee, email, asset, status,hashed) VALUES(%s,%s,%s,%s,%s);"""
        data = (row[0], row[1], row[2], row[3], row[4])

        try:
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error: ", e)

    print("All Data Inserted Successfully")
    return

def update_table(dbName: str, json_stream: json, table_name: str) -> None:
    conn, cur = DBConnect(dbName)
    update_data = json.dumps([json.loads(json_stream)])
    df = pd.read_json(update_data)
    for _, row in df.iterrows():
        sqlQuery = f"""UPDATE {table_name} SET asset = %s, status = %s, hashed= %s WHERE email = %s;"""
        data = (int(row[0]), str(row[1]), str(row[3]), str(row[2]))

        try:
            cur.execute(sqlQuery, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error: ", e)

    print("All Data Updated Successfully")
    return

def optin_update(dbName: str, json_stream: json, table_name: str) -> None:
    conn, cur = DBConnect(dbName)
    update_data = json.dumps([json.loads(json_stream)])
    df = pd.read_json(update_data)

    for _, row in df.iterrows():
        sqlQuery = f"""UPDATE {table_name} SET status = %s, remark = %s WHERE asset = %s;"""
        data = ((row[0]), (row[1]), (row[2]))

        try:
            cur.execute(sqlQuery, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("Error: ", e)

    print("All Data Updated Successfully")
    return

def db_get_values(dbName: str="trainee"):
    conn, cur = DBConnect(dbName)
    sqlQuery = 'SELECT * FROM trainee;'
    try:
        cur.execute(sqlQuery)
        result = cur.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    
def db_get_values_by_asset(asset:str,dbName: str="trainee"):
    conn, cur = DBConnect(dbName)
    sqlQuery = f'SELECT remark,email,hashed FROM trainee WHERE asset = {asset};'
    try:
        cur.execute(sqlQuery)
        result = cur.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("Error: ", e)  

def db_get_values_by_addr(addr:str,dbName: str="trainee"):
    conn, cur = DBConnect(dbName)
    sqlQuery = f'SELECT asset,status,hashed FROM trainee WHERE remark = {addr};'
    try:
        cur.execute(sqlQuery)
        result = cur.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("Error: ", e)