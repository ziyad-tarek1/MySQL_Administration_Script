import mysql.connector
import config  # Import the config module

# Global variables for connection and cursor
conn = None
cursor = None
current_db = None  # Track the currently selected database


def connect_to_mysql():
    global conn, cursor
    while True:
        try:
            # Prompt the user but use config.py values as defaults
            host = input(f"Enter MySQL host (default: {config.MYSQL_HOST}): ") or config.MYSQL_HOST
            user = input(f"Enter MySQL username (default: {config.MYSQL_USER}): ") or config.MYSQL_USER
            password = input("Enter MySQL password: ") or config.MYSQL_PASSWORD

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
        databases = cursor.fetchall()  # get the query output in the form of list of tubles 
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name to delete: ")
            if not table_name:
                print("return to the menu.")
                return
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return           
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
# Display 
def select_data():
    if not check_database_selected():
        return
    
    while True:
        try:
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return  
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return  
            column = input("Enter column to update: ")
            new_value = input(f"Enter new value for {column}: ")
            condition = input(f'Enter condition (e.g., {column}=1 , for string use {column}="name" ): ')
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return  
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
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name: ")
            if not table_name:
                print("return to the menu.")
                return
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


# Function for flexible search queries
def flexible_search():
    if not check_database_selected():
        return
    
    while True:
        try:
            print("Leave the Table name empty to return to the main menu")
            table_name = input("Enter table name : ")
            if not table_name:
                print("return to the menu.")
                return
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


# Function to create a MySQL user
def create_user():
    while True:
        response = input("Are you sure you want to create a new user? (yes/no): ").lower()
        if response in {'yes', 'y'}:       
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
        else:
            print("Creation canceled.")
            return  

# Function to delete a MySQL user
def delete_user():
    while True:
        response = input("Are you sure you want to delete a user? (yes/no): ").lower()
        if response in {'yes', 'y'}:    
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
        else:
            print("Deletion has been canceled.")
            return  

########################################################################################################
def user_exists(username, host):
    cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE user = %s AND host = %s", (username, host))
    return cursor.fetchone()[0] > 0

def database_exists(database):
    cursor.execute("SHOW DATABASES")
    return database in [db[0] for db in cursor.fetchall()]
########################################################################################################




# Function to grant privileges to a user
def grant_privileges():
    while True:
        response = input("Are you sure you want to grant privileges to a user? (yes/no): ").lower()
        if response not in {'yes', 'y'}:
            print("Operation cancelled.")
            return
        try:
            username = input("Enter username: ")
            host = input("Enter host (default: localhost): ") or "localhost"
            if not user_exists(username, host):
                print(f"Error: User '{username}' does not exist on host '{host}'.")
                continue
            database = input("Enter database name: ")
            if not database_exists(database):
                print(f"Error: Database '{database}' does not exist.")
                continue
            privileges = input("Enter privileges (e.g., SELECT, INSERT, UPDATE): ").upper()        
            confirmation = input(f"Are you sure you want to grant privileges {privileges} to {username}? (yes/no): ").lower()
            if confirmation in {'yes', 'y'}:
                cursor.execute(f"GRANT {privileges} ON {database}.* TO '{username}'@'{host}'")
                conn.commit()
                print(f"Privileges granted to '{username}' successfully!")
                break
            else:
                print("Operation cancelled.")
                return

        except mysql.connector.Error as err:
            print(f"Database error: {err}. Please check your inputs and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")


# Function to revoke privileges from a user
def revoke_privileges():
    while True:
        response = input("Are you sure you want to revoke privileges from a user? (yes/no): ").lower()
        if response in {'yes', 'y'}: 
            try:
                username = input("Enter username: ")
                host = input("Enter host (default: localhost): ") or "localhost"
                if not user_exists(username, host):
                    print(f"Error: User '{username}' does not exist on host '{host}'.")
                    continue
                database = input("Enter database name: ")
                if not database_exists(database):
                    print(f"Error: Database '{database}' does not exist.")
                    continue
                privileges = input("Enter privileges to revoke (e.g., SELECT, INSERT, UPDATE): ").upper()
                confirmation = input(f"Are you sure you want to revoke privileges {privileges} from {username}? (yes/no): ").lower()
                if confirmation in {'yes', 'y'}:
                    cursor.execute(f"REVOKE {privileges} ON {database}.* FROM '{username}'@'{host}'")
                    conn.commit()
                    print(f"Privileges revoked from '{username}' successfully!")
                    break
                else:
                    print("operation cancelled")
                    return
            except mysql.connector.Error as err:
                print(f"Error: {err}. Please check your inputs and try again.")
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")
        else:
            print("operation cancelled")
            return


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
        print("9. Display data from a table")
        print("10. Update data in a table")
        print("11. Delete data from a table")
        print("12. Search data in a table")
        print("13. Flexible search queries")
        print("14. Create MySQL user")
        print("15. Delete MySQL user")
        print("16. Grant privileges")
        print("17. Revoke privileges")
        print("18. Exit")
       
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
            flexible_search()
        elif choice == '14':
            create_user()
        elif choice == '15':
            delete_user()
        elif choice == '16':
            grant_privileges()
        elif choice == '17':
            revoke_privileges()
        elif choice == '18':
            break
        else:
            print("Invalid choice! Please try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
