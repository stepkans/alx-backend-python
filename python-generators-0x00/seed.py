#!/usr/bin/python3
import mysql.connector
import csv
import os
from uuid import UUID

DB_NAME = "ALX_prodev"

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists.")
    except mysql.connector.Error as err:
        print(f"Database creation error: {err}")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password", 
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Table creation error: {err}")
    cursor.close()

def insert_data(connection, file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return
    cursor = connection.cursor()
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    UUID(row['user_id'])  # validate UUID
                    cursor.execute("""
                        INSERT IGNORE INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (row['user_id'], row['name'], row['email'], row['age']))
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
        connection.commit()
        print(f"Data from {file_path} inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    cursor.close()
