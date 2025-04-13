import psycopg2 # type: ignore
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="2955492Frybtn"
)
cur = conn.cursor()

# 1. Create Table
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    

# 2. Insert from CSV
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s);", (row[0], row[1]))
            except psycopg2.Error as e:
                print(f"Error inserting {row}: {e}")
    conn.commit()

# 3. Insert from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    try:
        cur.execute("INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s);", (name, phone))
        conn.commit()
        print("Inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")

# 4. Update data
def update_data(old_value, new_value, field='first_name'):
    if field not in ('first_name', 'phone'):
        print("Invalid field.")
        return
 # 5. Query data
def query_data(filter_by=None, value=None):
    if filter_by and value:
        cur.execute(f"SELECT * FROM PhoneBook WHERE {filter_by} = %s;", (value,))
    else:
        cur.execute("SELECT * FROM PhoneBook;")
    for row in cur.fetchall():
        print(row)
   
# 6. Delete data
def delete_data(identifier, by='first_name'):
    if by not in ('first_name', 'phone'):
        print("Invalid delete filter.")
        return
    cur.execute(f"DELETE FROM PhoneBook WHERE {by} = %s;", (identifier,))
    conn.commit()
    print("Deleted successfully.")

# Clean up
def close_connection():
    cur.close()
    conn.close()    
if __name__ == "__main__":
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Data")
        print("4. Query Data")
        print("5. Delete Data")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            insert_from_csv('phonebook.csv')
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            f = input("Field to update (first_name or phone): ")
            old = input("Old value: ")
            new = input("New value: ")
            update_data(old, new, f)
        elif choice == '4':
            f = input("Filter by (first_name or phone or leave blank): ")
            if f:
                v = input("Enter value: ")
                query_data(f, v)
            else:
                query_data()
        elif choice == '5':
            by = input("Delete by (first_name or phone): ")
            val = input("Enter value to delete: ")
            delete_data(val, by)
        elif choice == '6':
            break

    close_connection()
