#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def average_age():
    """
    Calculates and prints the average age using the stream_user_ages generator
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    average_age()
