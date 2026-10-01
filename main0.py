import mysql.connector
from tabulate import tabulate

# ------------------ DATABASE CONNECTION ------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Railways"
)

# IMPORTANT: buffered cursor to avoid unread result error
mycursor = mydb.cursor(buffered=True)

mycursor.execute("CREATE DATABASE IF NOT EXISTS Railways")
mycursor.execute("USE Railways")
print("DATABASE CREATED")

# ------------------ TABLE DISPLAY FUNCTION ------------------
def show_table(cursor):
    rows = cursor.fetchall()
    if not rows:
        print("No records found.")
        return

    columns = [col[0] for col in cursor.description]

    if "Price" in columns and "Quantity" in columns:
        new_rows = []
        for row in rows:
            r = list(row)
            price = row[columns.index("Price")]
            qty = row[columns.index("Quantity")]
            r.append(price * qty)
            new_rows.append(r)
        columns.append("Total")
        rows = new_rows

    print(tabulate(rows, headers=columns, tablefmt="grid"))


# ------------------ USER TABLE ------------------
mycursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(30)
)
""")
mydb.commit()


# ------------------ MAIN PROGRAM ------------------
while True:
    print("\n1: Signup  2: Login  3: Exit")
    choice = int(input("Choose (1/2/3): "))

    # ------------------ SIGNUP ------------------
    if choice == 1:
        username = input("Enter Username: ")
        pw = input("Enter Password: ")

        try:
            mycursor.execute("INSERT INTO users VALUES (%s, %s)", (username, pw))
            mydb.commit()
            print("+++++++ SIGNUP SUCCESSFUL +++++++")
        except:
            print("USERNAME ALREADY EXISTS!")

    # ------------------ LOGIN ------------------
    elif choice == 2:
        username = input("Enter Username: ")
        pw = input("Enter Password: ")

        admin = False
        if username == "admin@rail" and pw == "admin_password@rail":
            admin = True
            print("\n+++++++ ADMIN LOGIN SUCCESSFUL +++++++\n")
        else:
            mycursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, pw)
            )
            if not mycursor.fetchone():
                print("INVALID USERNAME OR PASSWORD")
                continue
            print("\n+++++++ USER LOGIN SUCCESSFUL +++++++\n")

        print("""
============================================================
=============== INDIAN RAILWAY MANAGEMENT SYSTEM ===========
============================================================
""")

        # ------------------ CREATE TABLES ------------------
        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Trains(
            TrainNo INT PRIMARY KEY,
            TrainName VARCHAR(50),
            Source VARCHAR(40),
            Destination VARCHAR(40),
            Seats INT,
            Price INT
        )
        """)

        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Tickets(
            PassengerName VARCHAR(40),
            Phone CHAR(10),
            TrainNo INT,
            Quantity INT,
            Price INT,
            FOREIGN KEY (TrainNo) REFERENCES Trains(TrainNo)
        )
        """)

        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff(
            Name VARCHAR(40),
            Gender VARCHAR(10),
            Age INT,
            Phone CHAR(10) UNIQUE,
            Position VARCHAR(30)
        )
        """)
        mydb.commit()

        # ------------------ MAIN MENU ------------------
        while True:
            print("""
1: Add Train
2: Remove Train
3: Search Train
4: Staff Management
5: Ticket Booking / Records
6: Available Trains List
7: Total Revenue
8: Logout
""")

            op = int(input("Enter your choice: "))

            # ------------------ ADD TRAIN ------------------
            if op == 1:
                if not admin:
                    print("ADMIN ONLY OPTION!")
                    continue

                tno = int(input("Train Number: "))
                name = input("Train Name: ")
                src = input("Source: ")
                dst = input("Destination: ")
                seats = int(input("Seats: "))
                price = int(input("Price: "))

                mycursor.execute("SELECT * FROM Trains WHERE TrainNo=%s", (tno,))
                if mycursor.fetchone():
                    print("TRAIN ALREADY EXISTS!")
                else:
                    mycursor.execute(
                        "INSERT INTO Trains VALUES (%s,%s,%s,%s,%s,%s)",
                        (tno, name, src, dst, seats, price)
                    )
                    mydb.commit()
                    print("TRAIN ADDED SUCCESSFULLY!")

            # ------------------ REMOVE TRAIN ------------------
            elif op == 2:
                if not admin:
                    print("ADMIN ONLY OPTION!")
                    continue

                tno = int(input("Train No: "))
                mycursor.execute("SELECT * FROM Trains WHERE TrainNo=%s", (tno,))
                if mycursor.fetchone():
                    mycursor.execute("DELETE FROM Trains WHERE TrainNo=%s", (tno,))
                    mydb.commit()
                    print("TRAIN REMOVED!")
                else:
                    print("TRAIN NOT FOUND!")

            # ------------------ SEARCH TRAIN ------------------
            elif op == 3:
                print("1: By Train No  2: By Source  3: By Destination")
                s = int(input("Choose: "))

                if s == 1:
                    tno = int(input("Train No: "))
                    mycursor.execute("SELECT * FROM Trains WHERE TrainNo=%s", (tno,))
                elif s == 2:
                    src = input("Source: ")
                    mycursor.execute("SELECT * FROM Trains WHERE Source=%s", (src,))
                elif s == 3:
                    dst = input("Destination: ")
                    mycursor.execute("SELECT * FROM Trains WHERE Destination=%s", (dst,))
                show_table(mycursor)

            # ------------------ STAFF ------------------
            elif op == 4:
                print("1: Add Staff  2: Remove Staff  3: View Staff")
                st = int(input("Choose: "))

                if st == 1:
                    mycursor.execute(
                        "INSERT INTO Staff VALUES (%s,%s,%s,%s,%s)",
                        (
                            input("Name: "),
                            input("Gender: "),
                            int(input("Age: ")),
                            input("Phone: "),
                            input("Position: ")
                        )
                    )
                    mydb.commit()
                    print("STAFF ADDED!")

                elif st == 2:
                    name = input("Name: ")
                    mycursor.execute("DELETE FROM Staff WHERE Name=%s", (name,))
                    mydb.commit()
                    print("STAFF REMOVED!")

                elif st == 3:
                    mycursor.execute("SELECT * FROM Staff")
                    show_table(mycursor)

            # ------------------ TICKETS ------------------
            elif op == 5:
                print("1: Book Ticket  2: View Tickets  3: Reset Tickets")
                t = int(input("Choose: "))

                if t == 1:
                    pname = input("Passenger Name: ")
                    phone = input("Phone: ")
                    tno = int(input("Train No: "))

                    mycursor.execute(
                        "SELECT Seats, Price FROM Trains WHERE TrainNo=%s", (tno,)
                    )
                    data = mycursor.fetchone()
                    if not data:
                        print("TRAIN NOT FOUND!")
                        continue

                    seats, price = data
                    qty = int(input("Quantity: "))

                    if qty > seats:
                        print("NOT ENOUGH SEATS!")
                    else:
                        mycursor.execute(
                            "INSERT INTO Tickets VALUES (%s,%s,%s,%s,%s)",
                            (pname, phone, tno, qty, price)
                        )
                        mycursor.execute(
                            "UPDATE Trains SET Seats=Seats-%s WHERE TrainNo=%s",
                            (qty, tno)
                        )
                        mydb.commit()
                        print("TICKET BOOKED!")

                elif t == 2:
                    mycursor.execute("SELECT * FROM Tickets")
                    show_table(mycursor)

                elif t == 3:
                    mycursor.execute("DELETE FROM Tickets")
                    mydb.commit()
                    print("ALL TICKETS CLEARED!")

            # ------------------ TRAIN LIST ------------------
            elif op == 6:
                mycursor.execute("SELECT * FROM Trains")
                show_table(mycursor)

            # ------------------ REVENUE ------------------
            elif op == 7:
                mycursor.execute("SELECT SUM(Price * Quantity) FROM Tickets")
                result = mycursor.fetchone()
                total = result[0] if result and result[0] else 0
                print("TOTAL REVENUE:", total)

            # ------------------ LOGOUT ------------------
            elif op == 8:
                break

    elif choice == 3:
        print("GOODBYE!")
        break

    else:
        print("INVALID CHOICE!")
