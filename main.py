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
print("DATABASE CREATED")

# Create users Table if not exist
mycursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    Email varchar(30) PRIMARY KEY,
    Name varchar(50),
    DOB char(10),
    Age int(3),
    Mobile char(10) UNIQUE,
    Gender varchar(6),
    Pass varchar(100)
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
        return Email
    
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

class Railways:
    
    
    def signup(self):
        data = userInfo()
        
        try:
            mycursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)", (data.email(), data.name(), data.dob(), data.age(), data.mobile(), data.gender(), data.passWd()))
            mydb.commit()
            print("+++++++ SIGNUP SUCCESSFUL +++++++")
            return 
        except:
            print("USERNAME ALREADY EXISTS!")
            return
    

user = Railways()

while 1:
    print("0. Exit")
    print("1. Signup")
    print("2. Login")

    choice = int(input("Choose: "))

    if choice == 0:
        break
    
    elif choice == 1:
        user.signup()