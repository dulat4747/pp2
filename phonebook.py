import psycopg2
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    sql = ''
    try:

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="127.0.0.1",
            database="postgres",
            user="postgres",
            port="5432",
            password="Dulat2005")

        # Autocommit to database
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        #
        # # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        #create a table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_book (
                contact_name VARCHAR(255) PRIMARY KEY,
                contact_number INT NOT NULL
            )
        """)
        # Users Action
        choose = input("Choose:\n        I - Insert New Contact\n        U(1|2) - Change Contact Name(1) or Number(2)\n        Q(1|2) - Search Contact Name(1) or Number(2)\n        D(1|2) - Delete Contact Name(1) or Number(2)\n\nMY CHOICE: ")
        # Insert data
        if choose == 'I':
            sql = """INSERT INTO phone_book(contact_name, contact_number)
                     VALUES(%s,%s);"""

            cur.execute(sql,(input("Enter Contact Name: \n"), input("Enter Contact Number: \n")))
            print("Your Contact Saved Successfully!\n")
            ################################
        # if choose == 'C':
        #     cur.execute("""/copy (SELECT * FROM csv_table) to "C:\Users\lenovo\Documents\PP2\SIS\SIS10\PhoneBook\data\csv_table" with csv""")
        #     cur.execute("""COPY csv_table(contact_name, contact_number)
        #                    FROM "C:\Users\lenovo\Documents\PP2\SIS\SIS10\PhoneBook\data\csv_table"
        #                    DELIMITER ','
        #                    CSV HEADER;""")
        #     for i in cur.fetchall():
        #         print(i)
        #     file = open('data\\csv_table')
        #     contents = csv.reader(file)
        #     insert_records = "INSERT INTO phone_book(contact_name, contact_number) VALUES(?, ?)"
        #     cur.executemany(insert_records, contents)
        #     select_all = "SELECT * FROM phone_book"
        #     rows = cur.execute(select_all).fetchall()
            
        #     # Output to the console screen
        #     for r in rows:
        #         print(r)
             ######################################
        # Update Data
        elif choose == 'U1':
            change = input("Change: ")
            to = input("To: ")
            cur.execute(f"""UPDATE phone_book
            SET contact_name = '{to}' 
            WHERE contact_name = '{change}';""")
            print("Your Updating Saved Successfully!\n")

        elif choose == 'U2':
            change = input("Name: ")
            to1 = input("New Number: ")
            cur.execute(f"""UPDATE phone_book
            SET contact_number = {to1} 
            WHERE contact_name = '{change}';""")
            print("Your Updating Saved Successfully!\n")

        # Quering Data
        elif choose == 'Q1':
            n = input("Contact Name: ")
            cur.execute(f"""SELECT * FROM phone_book WHERE contact_name = '{n}';""")
            print(f"{n}'s Contact Number:", cur.fetchone()[1])

        elif choose == 'Q2':
            n = input("Contact Number: ")
            cur.execute(f"""SELECT * FROM phone_book WHERE contact_number = {n};""")
            print(f"It's {cur.fetchone()[0]}'s Contact Number")
        elif choose == 'D1':
            n = input("Contact Name: ")
            cur.execute(f"""DELETE FROM phone_book WHERE contact_name = '{n}'""")
            print("Removing Succesfully Finished!")
        elif choose == 'D2':
            n = input("Contact Number: ")
            cur.execute(f"""DELETE FROM phone_book WHERE contact_number = {n}""")
            print("Removing Succesfully Finished!")

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


if __name__ == '__main__':
    connect()