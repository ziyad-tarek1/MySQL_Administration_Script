# MySQL Administration Script

**A powerful Python-based CLI tool for managing MySQL databases, tables, and users.**

---

## Features

### Database Management 🗃️
- **Connect to MySQL Server**: Establish a connection to a MySQL server.
- **List Databases with Sizes**: View all databases and their sizes in MB.
- **Switch Database**: Switch to an existing database or create a new one.

### Table Management 📊
- **Show Tables**: List all tables in the current database.
- **List Tables with Row Counts**: Display tables along with their row counts.
- **Create Table**: Create a new table with specified columns.
- **Delete Table**: Delete an existing table.
- **Describe Table**: Show the structure of a table.
- **Show Foreign Keys and Indexes**: Display foreign key constraints and indexes for a table.
- **Show Table Relationships**: Display relationships between tables (foreign keys).

### Data Management 📝
- **Insert Data**: Insert data into a table.
- **Select Data**: Retrieve and display data from a table.
- **Update Data**: Update existing data in a table.
- **Delete Data**: Delete data from a table based on a condition.
- **Search Data**: Search for data in a table using a condition.
- **Bulk Insert from CSV**: Insert data from a CSV file into a table.
- **Paginated Data Selection**: Retrieve data in paginated form.
- **Flexible Search Queries**: Perform complex search queries.

### User Permissions 👤
- **Create User**: Create a new MySQL user.
- **Delete User**: Delete an existing MySQL user.
- **Grant Privileges**: Grant privileges to a user.
- **Revoke Privileges**: Revoke privileges from a user.

### Performance & Logs 📈
- **Show Slow Queries**: Display slow queries logged by MySQL.
- **Display Database Storage Size**: Show the storage size of all databases.

---

## Prerequisites

1. **Python 3.x**: Download and install Python from [python.org](https://www.python.org/).
2. **MySQL Connector/Python**: Install the MySQL connector using pip:
   ```bash
   pip install mysql-connector-python
   ```
3. **MySQL Server**: Ensure you have access to a MySQL server with the necessary credentials.

**Note**: Ensure your MySQL server is running and accessible before using this script.

---

## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ziyad-tarek1/MySQL_Administration_Script.git
   cd MySQL_Administration_Script
   ```

2. **Run the Script**:
   ```bash
   python mysql_admin_script.py
   ```

3. **Follow the Prompts**:
   - Enter your MySQL host, username, and password when prompted.
   - Use the menu to select the operation you want to perform.

**Tip**: It's recommended to run this script in a virtual environment to avoid dependency conflicts.

---

## Detailed Command Explanations

### Database Management
#### 1. List Databases with Sizes
- Displays all databases and their sizes in MB.
- Example:
  ```
  - my_database: 12.34 MB
  - test_db: 0.00 MB
  ```

#### 2. Switch Database
- Switches to an existing database or creates a new one if it doesn't exist.
- Example:
  ```
  Enter the database name to switch to: my_database
  Switched to database: my_database
  ```

### Table Management
#### 3. Show Tables
- Lists all tables in the current database.
- Example:
  ```
  - users
  - orders
  ```

#### 4. List Tables with Row Counts
- Displays tables along with their row counts.
- Example:
  ```
  - users: 100 rows
  - orders: 50 rows
  ```

#### 5. Create Table
- Creates a new table with specified columns.
- Example:
  ```
  Enter table name: products
  Enter columns (e.g., id INT PRIMARY KEY, name VARCHAR(255)): id INT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2)
  Table 'products' created successfully!
  ```

#### 6. Delete Table
- Deletes an existing table.
- Example:
  ```
  Enter table name to delete: products
  Table 'products' deleted successfully!
  ```

#### 7. Describe Table
- Shows the structure of a table.
- Example:
  ```
  Field   Type            Null    Key     Default     Extra
  id      int(11)         NO      PRI     NULL        auto_increment
  name    varchar(255)    YES             NULL
  ```

#### 8. Show Foreign Keys and Indexes
- Displays foreign key constraints and indexes for a table.
- Example:
  ```
  Indexes:
  - Index Name: PRIMARY, Column: id, Unique: True
  Foreign Keys:
  - Constraint: fk_user, Column: user_id, References: users(id)
  ```

#### 9. Show Table Relationships
- Displays relationships between tables (foreign keys).
- Example:
  ```
  Table: orders, Column: user_id, Foreign Key: fk_user, References: users(id)
  ```

### Data Management
#### 10. Insert Data
- Inserts data into a table.
- Example:
  ```
  Enter table name: users
  Enter value for id: 1
  Enter value for name: John Doe
  Enter value for email: john@example.com
  Data inserted successfully!
  ```

#### 11. Select Data
- Retrieves and displays data from a table.
- Example:
  ```
  (1, 'John Doe', 'john@example.com')
  (2, 'Jane Doe', 'jane@example.com')
  ```

#### 12. Update Data
- Updates existing data in a table.
- Example:
  ```
  Enter table name: users
  Enter column to update: name
  Enter new value for name: John Smith
  Enter condition (e.g., id=1): id=1
  Data updated successfully!
  ```

#### 13. Delete Data
- Deletes data from a table based on a condition.
- Example:
  ```
  Enter table name: users
  Enter condition to delete (e.g., id=1): id=1
  Data deleted successfully!
  ```

#### 14. Search Data
- Searches for data in a table using a condition.
- Example:
  ```
  Enter table name: users
  Enter search condition (e.g., name='John'): name LIKE '%John%'
  (1, 'John Doe', 'john@example.com')
  ```

#### 15. Bulk Insert from CSV
- Inserts data from a CSV file into a table.
- Example:
  ```
  Enter table name: users
  Enter CSV file path: users.csv
  Inserted 10 rows successfully!
  ```

#### 16. Paginated Data Selection
- Retrieves data in paginated form.
- Example:
  ```
  Enter table name: users
  Enter page size: 10
  Enter page number: 1
  (1, 'John Doe', 'john@example.com')
  (2, 'Jane Doe', 'jane@example.com')
  ```

#### 17. Flexible Search Queries
- Performs complex search queries.
- Example:
  ```
  Enter table name: users
  Enter search condition (e.g., name LIKE '%John%'): email LIKE '%example.com%' AND name LIKE '%John%'
  (1, 'John Doe', 'john@example.com')
  ```

### User Permissions
#### 18. Create User
- Creates a new MySQL user.
- Example:
  ```
  Enter new username: new_user
  Enter password: password123
  Enter host (default: localhost): localhost
  User 'new_user' created successfully!
  ```

#### 19. Delete User
- Deletes an existing MySQL user.
- Example:
  ```
  Enter username to delete: new_user
  Enter host (default: localhost): localhost
  User 'new_user' deleted successfully!
  ```

#### 20. Grant Privileges
- Grants privileges to a user.
- Example:
  ```
  Enter username: new_user
  Enter host (default: localhost): localhost
  Enter database name: my_database
  Enter privileges (e.g., SELECT, INSERT, UPDATE): SELECT, INSERT
  Privileges granted to 'new_user' successfully!
  ```

#### 21. Revoke Privileges
- Revokes privileges from a user.
- Example:
  ```
  Enter username: new_user
  Enter host (default: localhost): localhost
  Enter database name: my_database
  Enter privileges to revoke (e.g., SELECT, INSERT, UPDATE): SELECT
  Privileges revoked from 'new_user' successfully!
  ```

### Performance & Logs
#### 22. Show Slow Queries
- Displays slow queries logged by MySQL.
- Example:
  ```
  Slow Queries:
  SELECT * FROM users WHERE name LIKE '%John%'
  ```

#### 23. Display Database Storage Size
- Shows the storage size of all databases.
- Example:
  ```
  Database Storage Sizes:
  - my_database: 12.34 MB
  - test_db: 0.00 MB
  ```

---

## Complex Showcase

### Scenario: Manage a Blog Database
1. **Connect to MySQL Server**:
   - Enter host, username, and password.

2. **Create a New Database**:
   - Use option `2` to create a database named `blog_db`.

3. **Create Tables**:
   - Use option `5` to create a `users` table:
     ```
     Enter table name: users
     Enter columns: id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255), email VARCHAR(255)
     ```
   - Use option `5` to create a `posts` table:
     ```
     Enter table name: posts
     Enter columns: id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, title VARCHAR(255), content TEXT, FOREIGN KEY (user_id) REFERENCES users(id)
     ```

4. **Insert Data**:
   - Use option `8` to insert a user:
     ```
     Enter table name: users
     Enter value for id: 1
     Enter value for username: john_doe
     Enter value for email: john@example.com
     ```
   - Use option `8` to insert a post:
     ```
     Enter table name: posts
     Enter value for id: 1
     Enter value for user_id: 1
     Enter value for title: My First Post
     Enter value for content: This is the content of my first post.
     ```

5. **Show Table Relationships**:
   - Use option `17` to view relationships:
     ```
     Table: posts, Column: user_id, Foreign Key: fk_user, References: users(id)
     ```

6. **Search Data**:
   - Use option `12` to search for posts by a user:
     ```
     Enter table name: posts
     Enter search condition: user_id=1
     (1, 1, 'My First Post', 'This is the content of my first post.')
     ```

7. **Bulk Insert from CSV**:
   - Use option `14` to insert multiple posts from a CSV file.

8. **Monitor Performance**:
   - Use option `22` to view slow queries.
   - Use option `23` to check database storage size.

---

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Authors

- **ziyad-tarek1**  
  ![GitHub Avatar](https://avatars.githubusercontent.com/ziyad-tarek1)  
  GitHub: [ziyad-tarek1](https://github.com/ziyad-tarek1)  
  Email: ziyadtarek180@gmail.com

---

## Ready to Get Started?

Clone the repository and start managing your MySQL databases with ease! 🚀
