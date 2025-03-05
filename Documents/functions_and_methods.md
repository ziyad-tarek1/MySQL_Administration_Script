### 1. **Connection-Related Functions**
   - **`mysql.connector.connect()`**  
     Used to establish a connection to the MySQL server.  
     Example:
     ```python
     conn = mysql.connector.connect(host=host, user=user, password=password)
     ```

   - **`conn.database`**  
     Used to set or switch the current database.  
     Example:
     ```python
     conn.database = new_db
     ```

   - **`conn.commit()`**  
     Used to commit the current transaction (save changes to the database).  
     Example:
     ```python
     conn.commit()
     ```

   - **`conn.close()`**  
     Used to close the connection to the MySQL server.  
     Example:
     ```python
     conn.close()
     ```

---

### 2. **Cursor-Related Functions**
   - **`conn.cursor()`**  
     Used to create a cursor object for executing SQL queries.  
     Example:
     ```python
     cursor = conn.cursor()
     ```

   - **`cursor.execute()`**  
     Used to execute a SQL query.  
     Example:
     ```python
     cursor.execute("SHOW DATABASES")
     ```

   - **`cursor.fetchall()`**  
     Used to fetch all rows from the result of a query.  
     Example:
     ```python
     databases = cursor.fetchall()
     ```

   - **`cursor.fetchone()`**  
     Used to fetch a single row from the result of a query.  
     Example:
     ```python
     size = cursor.fetchone()
     ```

   - **`cursor.close()`**  
     Used to close the cursor object.  
     Example:
     ```python
     cursor.close()
     ```

---

### 3. **Error Handling**
   - **`mysql.connector.Error`**  
     Used to catch MySQL-specific errors.  
     Example:
     ```python
     except mysql.connector.Error as err:
         print(f"Error: {err}")
     ```

---

### 4. **Other Functions**
   - **`cursor.fetchall()`**  
     Used to retrieve all rows from the result of a query.  
     Example:
     ```python
     tables = cursor.fetchall()
     ```

   - **`cursor.fetchone()`**  
     Used to retrieve a single row from the result of a query.  
     Example:
     ```python
     row = cursor.fetchone()
     ```

---

### Summary of All `mysql.connector` Functions and Methods
| **Function/Method**            | **Description**                                                                 |
|--------------------------------|---------------------------------------------------------------------------------|
| `mysql.connector.connect()`    | Establishes a connection to the MySQL server.                                   |
| `conn.database`                | Sets or switches the current database.                                          |
| `conn.commit()`                | Commits the current transaction (saves changes to the database).                |
| `conn.close()`                 | Closes the connection to the MySQL server.                                      |
| `conn.cursor()`                | Creates a cursor object for executing SQL queries.                              |
| `cursor.execute()`             | Executes a SQL query.                                                           |
| `cursor.fetchall()`            | Fetches all rows from the result of a query.                                    |
| `cursor.fetchone()`            | Fetches a single row from the result of a query.                                |
| `cursor.close()`               | Closes the cursor object.                                                       |
| `mysql.connector.Error`        | Catches MySQL-specific errors.                                                  |

---

### Example Usage in The Code
Here’s how these functions and methods are used in The script:

1. **Connecting to MySQL**:
   ```python
   conn = mysql.connector.connect(host=host, user=user, password=password)
   cursor = conn.cursor()
   ```

2. **Executing a Query**:
   ```python
   cursor.execute("SHOW DATABASES")
   ```

3. **Fetching Results**:
   ```python
   databases = cursor.fetchall()
   ```

4. **Committing Changes**:
   ```python
   conn.commit()
   ```

5. **Error Handling**:
   ```python
   except mysql.connector.Error as err:
       print(f"Error: {err}")
   ```

6. **Closing Connections**:
   ```python
   cursor.close()
   conn.close()
   ```

