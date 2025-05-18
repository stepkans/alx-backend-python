#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator that yields one row at a time from user_data table
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password", 
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return
