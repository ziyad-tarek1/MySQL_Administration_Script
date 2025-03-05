### 1. **Connect to MySQL Server**
   - No explicit query is executed here, but the connection is established using:
     ```python
     conn = mysql.connector.connect(host=host, user=user, password=password)
     ```

---

### 2. **List Databases**
   - Query to list all databases:
     ```sql
     SHOW DATABASES;
     ```

---

### 3. **Calculate Database Size**
   - Query to calculate the size of a specific database:
     ```sql
     SELECT table_schema AS 'Database', 
            SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' 
     FROM information_schema.TABLES 
     WHERE table_schema = 'db_name' 
     GROUP BY table_schema;
     ```

---

### 4. **Switch Database**
   - Query to switch to a specific database:
     ```python
     conn.database = new_db
     ```

   - Query to create a new database if it doesn't exist:
     ```sql
     CREATE DATABASE db_name;
     ```

---

### 5. **List Tables**
   - Query to list all tables in the current database:
     ```sql
     SHOW TABLES;
     ```

---

### 6. **List Tables with Row Counts**
   - Query to count rows in a specific table:
     ```sql
     SELECT COUNT(*) FROM table_name;
     ```

---

### 7. **Create Table**
   - Query to create a new table:
     ```sql
     CREATE TABLE table_name (column_definitions);
     ```

---

### 8. **Delete Table**
   - Query to delete a table:
     ```sql
     DROP TABLE table_name;
     ```

---

### 9. **Describe Table**
   - Query to describe the structure of a table:
     ```sql
     DESCRIBE table_name;
     ```

---

### 10. **Insert Data**
   - Query to insert data into a table:
     ```sql
     INSERT INTO table_name VALUES (value1, value2, ...);
     ```

---

### 11. **Select Data**
   - Query to select all data from a table:
     ```sql
     SELECT * FROM table_name;
     ```

---

### 12. **Update Data**
   - Query to update data in a table:
     ```sql
     UPDATE table_name SET column_name = new_value WHERE condition;
     ```

---

### 13. **Delete Data**
   - Query to delete data from a table:
     ```sql
     DELETE FROM table_name WHERE condition;
     ```

---

### 14. **Search Data**
   - Query to search for data in a table:
     ```sql
     SELECT * FROM table_name WHERE condition;
     ```

---

### 15. **Flexible Search**
   - Query to perform a flexible search:
     ```sql
     SELECT * FROM table_name WHERE condition;
     ```

---

### 16. **Create MySQL User**
   - Query to create a new MySQL user:
     ```sql
     CREATE USER 'username'@'host' IDENTIFIED BY 'password';
     ```

---

### 17. **Delete MySQL User**
   - Query to delete a MySQL user:
     ```sql
     DROP USER 'username'@'host';
     ```

---

### 18. **Grant Privileges**
   - Query to grant privileges to a user:
     ```sql
     GRANT privileges ON database_name.* TO 'username'@'host';
     ```

---

### 19. **Revoke Privileges**
   - Query to revoke privileges from a user:
     ```sql
     REVOKE privileges ON database_name.* FROM 'username'@'host';
     ```

---

### Summary of All Queries
| **Functionality**               | **Query**                                                                 |
|---------------------------------|--------------------------------------------------------------------------|
| List Databases                  | `SHOW DATABASES;`                                                        |
| Calculate Database Size         | `SELECT table_schema AS 'Database', SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES WHERE table_schema = 'db_name' GROUP BY table_schema;` |
| Create Database                 | `CREATE DATABASE db_name;`                                               |
| List Tables                     | `SHOW TABLES;`                                                           |
| Count Rows in Table             | `SELECT COUNT(*) FROM table_name;`                                       |
| Create Table                    | `CREATE TABLE table_name (column_definitions);`                          |
| Delete Table                    | `DROP TABLE table_name;`                                                 |
| Describe Table                  | `DESCRIBE table_name;`                                                   |
| Insert Data                     | `INSERT INTO table_name VALUES (value1, value2, ...);`                   |
| Select Data                     | `SELECT * FROM table_name;`                                              |
| Update Data                     | `UPDATE table_name SET column_name = new_value WHERE condition;`         |
| Delete Data                     | `DELETE FROM table_name WHERE condition;`                                |
| Search Data                     | `SELECT * FROM table_name WHERE condition;`                              |
| Flexible Search                 | `SELECT * FROM table_name WHERE condition;`                              |
| Create MySQL User               | `CREATE USER 'username'@'host' IDENTIFIED BY 'password';`                |
| Delete MySQL User               | `DROP USER 'username'@'host';`                                           |
| Grant Privileges                | `GRANT privileges ON database_name.* TO 'username'@'host';`              |
| Revoke Privileges               | `REVOKE privileges ON database_name.* FROM 'username'@'host';`           |

