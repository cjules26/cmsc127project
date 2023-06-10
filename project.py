import mysql.connector as mariadb 
from tabulate import tabulate
import re

print("User: root")
pword = 'neverevernever'

mariadb_connection = mariadb.connect(user ='root', password = pword, host='localhost', port='3306')

create_cursor = mariadb_connection.cursor(buffered=True)

create_cursor.execute("DROP DATABASE IF EXISTS `app`")

create_cursor.execute("CREATE DATABASE IF NOT EXISTS `app`")

create_cursor.execute("SHOW DATABASES")

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

# Execute multiple SQL statements individually
statements = [
    'INSERT INTO person VALUES("U1", "Mario", "Beatles", -100, 300, NULL);',
    'INSERT INTO person VALUES("U2", "Lea", "Smith", -30, 130, "U1");',
    'INSERT INTO person VALUES("U3", "Sophia", "Brown", -400, 500, "U1");',
    'INSERT INTO person VALUES("U4", "Daniel", "Taft", -1500, 1500, "U1");',
    'INSERT INTO person VALUES("U5", "Olivia", "Davis", 400, 0, "U1");',
    'INSERT INTO GROUPING VALUES("G1", "AAA", 8000, 2000);',
    'INSERT INTO GROUPING VALUES("G2", "BBB", 11000, 4000);',
    'INSERT INTO group_member VALUES("G1", "U1");',
    'INSERT INTO group_member VALUES("G1", "U2");',
    'INSERT INTO group_member VALUES("G2", "U5");',
    'INSERT INTO group_member VALUES("G1", "U3");',
    'INSERT INTO group_member VALUES("G2", "U4");',
    'INSERT INTO EXPENSE VALUES ("E1", 10000, "U3","U1", "2021-07-12", "2021-07-20", "U1", null);',
    'INSERT INTO EXPENSE VALUES ("E2", 20000, "U1","U2" , "2022-01-12", "2022-09-26", "U1", null);',
    'INSERT INTO EXPENSE VALUES ("E3", 1000, "U4", "U1", "2010-01-02", "2012-11-19", "U1", null);',
    'INSERT INTO EXPENSE VALUES ("E4", 1050, "U5", "U1", "2021-07-20", null, "U1", null);',
    'INSERT INTO EXPENSE VALUES ("E5", 120, "G2","U1", "2019-07-12", null, "U1","G2");',
    'INSERT INTO EXPENSE VALUES ("E6", 150, "U1","G1", "2019-07-12", null, "U1","G1");',
    'INSERT INTO EXPENSE VALUES ("E7", 150, "U1","G1", "2019-07-12", null, "U1","G1");',
    'INSERT INTO EXPENSE VALUES ("E8", 150, "U1","G2", "2019-07-12", null, "U1","G2");',
    'INSERT INTO EXPENSE VALUES ("E9", 750, "U1","G1", "2019-07-12", null, "U1","G1");',
    'INSERT INTO EXPENSE VALUES ("E10", 500, "U1","G2", "2019-07-12", null, "U1","G2");',
]

for statement in statements:
    create_cursor.execute(statement)

mariadb_connection.commit()

create_cursor.execute("SHOW TABLES")

tables = create_cursor.fetchall()

if len(tables) == 0:
    print("No tables yet")
else:
    print("TABLES:")
    for table in tables:
        print(" ", table[0])

def format_decimal(value):
    decimal_part = value % 1
    # no decimal part to print
    if decimal_part == 0:
        return "%.0f" % value
    else:
        return "%.2f" % value

## USER FUNCTIONS

def addUser():
    create_cursor.execute("SELECT COUNT(userID) FROM PERSON")
    row = create_cursor.fetchone()
    userIDcount = row[0] if row else 0
    if userIDcount == 0:
        userID = "U1"
        fName = input("Enter First Name: ")
        lName = input("Enter Last Name: ")
        moneyOwed = float(input("Enter Money Owed: "))
        moneyLent = float(input("Enter Money Lent: "))
        sql_statement = 'INSERT INTO PERSON(userId,fName,lName,moneyOwed,moneyLent) VALUES(%s,%s,%s,%s,%s)'
        insert = (userID,fName,lName,moneyOwed,moneyLent)
        create_cursor.execute(sql_statement, insert)
    else:
        userID = "U" + str(userIDcount + 1)
        fName = input("Enter First Name: ")
        lName = input("Enter Last Name: ")
        moneyOwed = float(input("Enter Money Owed: "))
        moneyLent = float(input("Enter Money Lent: "))
        borrowerId = input("Enter borrower ID: ")
        sql_statement = 'INSERT INTO PERSON VALUES(%s,%s,%s,%s,%s,%s)'
        insert = (userID,fName,lName,moneyOwed,moneyLent,borrowerId)
        create_cursor.execute(sql_statement, insert)
    print("\nSuccessfully added Person!\n")
    mariadb_connection.commit()

def updateFirstName(id):
    sql_statement = "SELECT fName FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} First Name: {result}")
    new_first_name = input("Enter new First Name: ")
    sql_statement = "UPDATE person SET fName = %s WHERE userID = %s"
    insert = (new_first_name, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSuccessfully updated {id}'s First Name!\n")

def updateLastName(id):
    sql_statement = "SELECT lName FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Last Name: {result}")
    new_last_name = input("Enter new Last Name: ")
    sql_statement = "UPDATE person SET lName = %s WHERE userID = %s"
    insert = (new_last_name, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSuccessfully updated {id}'s Last Name!\n")

def updatePersonMoneyOwed(id):
    sql_statement = "SELECT moneyOwed FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Money Owed: {result}")
    updated_money_owed = 0.0
    while True:
        try:
            updated_money_owed = float(input("Update Money Owed: "))
            break
        except:
            print("Invalid input.")
    sql_statement = "UPDATE person SET moneyOwed = %s WHERE userID = %s"
    insert = (updated_money_owed, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY OWED!\n")

def updatePersonMoneyLent(id):
    sql_statement = "SELECT moneyLent FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Money Lent: {result}")
    updated_money_lent = 0.0
    while True:
        try:
            updated_money_lent = float(input("Update Money Lent: "))
            break
        except:
            print("Invalid input.")
        
    sql_statement = "UPDATE person SET moneyLent = %s WHERE userID = %s"
    insert = (updated_money_lent, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY LENT!\n")

def showUpdatePersonMenu():
    while True:
        sql_statement = "SELECT userID FROM person"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter userID: ")
        if not re.match(r'^U\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("User ID not found!")
            return
        else:
            break

    while(True):
        print("\n****SELECT UPDATE****")
        print("[1] Update First Name")
        print("[2] Update Last Name")
        print("[3] Update Money Owed")
        print("[4] Update Money Lent")
            
        choice = input("Please enter choice: ") 

        if (choice == "1"):
            updateFirstName(id)
        elif (choice =="2"):
            updateLastName(id)
        elif (choice == "3"):
            updatePersonMoneyOwed(id)
        elif (choice == "4"):
            updatePersonMoneyLent(id)
        else:
            print("INVALID CHOICE!!")
            continue
        print()
        break

def viewAllPerson():
    sql_statement = "SELECT * FROM person"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["userID", "First Name","Last Name", "Money Owed", "Money Lent", "borrowerID"]]
    for res in result:
        person_data = [res[0], res[1], res[2], str(res[3]), str(res[4]), res[5]]
        table_data.append(person_data)
    print("CURRENT PERSONS")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def searchPerson():
    while True:
        sql_statement = "SELECT userID FROM person"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter userID: ")
        if not re.match(r'^U\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("User ID not found!")
            return
        else:
            break
        
    sql_statement = "SELECT * FROM person WHERE userID=%s"
    sql_data = (id,)
    create_cursor.execute(sql_statement, sql_data)
    person =  create_cursor.fetchone()
    print("\nVIEWING PERSON...\n")
    print(" userID:", person[0])
    print(" First Name:", person[1])
    print(" Last Name: ", person[2])
    print(" Money Owed:", format_decimal(person[3]))
    print(" Money Lent by Group:", format_decimal(person[4]))
    print(" borrowerID: ", person[5])

def userMenu():
    choice = -1
    while (choice != 0):
        print("\n**********USER MENU*********")
        print("[1] Add User")
        print("[2] Update User")
        print("[3] Delete User")
        print("[4] Search User")
        print("[5] View All Users")
        print("[0] Return\n")
        
        choice = input("Please enter choice: ")  

        if choice == "1":
            addUser()
        elif choice == "2":
            showUpdatePersonMenu()
        elif choice == "3":
            deletePerson()
        elif choice == "4":
            searchPerson()
        elif choice == "5":
            viewAllPerson()
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue


## GROUP FUNCTIONS

def addGroup():
    create_cursor.execute("SELECT COUNT(groupID) FROM GROUPING")
    row = create_cursor.fetchone()
    groupIDcount = row[0] if row else 0
    if groupIDcount == 0:
        groupID = "G1"
    else:
        groupID = "G" + str(groupIDcount + 1)

    groupName = input("Enter Group Name: ")
    moneyOwed = float(input("Enter Money Owed: "))
    moneyLent = float(input("Enter Money Lent: "))
    sql_statement = 'INSERT INTO GROUPING(groupID,groupName,moneyOwed,moneyLent) VALUES(%s,%s,%s,%s)'
    insert = (groupID,groupName,moneyOwed,moneyLent)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()

def updateGroupName(id):
    sql_statement = "SELECT groupName FROM GROUPING where groupID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Group Name: {result}")
    new_group_name = input("Enter new group name: ")
    sql_statement = "UPDATE grouping SET groupName = %s WHERE groupID = %s"
    insert = (new_group_name, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s GROUP NAME!\n")

def updateGroupMoneyOwed(id):
    sql_statement = "SELECT moneyOwed FROM GROUPING where groupID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Group Money Owed: {result}")
    updated_money_owed = 0.0
    while True:
        try:
            updated_money_owed = float(input("Update Money Owed: "))
            break
        except:
            print("Invalid input.")
    sql_statement = "UPDATE grouping SET moneyOwed = %s WHERE groupID = %s"
    insert = (updated_money_owed, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY OWED!\n")

def updateGroupMoneyLent(id):
    sql_statement = "SELECT moneyOwed FROM GROUPING where groupID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Group Money Lent: {result}")
    updated_money_lent = 0.0
    while True:
        try:
            updated_money_lent = float(input("Update Money Lent: "))
            break
        except:
            print("Invalid input.")
    sql_statement = "UPDATE grouping SET moneyLent = %s WHERE groupID = %s"
    insert = (updated_money_lent, id)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY LENT!\n")

def deletePerson():
    while True:
        sql_statement = "SELECT userID FROM person"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter userID: ")
        if not re.match(r'^U\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("User ID not found!")
            return
        else:
            break

    sql_statement = "DELETE from person where userID = %s"
    create_cursor.execute(sql_statement,(id,))
    mariadb_connection.commit()
    print("Successfully deleted!")

def showUpdateGroupMenu():
    while True:
        sql_statement = "SELECT groupID FROM grouping"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter groupID: ")
        if not re.match(r'^G\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("Group ID not found!")
            return
        else:
            break
    
    while(True):
        print("\n****SELECT UPDATE****")
        print("[1] Update Group Name")
        print("[2] Update Money Owed")
        print("[3] Update Money Lent")

        choice = input("\nPlease enter your choice: ")

        if (choice == "1"):
            updateGroupName(id)
        elif (choice == "2"):
            updateGroupMoneyOwed(id)
        elif (choice == "3"):
            updateGroupMoneyLent(id)
        else:
            print("INVALID CHOICE!!")
            continue
        break

def deleteGroup():
    while True:
        sql_statement = "SELECT groupID FROM grouping"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter groupID: ")
        if not re.match(r'^G\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("Group ID not found!")
            return
        else:
            break

    sql_statement = "SELECT groupID FROM GROUPING"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    selected_groupId = input("Enter Group ID: ")
    if (selected_groupId in list_of_ids):
        sql_statement = "DELETE from grouping where groupID = %s"
        create_cursor.execute(sql_statement, (selected_groupId,))
        mariadb_connection.commit()
    else:
        print(f"GRPUD ID {selected_groupId} was not found!")
        

def viewAllGroups():
    sql_statement = "SELECT * FROM GROUPING"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Group ID", "Group Name", "Money Owed", "Money Lent"]]
    for res in result:
        group_data = [res[0], res[1], str(res[2]), str(res[3])]
        table_data.append(group_data)
    print("\nCURRENT GROUPS")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewGroupsWithOutstandingBalance():
    sql_statement = "SELECT * FROM grouping WHERE moneyOwed>0;"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Group ID", "Group Name", "Money Owed", "Money Lent"]]
    for res in result:
        group_data = [res[0], res[1], str(res[2]), str(res[3])]
        table_data.append(group_data)
    print("\nGROUPS WITH OUTSTANDING BALANCE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    
def searchGroup():
    while True:
        sql_statement = "SELECT groupID FROM grouping"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        userIds = [item[0] for item in result]

        id = input("Enter groupID: ")
        if not re.match(r'^G\d+$', id):
            print("Invalid input")
        elif id not in userIds:
            print("Group ID not found!")
            return
        else:
            break
    
    sql_statement = "SELECT * FROM grouping WHERE groupID=%s"
    sql_data = (id,)
    create_cursor.execute(sql_statement, sql_data)
    group =  create_cursor.fetchone()

    sql_statement = "SELECT fName, lName FROM grouping NATURAL JOIN group_member JOIN person ON group_member.memberID=person.userID where groupID=%s"
    sql_data = (id,)
    create_cursor.execute(sql_statement, sql_data)
    memberNames =  create_cursor.fetchall()
    memberNames = [member[0] + ' ' + member[1] for member in memberNames]

    print("\nVIEWING GROUP...\n")
    print(" Group ID:", group[0])
    print(" Group Name:", group[1])
    print(" Money Owed by Group:", format_decimal(group[2]))
    print(" Money Lent by Group:", format_decimal(group[3]))
    print(" Group Members:", ', '.join(memberNames))

def viewExpense():
    sql_statement = "SELECT expenseID FROM EXPENSE"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    list_of_expenses = [expense[0] for expense in result]
    selected_expenseId = input("Enter Expense ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (selected_expenseId in list_of_expenses):
        sql_statement = "SELECT * from EXPENSE where expenseID = %s"
        create_cursor.execute(sql_statement, (selected_expenseId,))
        expense_info =  create_cursor.fetchone()
        table_data.append([expense_info[i] for i in range(0,len(table_data[0]))])
    else:
        print(f"EXPENSE ID {selected_expenseId} was not found!!!")
        return
    print(f"\n{selected_expenseId} EXPENSE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewAllExpenses():
    sql_statement = "SELECT * FROM EXPENSE order by length(expenseID), (substring(expenseID, length(expenseID)))"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    print(result)
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewUserExpenses():
    sql_statement = "SELECT userID FROM PERSON"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    selected_userId = input("Enter User ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (selected_userId in list_of_ids):
        sql_statement = "SELECT * FROM EXPENSE where sender = %s"
        create_cursor.execute(sql_statement, (selected_userId,))
        result = create_cursor.fetchall()
        [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    else:
        print(f"USER ID {selected_userId} was not found!!!")
        return
    print(f"\n{selected_userId}'s EXPENSES")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewGroupExpenses():
    sql_statement = "SELECT groupID FROM grouping"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    selected_groupId = input("Enter Group ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (selected_groupId in list_of_ids):
        sql_statement = "SELECT * FROM EXPENSE where sender = %s"
        create_cursor.execute(sql_statement, (selected_groupId,))
        result = create_cursor.fetchall()
        [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    else:
        print(f"GROUP ID {selected_groupId} was not found!!!")
        return
    print(f"\n{selected_groupId}'s EXPENSES")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def insertExpense():
    sql_statement = "SELECT * from EXPENSE order by length(expenseID), (substring(expenseID, length(expenseID)))"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    result = result[-1][0][1:]
    next_id =  f"E{int(result) + 1}"
    amount = int(input("Enter expense amount: "))
    sender = input("Enter expense sender ID: ")
    receiver = input("Enter expense receiver ID: ")
    dateOwed = input("Enter date owed: ")
    datePaid = "null"
    paid = input("Transaction was paid? (y/n): ") 
    if (paid == "y"):
        datePaid = input("Enter date paid: ")
    userId = "U1"
    groupID = "null"
    if (sender[0] == "G"):
        groupID = sender
    elif (receiver[0] == "G"):
        groupID = receiver
    
    if (datePaid == "null" and groupID == "null"):
        sql_statement = "INSERT INTO EXPENSE(expenseID, amount, sender, recipient, dateOwed, userID) VALUES(%s, %s, %s, %s, str_to_date(%s, '%Y-%m-%d'), %s)"
        create_cursor.execute(sql_statement, (next_id, amount, sender, receiver, dateOwed, userId,))
    elif (datePaid == "null"):
        sql_statement = "INSERT INTO EXPENSE(expenseID, amount, sender, recipient, dateOwed, userID, groupID) VALUES(%s, %s, %s, %s, str_to_date(%s, '%Y-%m-%d'), %s, %s)"
        create_cursor.execute(sql_statement, (next_id, amount, sender, receiver, dateOwed, userId, groupID,))
    elif (groupID == "null"):
        sql_statement = "INSERT INTO EXPENSE(expenseID, amount, sender, recipient, dateOwed, datePaid, userID) VALUES(%s, %s, %s, %s, str_to_date(%s, '%Y-%m-%d'), str_to_date(%s, '%Y-%m-%d'), %s)"
        create_cursor.execute(sql_statement, (next_id, amount, sender, receiver, dateOwed, datePaid, userId,))
    else:
        sql_statement = "INSERT INTO EXPENSE VALUES(%s, %s, %s, %s, str_to_date(%s, '%Y-%m-%d'), str_to_date(%s, '%Y-%m-%d'), %s, %s)"
        create_cursor.execute(sql_statement, (next_id, amount, sender, receiver, dateOwed, datePaid, userId, groupID)   )
    print("AN EXPENSE WAS INSERTED SUCCESSFULLY")


def viewCurrentBalanceFromAllExpenses():
    sql_statement = "SELECT moneyOwed FROM PERSON where userID='U1'"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Current Balance"]]

    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(f"\nMain User's Current Balance")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewExpenseMadeWithinAMonth():
    months = { "1": "January", "2": "February", "3":"March", "4":"April", "5":"May", "6":"June", "7":"July", "8":"August", "9":"September", "10":"October", "11":"November", "12":"December" }
    month = input("Enter Month in digits:")
    print(f"Month selected: {months[month]}")
    sql_statement = "SELECT* from expense where month(dateOwed) = %s"
    create_cursor.execute(sql_statement,(month,))
    result = create_cursor.fetchall()
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewUsersWithOutstandingBalance():
    sql_statement ="SELECT* from person where moneyOwed >0 and userID !='U1'"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["userID", "First Name","Last Name", "Money Owed", "Money Lent", "borrowerID"]]
    for res in result:
        person_data = [res[0], res[1], res[2], str(res[3]), str(res[4]), res[5]]
        table_data.append(person_data)
    print("CURRENT PERSON(S) WITH OUTSTANDING BALANCE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def reports():
    choice = -1
    while (choice != 0):
        print("\n**********REPORTS MENU*********")
        print("[1] View all expenses made within a month")
        print("[2] View all expenses made with a friend")
        print("[3] View all expenses made with a group")
        print("[4] View current balance from all expenses")
        print("[5] View all friends with outstanding balance")
        print("[6] View all groups")
        print("[7] View all groups with an outstanding balance")
        print("[0] Return\n")

        choice = input("Please enter choice: ")  

        if choice == "1":
            viewExpenseMadeWithinAMonth()
        elif choice == "2":
            viewUserExpenses()
        elif choice == "3":
            viewGroupExpenses()
        elif choice == "4":
            viewCurrentBalanceFromAllExpenses()
        elif choice == "5":
            viewUsersWithOutstandingBalance()
        elif choice == "6":
            viewAllGroups()
        elif choice == "7":
            viewGroupsWithOutstandingBalance()
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue

def groupMenu():
    choice = -1
    while (choice != 0):
        print("\n**********GROUP MENU*********")
        print("[1] Add Group")
        print("[2] Delete Group")
        print("[3] Search Group")
        print("[4] Update Group")
        print("[5] View All Groups")
        print("[6] View Groups with Outstanding Balance")
        print("[0] Return\n")

        choice = input("Please enter choice: ") 

        if choice == "1":
            addGroup()
        elif choice == "2":
            deleteGroup()
        elif choice == "3":
            searchGroup()
        elif choice == "4":
            showUpdateGroupMenu()
        elif choice == "5":
            viewAllGroups()
        elif choice == "6":
            viewGroupsWithOutstandingBalance()
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue


def expenseMenu():
    choice = -1
    while (choice != 0):
        print("\n**********EXPENSE MENU*********")
        print("[1] View Expense")
        print("[2] View All Expenses")
        print("[3] View User Expenses")
        print("[4] View Group Expenses")
        print("[5] Insert an expense")
        print("[6] Delete an expense")
        print("[7] Update an expense")
        print("[0] Return\n")
        
        choice = input("Please enter choice: ")

        if choice == "1":
            viewExpense()
        elif choice == "2":
            viewAllExpenses()
        elif choice == "3":
            viewUserExpenses()
        elif choice == "4":
            viewGroupExpenses()
        elif choice == "5":
            insertExpense()
        elif choice == "6":
            deleteExpense()
        elif choice == "7":
            updateExpense()
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue

def menu():
    choice = -1
    while (choice != 0):
        print("**********MENU*********")
        print("[1] User")
        print("[2] Group")
        print("[3] Expense")
        print("[4] Generate Reports")
        print("[0] Exit\n")
        
        choice = input("Please enter choice: ") 
        
        if choice == "1":
            userMenu()
        elif choice == "2":
            groupMenu()
        elif choice == "3":
            expenseMenu()
        elif choice == "4":
            reports()
        elif choice == "0":
            print()
            print("Thank you!\n")
            break
        else:
            print("Invalid Choice!!!")
            continue


menu()

create_cursor.close()   
mariadb_connection.close()