#!/usr/bin/python3
import mysql.connector # type: ignore
from mysql.connector import errorcode # type: ignore
import pandas as pd # type: ignore
import uuid

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # Your MySQL username
            password="password" # Your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create ALX_prodev database
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create user_data table
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )
    """
    cursor.execute(create_table_query)
    print("Table user_data created successfully")

# Insert data from CSV
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    data = pd.read_csv(csv_file)
    for _, row in data.iterrows():
        user_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, (user_id, row['name'], row['email'], row['age']))
    connection.commit()
    print("Data inserted successfully")

# Generator to stream rows
def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
