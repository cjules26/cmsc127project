import mysql.connector as mariadb 

mariadb_connection = mariadb.connect(user ='root', password ='mariadb26', host='localhost', port='3306')

create_cursor = mariadb_connection.cursor(buffered=True)

create_cursor.execute("DROP DATABASE IF EXISTS `app`")

create_cursor.execute("CREATE DATABASE IF NOT EXISTS `app`")

create_cursor.execute("SHOW DATABASES")

databases = create_cursor.fetchall()

print("DATABASES:")
for database in databases:
    print(" ", database[0])

create_cursor.execute("USE app")

create_cursor.execute("""CREATE TABLE PERSON (
    userID VARCHAR(4) NOT NULL,
    fName VARCHAR(30), 
    lName VARCHAR(30),
    moneyOwed DECIMAL(8, 2),
    moneyLent DECIMAL(8, 2),
    borrowerId_fk VARCHAR(4),
    PRIMARY KEY (userID),
    CONSTRAINT borrower_user 
    FOREIGN KEY (borrowerId_fk) 
    REFERENCES PERSON(userID))""")

create_cursor.execute("""CREATE TABLE GROUPING (
    groupID VARCHAR(4) NOT NULL, 
    groupName VARCHAR (30), 
    moneyOwed DECIMAL(8,2), 
    moneyLent DECIMAL(8,2),
    PRIMARY KEY (groupID))""")

create_cursor.execute("""CREATE TABLE GROUP_MEMBER(
    groupID VARCHAR(4) NOT NULL, 
    memberID VARCHAR(4) NOT NULL, 
    PRIMARY KEY(groupID, memberID))""")

create_cursor.execute("""CREATE TABLE EXPENSE(
    expenseID VARCHAR(6) NOT NULL, 
    amount DECIMAL(8,2), 
    sender VARCHAR(4), 
    recipient VARCHAR(4), 
    dateOwed DATE, 
    datePaid DATE, 
    userID VARCHAR(4), 
    groupID VARCHAR(4), 
    PRIMARY KEY(expenseID), 
    CONSTRAINT deptfk FOREIGN KEY (userID) references PERSON(userID), 
    CONSTRAINT groupfk FOREIGN KEY (groupID) references GROUPING(groupID))""")

create_cursor.execute("SHOW TABLES")

tables = create_cursor.fetchall()

if len(tables) == 0:
    print("No tables yet")
else:
    print("TABLES:")
    for table in tables:
        print(" ", table[0])

def addUser():
    create_cursor.execute("SELECT COUNT(userID) FROM PERSON")
    row = create_cursor.fetchone()
    userIDcount = row[0] if row else 0
    if userIDcount == 0:
        userID = "U1"
    else:
        userID = "U" + str(userIDcount + 1)
        
    fName = input("Enter First Name: ")
    lName = input("Enter Last Name: ")
    moneyOwed = float(input("Enter Money Owed: "))
    moneyLent = float(input("Enter Money Lent: "))
    sql_statement = 'INSERT INTO PERSON(userId,fName,lName,moneyOwed,moneyLent) VALUES(%s,%s,%s,%s,%s)'
    insert = (userID,fName,lName,moneyOwed,moneyLent)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()

def userMenu():
    choice = -1
    while (choice != 0):
        print("\n**********USER MENU*********")
        print("[1] Add User")
        print("[2] Update User")
        print("[3] Delete User")
        print("[4] Update User")
        print("[0] Return\n")
        choice = int(input("Please enter choice: "))
        if choice == 1:
            print(1)
            addUser()
        elif choice == 2:
            print("2")
        elif choice == 3:
            print("3")
        elif choice == 4:
            print()
        elif choice == 0:
            print()
        else:
            print("Invalid Choice!!!")

def menu():
    choice = -1
    while (choice != 0):
        print("**********MENU*********")
        print("[1] User")
        print("[2] Group")
        print("[3] Expense")
        print("[0] Exit\n")
        choice = int(input("Please enter choice: "))
        if choice == 1:
            userMenu()
        elif choice == 2:
            print("2")
        elif choice == 3:
            print("3")
        elif choice == 0:
            print("Thank you!")
        else:
            print("Invalid Choice!!!")


menu()

create_cursor.close()   
mariadb_connection.close()