import mysql.connector
import csv
import os

# Global variables for connection and cursor
conn = None
cursor = None
current_db = None  # Track the currently selected database

# Function to establish connection to MySQL server
def connect_to_mysql():
    global conn, cursor
    while True:
        try:
            host = input("Enter MySQL host (default: localhost): ") or "localhost"
            user = input("Enter MySQL username: ")
            password = input("Enter MySQL password: ")

            # Connect to MySQL without specifying a database
            conn = mysql.connector.connect(host=host, user=user, password=password)
            cursor = conn.cursor()
            print("Connected to MySQL server successfully!")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your credentials and try again.")

# Function to switch or select a database
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

# Function to check if a database is selected
def check_database_selected():
    if not current_db:
        print("No database selected. Please select a database first.")
        switch_database()
        return False
    return True

# Function to list all databases with their sizes
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

# Function to show tables
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

# Function to list all tables with row counts
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

# Function to create a table
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

# Function to delete a table
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

# Function to describe a table
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

# Function to insert data
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

# Function to select data
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

# Function to update data
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

# Function to delete data
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

# Function to search data
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

# Function to show foreign key constraints and indexes
def show_foreign_keys_and_indexes():
    if not check_database_selected():
        return
    
    while True:
        try:
            table_name = input("Enter table name: ")
            cursor.execute(f"SHOW INDEX FROM {table_name}")
            indexes = cursor.fetchall()
            if indexes:
                print("\nIndexes:")
                for index in indexes:
                    print(f"- Index Name: {index[2]}, Column: {index[4]}, Unique: {index[1] == 0}")
            else:
                print("No indexes found.")

            cursor.execute(f"""
                SELECT 
                    CONSTRAINT_NAME, 
                    COLUMN_NAME, 
                    REFERENCED_TABLE_NAME, 
                    REFERENCED_COLUMN_NAME 
                FROM 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE 
                    TABLE_NAME = '{table_name}' 
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """)
            foreign_keys = cursor.fetchall()
            if foreign_keys:
                print("\nForeign Keys:")
                for fk in foreign_keys:
                    print(f"- Constraint: {fk[0]}, Column: {fk[1]}, References: {fk[2]}({fk[3]})")
            else:
                print("No foreign keys found.")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")

# Function to bulk insert data from CSV
def bulk_insert_from_csv():
    if not check_database_selected():
        return
    
    while True:
        try:
            table_name = input("Enter table name: ")
            file_path = input("Enter CSV file path: ")
            
            if not os.path.exists(file_path):
                print("File does not exist.")
                return
            
            with open(file_path, 'r') as file:
                csv_data = csv.reader(file)
                headers = next(csv_data)
                columns = ", ".join(headers)
                placeholders = ", ".join(["%s"] * len(headers))
                
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.executemany(query, csv_data)
                conn.commit()
                print(f"Inserted {cursor.rowcount} rows successfully!")
                break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")

# Function for paginated data selection
def paginated_select_data():
    if not check_database_selected():
        return
    
    while True:
        try:
            table_name = input("Enter table name: ")
            page_size = int(input("Enter page size: "))
            page_number = int(input("Enter page number: "))
            offset = (page_number - 1) * page_size
            
            query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")

# Function for flexible search queries
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

# Function to show table relationships
def show_table_relationships():
    if not check_database_selected():
        return
    
    while True:
        try:
            cursor.execute("""
                SELECT 
                    TABLE_NAME, 
                    COLUMN_NAME, 
                    CONSTRAINT_NAME, 
                    REFERENCED_TABLE_NAME, 
                    REFERENCED_COLUMN_NAME 
                FROM 
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE 
                    REFERENCED_TABLE_NAME IS NOT NULL 
                    AND TABLE_SCHEMA = DATABASE()
            """)
            relationships = cursor.fetchall()
            if relationships:
                print("\nTable Relationships:")
                for rel in relationships:
                    print(f"Table: {rel[0]}, Column: {rel[1]}, Foreign Key: {rel[2]}, References: {rel[3]}({rel[4]})")
            else:
                print("No relationships found.")
            break
        except mysql.connector.Error as err:
            print(f"Error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")

# Function to create a MySQL user
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

# Function to delete a MySQL user
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

# Function to grant privileges to a user
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

# Function to revoke privileges from a user
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

# Function to show slow queries
def show_slow_queries():
    try:
        cursor.execute("SHOW VARIABLES LIKE 'slow_query_log'")
        slow_query_log = cursor.fetchone()
        if slow_query_log and slow_query_log[1] == 'ON':
            cursor.execute("SELECT * FROM mysql.slow_log")
            slow_queries = cursor.fetchall()
            if slow_queries:
                print("\nSlow Queries:")
                for query in slow_queries:
                    print(query)
            else:
                print("No slow queries found.")
        else:
            print("Slow query log is not enabled.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to display database storage size
def display_database_storage_size():
    try:
        cursor.execute("""
            SELECT 
                table_schema AS 'Database', 
                SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' 
            FROM 
                information_schema.TABLES 
            GROUP BY 
                table_schema
        """)
        sizes = cursor.fetchall()
        if sizes:
            print("\nDatabase Storage Sizes:")
            for size in sizes:
                print(f"- {size[0]}: {size[1]:.2f} MB")
        else:
            print("No databases found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main function
def main():
    connect_to_mysql()
    while True:
        print("\nMySQL Administration Script")
        print("1. List databases with sizes")
        print("2. Switch database")
        print("3. Show tables")
        print("4. List tables with row counts")
        print("5. Create a table")
        print("6. Delete a table")
        print("7. Describe a table")
        print("8. Insert data into a table")
        print("9. Select data from a table")
        print("10. Update data in a table")
        print("11. Delete data from a table")
        print("12. Search data in a table")
        print("13. Show foreign keys and indexes")
        print("14. Bulk insert from CSV")
        print("15. Paginated data selection")
        print("16. Flexible search queries")
        print("17. Show table relationships")
        print("18. Create MySQL user")
        print("19. Delete MySQL user")
        print("20. Grant privileges")
        print("21. Revoke privileges")
        print("22. Show slow queries")
        print("23. Display database storage size")
        print("24. Exit")
       
        choice = input("Enter your choice: ")

        if choice == '1':
            list_databases_with_size()
        elif choice == '2':
            switch_database()
        elif choice == '3':
            show_tables()
        elif choice == '4':
            list_tables_with_row_counts()
        elif choice == '5':
            create_table()
        elif choice == '6':
            delete_table()
        elif choice == '7':
            describe_table()
        elif choice == '8':
            insert_data()
        elif choice == '9':
            select_data()
        elif choice == '10':
            update_data()
        elif choice == '11':
            delete_data()
        elif choice == '12':
            search_data()
        elif choice == '13':
            show_foreign_keys_and_indexes()
        elif choice == '14':
            bulk_insert_from_csv()
        elif choice == '15':
            paginated_select_data()
        elif choice == '16':
            flexible_search()
        elif choice == '17':
            show_table_relationships()
        elif choice == '18':
            create_user()
        elif choice == '19':
            delete_user()
        elif choice == '20':
            grant_privileges()
        elif choice == '21':
            revoke_privileges()
        elif choice == '22':
            show_slow_queries()
        elif choice == '23':
            display_database_storage_size()
        elif choice == '24':
            break
        else:
            print("Invalid choice! Please try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
