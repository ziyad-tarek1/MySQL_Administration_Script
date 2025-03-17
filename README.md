# MySQL Administration Script

Welcome to the MySQL Administration Script! This Python-based tool allows you to manage your MySQL databases with ease. It provides a wide range of functionalities, from listing databases and tables to creating users and managing privileges. Below, you'll find a detailed guide on how to use this script, including code snippets, explanations, and examples.

![d541b959-12db-4adb-9e57-b447a19d4595](https://github.com/user-attachments/assets/a2219827-5860-4b4e-b376-4f216b769d97)


---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
   - [1. List databases with sizes](#1-list-databases-with-sizes)
   - [2. Switch database](#2-switch-database)
   - [3. Show tables](#3-show-tables)
   - [4. List tables with row counts](#4-list-tables-with-row-counts)
   - [5. Create a table](#5-create-a-table)
   - [6. Delete a table](#6-delete-a-table)
   - [7. Describe a table](#7-describe-a-table)
   - [8. Insert data into a table](#8-insert-data-into-a-table)
   - [9. Display data from a table](#9-display-data-from-a-table)
   - [10. Update data in a table](#10-update-data-in-a-table)
   - [11. Delete data from a table](#11-delete-data-from-a-table)
   - [12. Search data in a table](#12-search-data-in-a-table)
   - [13. Flexible search queries](#13-flexible-search-queries)
   - [14. Create MySQL user](#14-create-mysql-user)
   - [15. Delete MySQL user](#15-delete-mysql-user)
   - [16. Grant privileges](#16-grant-privileges)
   - [17. Revoke privileges](#17-revoke-privileges)
   - [18. Exit](#18-exit)
4. [Contributing](#contributing)
5. [License](#license)
6. [Authors](#authors)

---

## Introduction

This script is designed to simplify MySQL database management tasks. It connects to a MySQL server using credentials stored in `config.py` and provides a command-line interface (CLI) for performing various operations. The script is modular, with each function handling a specific task, making it easy to extend or modify.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ziyad-tarek1/MySQL_Administration_Script.git
   cd MySQL_Administration_Script
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed. Then, install the required MySQL connector:
   ```bash
   pip install mysql-connector-python
   ```

3. **Configure `config.py`**:
   Edit the `config.py` file to include your MySQL server credentials:
   ```python
   MYSQL_HOST = "localhost"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "your_password"
   ```

4. **Run the Script**:
   Execute the script using Python:
   ```bash
   python mysql_admin.py
   ```

---

## Usage

### 1. List Databases with Sizes

**Function**: `list_databases_with_size()`

**Description**: Lists all databases on the MySQL server along with their sizes in MB.

**Code Snippet**:
```python
def list_databases_with_size():
    try:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("\nDatabases and Sizes:")
        for db in databases:
            db_name = db[0]
            cursor.execute(f"SELECT table_schema AS 'Database', SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES WHERE table_schema = '{db_name}' GROUP BY table_schema")
            size = cursor.fetchone()
            if size:
                print(f"- {db_name}: {size[1]:.2f} MB")
            else:
                print(f"- {db_name}: 0 MB")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
```

**Usage**:
```bash
Enter your choice: 1
```

**Output**:
```
Databases and Sizes:
- db1: 12.34 MB
- db2: 0 MB
```

---

### 2. Switch Database

**Function**: `switch_database()`

**Description**: Switches to a specified database. If the database does not exist, it prompts the user to create it.

**Code Snippet**:
```python
def switch_database():
    global conn, cursor, current_db
    while True:
        try:
            new_db = input("Enter the database name to switch to: ")
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            if new_db not in databases:
                create_db = input(f"Database '{new_db}' does not exist. Do you want to create it? (yes/no): ").strip().lower()
                if create_db == 'yes':
                    cursor.execute(f"CREATE DATABASE {new_db}")
                    print(f"Database '{new_db}' created successfully!")
                else:
                    print("Switching canceled.")
                    return
            conn.database = new_db
            current_db = new_db
            print(f"Switched to database: {new_db}")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 2
Enter the database name to switch to: my_database
```

**Output**:
```
Switched to database: my_database
```

---

### 3. Show Tables

**Function**: `show_tables()`

**Description**: Lists all tables in the currently selected database.

**Code Snippet**:
```python
def show_tables():
    if not check_database_selected():
        return
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print("\nTables:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
```

**Usage**:
```bash
Enter your choice: 3
```

**Output**:
```
Tables:
- table1
- table2
```

---

### 4. List Tables with Row Counts

**Function**: `list_tables_with_row_counts()`

**Description**: Lists all tables in the current database along with the number of rows in each table.

**Code Snippet**:
```python
def list_tables_with_row_counts():
    if not check_database_selected():
        return
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print("\nTables and Row Counts:")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                print(f"- {table_name}: {row_count} rows")
        else:
            print("No tables found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
```

**Usage**:
```bash
Enter your choice: 4
```

**Output**:
```
Tables and Row Counts:
- table1: 100 rows
- table2: 50 rows
```

---

### 5. Create a Table

**Function**: `create_table()`

**Description**: Creates a new table in the current database.

**Code Snippet**:
```python
def create_table():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            columns = input("Enter columns (e.g., id INT PRIMARY KEY, name VARCHAR(255)): ")
            query = f"CREATE TABLE {table_name} ({columns})"
            cursor.execute(query)
            conn.commit()
            print(f"Table '{table_name}' created successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 5
Enter table name: users
Enter columns: id INT PRIMARY KEY, name VARCHAR(255)
```

**Output**:
```
Table 'users' created successfully!
```

---

### 6. Delete a Table

**Function**: `delete_table()`

**Description**: Deletes a table from the current database.

**Code Snippet**:
```python
def delete_table():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name to delete: ")
            query = f"DROP TABLE {table_name}"
            cursor.execute(query)
            conn.commit()
            print(f"Table '{table_name}' deleted successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 6
Enter table name to delete: users
```

**Output**:
```
Table 'users' deleted successfully!
```

---

### 7. Describe a Table

**Function**: `describe_table()`

**Description**: Displays the structure of a table.

**Code Snippet**:
```python
def describe_table():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name to describe: ")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print("\nTable Structure:")
            for column in columns:
                print(column)
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 7
Enter table name to describe: users
```

**Output**:
```
Table Structure:
('id', 'int(11)', 'NO', 'PRI', None, '')
('name', 'varchar(255)', 'YES', '', None, '')
```

---

### 8. Insert Data into a Table

**Function**: `insert_data()`

**Description**: Inserts a new row into a table.

**Code Snippet**:
```python
def insert_data():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [col[0] for col in cursor.fetchall()]
            values = []
            for col in columns:
                value = input(f"Enter value for {col}: ")
                values.append(value)
            query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(values))})"
            cursor.execute(query, values)
            conn.commit()
            print("Data inserted successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 8
Enter table name: users
Enter value for id: 1
Enter value for name: John
```

**Output**:
```
Data inserted successfully!
```

---

### 9. display Data from a Table

**Function**: `select_data()`

**Description**: Retrieves and displays all rows from a table.

**Code Snippet**:
```python
def select_data():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 9
Enter table name: users
```

**Output**:
```
(1, 'John')
(2, 'Jane')
```

---

### 10. Update Data in a Table

**Function**: `update_data()`

**Description**: Updates a row in a table based on a condition.

**Code Snippet**:
```python
def update_data():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            column = input("Enter column to update: ")
            new_value = input(f"Enter new value for {column}: ")
            condition = input(f"Enter condition (e.g., {column}=1): ")
            query = f"UPDATE {table_name} SET {column} = %s WHERE {condition}"
            cursor.execute(query, (new_value,))
            conn.commit()
            print("Data updated successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 10
Enter table name: users
Enter column to update: name
Enter new value for name: Alice
Enter condition: id=1
```

**Output**:
```
Data updated successfully!
```

---

### 11. Delete Data from a Table

**Function**: `delete_data()`

**Description**: Deletes rows from a table based on a condition.

**Code Snippet**:
```python
def delete_data():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            condition = input("Enter condition to delete (e.g., id=1): ")
            query = f"DELETE FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            conn.commit()
            print("Data deleted successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 11
Enter table name: users
Enter condition to delete: id=1
```

**Output**:
```
Data deleted successfully!
```

---

### 12. Search Data in a Table

**Function**: `search_data()`

**Description**: Searches for rows in a table based on a condition.

**Code Snippet**:
```python
def search_data():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            condition = input("Enter search condition (e.g., name='John'): ")
            query = f"SELECT * FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 12
Enter table name: users
Enter search condition: name='John'
```

**Output**:
```
(1, 'John')
```

---

### 13. Flexible Search Queries

**Function**: `flexible_search()`

**Description**: Allows for more complex search queries using SQL-like conditions.

**Code Snippet**:
```python
def flexible_search():
    if not check_database_selected():
        return
    while True:
        try:
            table_name = input("Enter table name: ")
            condition = input("Enter search condition (e.g., name LIKE '%John%'): ")
            query = f"SELECT * FROM {table_name} WHERE {condition}"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 13
Enter table name: users
Enter search condition: name LIKE '%John%'
```

**Output**:
```
(1, 'John')
(3, 'Johnny')
```

---

### 14. Create MySQL User

**Function**: `create_user()`

**Description**: Creates a new MySQL user.

**Code Snippet**:
```python
def create_user():
    while True:
        try:
            username = input("Enter new username: ")
            password = input("Enter password: ")
            host = input("Enter host (default: localhost): ") or "localhost"
            cursor.execute(f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}'")
            conn.commit()
            print(f"User '{username}' created successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 14
Enter new username: new_user
Enter password: password123
Enter host (default: localhost): localhost
```

**Output**:
```
User 'new_user' created successfully!
```

---

### 15. Delete MySQL User

**Function**: `delete_user()`

**Description**: Deletes an existing MySQL user.

**Code Snippet**:
```python
def delete_user():
    while True:
        try:
            username = input("Enter username to delete: ")
            host = input("Enter host (default: localhost): ") or "localhost"
            cursor.execute(f"DROP USER '{username}'@'{host}'")
            conn.commit()
            print(f"User '{username}' deleted successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 15
Enter username to delete: new_user
Enter host (default: localhost): localhost
```

**Output**:
```
User 'new_user' deleted successfully!
```

---

### 16. Grant Privileges

**Function**: `grant_privileges()`

**Description**: Grants privileges to a MySQL user on a specific database.

**Code Snippet**:
```python
def grant_privileges():
    while True:
        try:
            username = input("Enter username: ")
            host = input("Enter host (default: localhost): ") or "localhost"
            database = input("Enter database name: ")
            privileges = input("Enter privileges (e.g., SELECT, INSERT, UPDATE): ")
            cursor.execute(f"GRANT {privileges} ON {database}.* TO '{username}'@'{host}'")
            conn.commit()
            print(f"Privileges granted to '{username}' successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 16
Enter username: new_user
Enter host (default: localhost): localhost
Enter database name: my_database
Enter privileges: SELECT, INSERT
```

**Output**:
```
Privileges granted to 'new_user' successfully!
```

---

### 17. Revoke Privileges

**Function**: `revoke_privileges()`

**Description**: Revokes privileges from a MySQL user on a specific database.

**Code Snippet**:
```python
def revoke_privileges():
    while True:
        try:
            username = input("Enter username: ")
            host = input("Enter host (default: localhost): ") or "localhost"
            database = input("Enter database name: ")
            privileges = input("Enter privileges to revoke (e.g., SELECT, INSERT, UPDATE): ")
            cursor.execute(f"REVOKE {privileges} ON {database}.* FROM '{username}'@'{host}'")
            conn.commit()
            print(f"Privileges revoked from '{username}' successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")
```

**Usage**:
```bash
Enter your choice: 17
Enter username: new_user
Enter host (default: localhost): localhost
Enter database name: my_database
Enter privileges to revoke: SELECT
```

**Output**:
```
Privileges revoked from 'new_user' successfully!
```

---

### 18. Exit

**Function**: Exits the script.

**Usage**:
```bash
Enter your choice: 18
```

**Output**:
```
Exiting the script...
```

---

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Authors

- **Ziyad Tarek**
  - GitHub: [Ziyad Tarek](https://github.com/ziyad-tarek1)
  - Email: ziyadtarek180@gmail.com

- **Mohamed Mahmoud**
  - GitHub: [Mohamed Mahmoud](https://github.com/Mo-5054)
  - Email: mohamedmahmoud6498@gmail.com

- **Muhammed Galal Zalat**
  - GitHub: [Muhammed Galal Zalat](https://github.com/Muhammed-Zalat)
  - Email: mohmed.galal.zalat.mz@gmail.com

---

Enjoy managing your MySQL databases with this script! 😊
