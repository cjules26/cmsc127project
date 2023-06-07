import mysql.connector as mariadb 

mariadb_connection = mariadb.connect(user ='root', password ='mariadb26', host='localhost', port='3306')

create_cursor =mariadb_connection.cursor()

create_cursor.execute("DROP DATABASE IF EXISTS `app`")
create_cursor.execute("CREATE DATABASE IF NOT EXISTS `app`")

create_cursor.execute("SHOW DATABASES")

for x in create_cursor:
    print(x)

create_cursor.execute("USE app")

create_cursor.execute("CREATE TABLE PERSON (userID VARCHAR(4) NOT NULL,fName VARCHAR(30), lName VARCHAR(30),moneyOwed DECIMAL(8, 2),moneyLent DECIMAL(8, 2),borrowerId_fk VARCHAR(4),PRIMARY KEY (userID),CONSTRAINT borrower_user FOREIGN KEY (borrowerId_fk) REFERENCES PERSON(userID))")

create_cursor.execute("CREATE TABLE GROUPING (groupID VARCHAR(4) NOT NULL, groupName VARCHAR (30), moneyOwed DECIMAL(8,2), moneyLent DECIMAL(8,2),PRIMARY KEY (groupID))")

create_cursor.execute("CREATE TABLE GROUP_MEMBER(groupID VARCHAR(4) NOT NULL, memberID VARCHAR(4) NOT NULL, PRIMARY KEY(groupID, memberID))")

create_cursor.execute("CREATE TABLE EXPENSE(expenseID VARCHAR(6) NOT NULL, amount DECIMAL(8,2), sender VARCHAR(4), recipient VARCHAR(4), dateOwed DATE, datePaid DATE, userID VARCHAR(4), groupID VARCHAR(4), PRIMARY KEY(expenseID), CONSTRAINT deptfk FOREIGN KEY (userID) references PERSON(userID), CONSTRAINT groupfk FOREIGN KEY (groupID) references GROUPING(groupID))")


name = input("What is your name?")