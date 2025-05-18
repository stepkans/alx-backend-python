# 🌀 Python Generators - Seed Project

## 📚 About the Project

This script sets up a MySQL database and populates it with sample user data. It is the foundation for using Python generators to stream data efficiently from a database.

---

## 🎯 Objectives

- Create and initialize a MySQL database (`ALX_prodev`)
- Define the `user_data` table with fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Import data from `user_data.csv`
- Prepare the environment for generator-based streaming in later tasks

---

## 🛠 Setup Instructions

1. **Install MySQL Connector for Python**
   ```bash
   pip install mysql-connector-python

2. **Run the Seeder**


``` bash

chmod +x 0-main.py
./0-main.py
Expected Output


3. **Expected Output** 
``` bash

connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('UUID...', 'Name...', 'Email...', age), ...]

## 📁 Files 

| File            | Description                                             |
| --------------- | ------------------------------------------------------- |
| `seed.py`       | Python script to connect, create, and seed the database |
| `user_data.csv` | CSV file containing sample user data                    |
| `0-main.py`     | Script to test seeding functionality                    |
