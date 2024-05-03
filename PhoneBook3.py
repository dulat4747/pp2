import psycopg2

def search():
    n = input("Contact Name or Number: ")
    cur.execute(f"""SELECT * FROM phone_book WHERE contact_name = '{n}%' OR contact_number = '{n}%';""")
    print(cur.fetchone())

def insert():
    n = input("Enter Contact Name:\n")
    n1 = str(input("Enter Contact Number:\n"))
    cur.execute(f"""SELECT * FROM phone_book WHERE contact_name = '{n}'""")
    if cur.fetchone() is None:
        cur.execute(f"""INSERT INTO phone_book(contact_name, contact_number)
             VALUES('{n}', '{n1}');""")
        print(f"{n}'s Number Inserted Successfully!")
    else:
        b = input("User Already Exists, Do You Want To Change Number (YES|NO):\n")
        if b == 'YES':
            cur.execute(f"""UPDATE phone_book
            SET contact_number = '{n1}' 
            WHERE contact_name = '{n}';""")
            print(f"{n}'s Number Updated Successfully!")
        else:
            print(f"{n}'s Number Does Not Changed!")

def delete():
    n = input("Contact Name or Number: ")
    cur.execute(f"""DELETE FROM phone_book WHERE contact_name = '{n}' OR contact_number = '{n}'""")
    print("Removing Succesfully Finished!")

def insert_list():
    print('Important: Contact Name Should Contain No More Than 50 Symbols And Only Capital Letters,\nContact Number Must Contain 11 digits And Starts with 87.........!')
    list1 = list(map(str, input("""Insert List of Contacts:\nContact Name: Contact Number\n""").split(', ')))
    list2 = []
    for i in list1:
        list2 = list(map(str, i.split(': ')))
        if list2[0][0].isupper() and (len(list2[1]) == 11 and (list2[1][0] == '8' and list2[1][1] == '7')):
            cur.execute(f"""SELECT * FROM phone_book WHERE contact_name = '{list2[0]}'""")
            if cur.fetchone() is None:
                cur.execute(f"""INSERT INTO phone_book(contact_name, contact_number)
                     VALUES('{list2[0]}', '{list2[1]}');""")
            else:
                b = input(f"{list2[0]} Already Exists, Do You Want To Change Number (YES|NO):\n")
                if b == 'YES':
                    cur.execute(f"""UPDATE phone_book
                    SET contact_number = '{list2[1]}' 
                    WHERE contact_name = '{list2[0]}';""")
        else:
            print(f"{list2[0]} or {list2[1]} Does Not Satisfy Requirements!")
    print("Inserting New Contacts Finished!")

def query():
    l = input('Enter Limit: ')
    o = input('Enter Offset: ')
    cur.execute(f"""SELECT * FROM phone_book
                    LIMIT {l} OFFSET {o}""")
    list3 = cur.fetchall()
    for i in range(int(l)):
        print(list3[i])

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="postgres",
            port="5432",
            password="Dulat2005")

        # Autocommit to database
        conn.autocommit = True

        # create a cursor
        global cur
        cur = conn.cursor()

        # Create a table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_book (
                contact_name VARCHAR(50) PRIMARY KEY,
                contact_number VARCHAR(50) NOT NULL
            )
        """)

        # Users Action
        choose = input("Choose:\n        I - Insert New Contact or Update\n        S1|S2 - Search Contact Name or Number\n        D1|D2 - Delete Contact Name or Number\n        L - Insert List of New Contacts\n        Q - querying data\n\nMY CHOICE: ")

        # Insert data
        if choose == 'I':
            insert()

        # Quering Data By Parts
        elif choose == 'S1':
            n = input("Contact Name: ")
            cur.execute(f"""SELECT * FROM phone_book WHERE contact_name = '{n}';""")
            print(f"{n}'s Contact Number:", cur.fetchone()[1])

        elif choose == 'S2':
            n = input("Contact Number: ")
            cur.execute(f"""SELECT * FROM phone_book WHERE contact_number = {n};""")
            print(f"It's {cur.fetchone()[0]}'s Contact Number")


        # Delete Data
        elif choose == 'D1':
            delete()

        elif choose == 'D2':
            delete()

        # Insert Data From List
        elif choose == 'L':
            insert_list()

        # Querying Data By Limits And Offset
        elif choose == 'Q':
            query()

        # Close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    connect()
