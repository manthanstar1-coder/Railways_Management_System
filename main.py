import mysql.connector as my
from tabulate import tabulate as tb
import datetime as dt
import bcrypt

# ------------------ DATABASE CONNECTION ------------------
mydb = my.connect(
    host="localhost",
    user="root",
    password="root",
)

# IMPORTANT: buffered cursor to avoid unread result error
mycursor = mydb.cursor(buffered=True)

mycursor.execute("CREATE DATABASE IF NOT EXISTS Railways")
mycursor.execute("USE Railways")

# Create users Table if not exist
mycursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    Email varchar(50) PRIMARY KEY,
    Name varchar(50),
    DOB char(10),
    Age int(3),
    Mobile char(10) UNIQUE,
    Gender varchar(6),
    Pass varchar(255),
    Type varchar(10),
    Position VARCHAR(30),
    Salary float,
    DOJ Date
)
""")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Trains(
    TrainNo INT PRIMARY KEY,
    TrainName VARCHAR(50),
    Source VARCHAR(40),
    Destination VARCHAR(40),
    Coaches INT,
    TotalSeats INT,
    Price INT,
    IsActive INT 
    
)
""")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Tickets(
    PNR INT PRIMARY KEY,
    Email varchar(50),
    TrainNo INT,
    PName varchar(50),
    PAge int(3),
    PMobile char(10),
    PGender varchar(6),
    BookedSeats INT,

    BoardingStation varchar(40),
    DestinationStation varchar(40),

    SeatNo varchar(20),
    BookingDate DATE,
    PaidAmount float,
    FOREIGN KEY (TrainNo) REFERENCES Trains(TrainNo) ON DELETE SET NULL,
    FOREIGN KEY (Email) REFERENCES Users(Email) ON DELETE SET NULL
) 
""")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Route(
    RouteID INT AUTO_INCREMENT PRIMARY KEY,
    TrainNo INT,
    StationName VARCHAR(50),
    StopNo INT,
    ArrivalTime TIME,
    DepartureTime TIME,

    FOREIGN KEY (TrainNo) REFERENCES Trains(TrainNo) ON DELETE SET NULL
)
""")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Fare(
    FareID INT AUTO_INCREMENT PRIMARY KEY,
    TrainNo INT,
    FromStation VARCHAR(50),
    ToStation VARCHAR(50),
    FareAmount FLOAT,

    FOREIGN KEY (TrainNo)
    REFERENCES Trains(TrainNo)
    ON DELETE SET NULL
)
""")
mydb.commit()

def show_table(cursor):
    rows = cursor.fetchall()
    if not rows:
        print("No records found.")
        return

    columns = [col[0] for col in cursor.description]
    print(tb(rows, headers=columns, tablefmt="grid"))
    return rows


class getInfo:
    def name(self):
        Name = input("Enter Name: ")
        return Name
    
    def dob(self):
        print("Date of Birth")
        self.day = int(input("Day: "))
        self.month = int(input("Month (in numeric): "))
        self.year = int(input("Year: "))
        return f"{self.day}/{self.month}/{self.year}"

    def age(self):
        diff = dt.datetime.now() - dt.datetime(self.year, self.month, self.day)
        Age =  diff.days // 365
        return Age
    
    def gender(self):
        while 1:
            Gender = input("Gender (M/F): ")
            if Gender.lower() == 'm':
                return "MALE"
            elif Gender.lower() == 'f':
                return "FEMALE"
            else:
                print("Invalid input.")
                
    def mobile(self):
        while 1:
            num = input("Mobile No.: ")
            if len(num) != 10 or not num.isdigit():
                print("Enter Valid Number")
            else:
                return num
    
    def email(self):
        Email = input("Enter Email: ")
        return Email.lower()
    
    def passWd(self):
        passwd = input("Create Password: ")
        repasswd = input("Confirm Password: ")
        
        if passwd == repasswd:
            hPin = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt()) # Hash PIN
            return hPin.decode('utf-8')

        else:
            print("Password didn't Match")
            print("Please enter valid password")
            return self.passWd()
    
    def doj(self):
        td = dt.date.today().strftime('%Y-%m-%d')
        return td
    
    def trainNo(self):
        tno = int(input("Train Number: "))
        return tno

    def trainName(self):
        name = input("Train Name: ")
        return name

    def trainSrc(self):
        src = input("Source: ")
        return src

    def trainDst(self):
        dst = input("Destination: ")
        return dst

    def trainCoaches(self):
        Coaches = int(input("Coaches: "))
        return Coaches

    def trainSeats(self):
        seats = int(input("Seats: "))
        return seats

    def ticketPrice(self):
        price = int(input("Price: "))
        return price
    def avlseats(self,trainNo):
      

        mycursor.execute("SELECT TotalSeats FROM Trains WHERE TrainNo=%s",(trainNo,))
        total = mycursor.fetchone()[0]

        mycursor.execute(("SELECT COALESCE(SUM(BookedSeats),0) FROM Tickets WHERE TrainNo=%s"),(trainNo,))

        booked = mycursor.fetchone()[0]

        return (total - booked)
    

class Railways:
    
    def signup(self):
        data = getInfo()
        
        try:
            mycursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (data.email(), data.name(), data.dob(), data.age(), data.mobile(), data.gender(), data.passWd(), "User", None, None, data.doj()))
            mydb.commit()
            print("+++++++ SIGNUP SUCCESSFUL +++++++")
            return 
        except:
            print("USERNAME ALREADY EXISTS!")
            return

    def login(self):
        while 1:
            E = input("Enter Email: ")
            P = input("Enter Pass: ")
            
            mycursor.execute(("select Email, Pass, Type, Name from users where Email = %s"),(E,))
            person = mycursor.fetchone() 
            
            if person and bcrypt.checkpw(P.encode('utf-8'),person[1].encode('utf8')) and person[2] == "User":
                print(f"Welcome, {person[3]}")
                board.userDashboard()
                print("Thank you for using our program.")
                return
            
            elif person and bcrypt.checkpw(P.encode('utf-8'),person[1].encode('utf8')) and person[2] == "staff":
                print(f"Welcome, {person[3]}")
                board.staffdashboard()
                print("Thank you for using our program.")
                return
            
            elif person and bcrypt.checkpw(P.encode('utf-8'),person[1].encode('utf-8')) and person[2] == 'admin':
                print(f"Welcome, {person[3]}")
                board.adminDashboard()
                print("Thank you for using our program.")
                return
                
            else: 
                print("Incorrect Credentials / User Doesn't exist.")
                
                
    def addTrain(self):
        
        
        tnum = data.trainNo()
        
        mycursor.execute(("SELECT * FROM Trains WHERE TrainNo=%s"), (tnum,))
        if mycursor.fetchone():
            print("TRAIN ALREADY EXISTS!")
        
        else:
            mycursor.execute("INSERT INTO Trains VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(tnum, data.trainName(), data.trainSrc(), data.trainDst(), data.trainCoaches(), data.trainSeats(), data.ticketPrice(), 1))
            mydb.commit()
            print("TRAIN ADDED SUCCESSFULLY!")
            
        return
    
            
    def searchTrain(self):

        while 1:
            print("1: By Train No\n2: By Source \n3: By Destination\n0: Exit")
        
            s = int(input("Choose: "))

            if s == 1:
                tno = int(input("Train No: "))
                mycursor.execute(("SELECT TrainNo, TrainName, Source, Destination, Coaches, TotalSeats, Price FROM Trains WHERE TrainNo = %s and isactive = 1"), (tno,))
                
                
            elif s == 2:
                src = input("Source: ")
                mycursor.execute(("SELECT TrainNo, TrainName, Source, Destination, Coaches, TotalSeats, Price FROM Trains WHERE Source = %s and isactive = 1"), (src,))
                
            elif s == 3:
                dst = input("Destination: ")
                mycursor.execute(("SELECT TrainNo, TrainName, Source, Destination, Coaches, TotalSeats, Price FROM Trains WHERE Destination = %s and isactive = 1"), (dst,))

            
            else:
                print("Invalid Input")
                
            rows = mycursor.fetchall()

            if not rows:
                print("No records found.")
                return

           
            elif rows:
                new_rows = []
                columns = [col[0] for col in mycursor.description]
                columns.append("Available Seats")
                for row in rows:
                    
                    row = list(row)
                    row.append(data.avlseats(row[0]))   # row[0] = TrainNo
                    new_rows.append(row)
                
                print(tb(new_rows, headers=columns, tablefmt="grid"))
                return

class Dashboards:
    def userDashboard(self):
        while 1:
            print("1: Search Train\n2: Ticket Booking\n3: Booked Ticket\n4: View/Update Profile\n5: Logout")
            
            choice = int(input("Choose: "))
            
            if choice == 5:
                return

            elif choice == 1:
                user.searchTrain()
                
            elif choice == 2:
                pass
                
            elif choice == 3:
                pass
                
            elif choice == 4:
                pass
            
            else:
                print("Invalid Input")
                
            
    def staffdashboard(self):    
        print("1: Add Train\n2: Remove Train\n3: Search Train\n4: Ticket Booking / Records\n5: Available Trains List\n6: Logout")
        choice = int(input("Choose: "))
        
        if choice == 6:
            return
        
        elif choice == 1:
            user.addTrain()
            pass
            
        elif choice == 2:
            pass
            
        elif choice == 3:
            user.searchTrain()
            
        elif choice == 4:
            pass
    
    
    def adminDashboard(self):
        print("1: Add Train\n2: Remove Train\n3: Search Train\n4: Staff Management\n5: Ticket Booking / Records\n6: Available Trains List\n7: Total Revenue\n8: Logout")
        choice = int(input("Choose: "))

        if choice == 8:
            return

        elif choice == 1:
            user.addTrain()
            
        elif choice == 2:
            user.removetrain()
            
        elif choice == 3:
            user.searchTrain()
            return
            
        elif choice == 4:
            pass
       
data = getInfo()
user = Railways()
board = Dashboards()
    
while 1:
    print("0. Exit")
    print("1. Signup")
    print("2. Login")

    choice = int(input("Choose: "))

    if choice == 0:
        break
    
    elif choice == 1:
        user.signup()
    
    elif choice == 2:
        user.login()
        
    else:
        print("Invalid Input")



