import csv
import sqlite3

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)


#query = "INSERT INTO sys_command VALUES (null,'obs', 'C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe')"
#cursor.execute(query)
#conn.commit()

#query = "INSERT INTO web_command VALUES (null,'Whatsapp', 'https://web.whatsapp.com/')"
#cursor.execute(query)
#conn.commit()

#query = "DELETE FROM web_command WHERE name='whatsapp'"
#cursor.execute(query)
#conn.commit()

# testing module
#app_name = "obs"
#cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#results = cursor.fetchall()
#print(results[0][0])




#cursor.execute("DROP TABLE IF EXISTS contacts;")
#conn.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(200),
                    phone VARCHAR(255),
                    email VARCHAR(255) NULL)''')

# Read data from CSV and insert into the database
desired_columns_indices = [0, 1, 2]  # Adjust column indices if needed (e.g., name, phone, email)

with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute('''INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)''', tuple(selected_data))

# Commit changes
conn.commit()

# Insert an example record manually
query = "INSERT INTO contacts (name, phone, email) VALUES ('Amit', '9177419700', NULL)"
cursor.execute(query)
conn.commit()

# Query for contact based on name
search_name = 'Krishna'.strip().lower()  # Search term, case-insensitive

cursor.execute("SELECT phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
               ('%' + search_name + '%', search_name + '%'))
results = cursor.fetchall()

# Check if a result was found
if results:
    print(f"Phone number for {search_name}: {results[0][0]}")
else:
    print(f"No contact found with the name {search_name}")

# Close connection
conn.close()