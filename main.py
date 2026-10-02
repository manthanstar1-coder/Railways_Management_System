import mysql.connector as my
import tabulate as tb
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
    Coaches INT(2),
    Seats INT,
    Price INT,
    IsActive INT DEFAULT 1 
)
""")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Tickets(
    PNR INT PRIMARY KEY,
    Email varchar(50),
    TrainNo INT,
    PName varchar(50),
    PAge int(3),
    PEmail varchar(50),
    PMobile char(10),
    PGender varchar(6),
    SeatNo varchar(5),
    BookingData DATE,
    PaidAmount float,
    FOREIGN KEY (TrainNo) REFERENCES Trains(TrainNo) ON DELETE SET NULL,
    FOREIGN KEY (Email) REFERENCES Users(Email) ON DELETE SET NULL

) 
""")
mydb.commit()


class userInfo:
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

class Railways:
    
    
    def signup(self):
        data = userInfo()
        
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
            
            query = mycursor.execute(("select Email, Pass, Type, Name from users where Email = %s"),(E,))
            person = mycursor.fetchone() 
            
            if person is not None and bcrypt.checkpw(P.encode('utf-8'),person[1].encode('utf8')) and person[2] == "User":
                print(f"Welcome, {person[3]}")
                board.userDashboard()
                print("Thank you for using our program.")
                return
            
            if person is not None and bcrypt.checkpw(P.encode('utf-8'),person[1].encode('utf8')) and person[2] == "staff":
                pass
                
            else: 
                print("Incorrect Credentials / User Doesn't exist.")
            
    def searchTrain():

        print("1: By Train No\n2: By Source \n3: By Destination")
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
                
                
            
class Dashboards:
    def userDashboard(self):
        while 1:
            print("1: Search Train\n2: Ticket Booking\n3: Booked Ticket\n4: View/Update Profile\n5: Logout")
            
            choice = int(input("Choose: "))
            
            if choice == 5:
                return

            elif choice == 1:
                # user.train(tra)
                pass
                
            elif choice == 2:
                pass
                
            elif choice == 3:
                pass
                
            elif choice == 4:
                pass

       

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



