import mysql.connector as mariadb 
from tabulate import tabulate
import re
import general_queries as gq
import person as p

print("User: root")
pword = input("Enter password: ")

mariadb_connection = mariadb.connect(user ='root', password = pword, host='localhost', port='3306')

create_cursor = mariadb_connection.cursor(buffered=True)

create_cursor_commit = mariadb_connection.commit()

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
    'INSERT INTO person VALUES("U1", "Mario", "Beatles", 600, 0, NULL);',
    'INSERT INTO person VALUES("U2", "Lea", "Smith", 0, 100, "U1");',
    'INSERT INTO person VALUES("U3", "Sophia", "Brown", 0, 100, "U1");',
    'INSERT INTO person VALUES("U4", "Daniel", "Taft", 0, 100, "U1");',
    'INSERT INTO person VALUES("U5", "Olivia", "Davis", 0, 100, "U1");',
    'INSERT INTO GROUPING VALUES("G1", "AAA", 0, 100);',
    'INSERT INTO GROUPING VALUES("G2", "BBB", 0, 100);',
    'INSERT INTO EXPENSE VALUES ("E1", 100, "U2","U1", "2021-07-12", null, "U2", null);',
    'INSERT INTO EXPENSE VALUES ("E2", 100, "U3","U1" , "2022-01-12", null, "U3", null);',
    'INSERT INTO EXPENSE VALUES ("E3", 100, "U4", "U1", "2010-01-02", null, "U4", null);',
    'INSERT INTO EXPENSE VALUES ("E4", 100, "U5", "U1", "2021-07-20", null, "U5", null);',
    'INSERT INTO EXPENSE VALUES ("E5", 100, "G1","U1", "2019-07-12", null, "U1","G2");',
    'INSERT INTO EXPENSE VALUES ("E6", 100, "G2","U1", "2019-07-12", null, "U1","G1");',
    'INSERT INTO EXPENSE VALUES ("E7", 100, "U2","U1", "2021-07-12", "2022-07-20", "U2", null);',
    'INSERT INTO EXPENSE VALUES ("E8", 100, "U3","U1" , "2021-01-12", "2022-09-26", "U3", null);',
    'INSERT INTO EXPENSE VALUES ("E9", 100, "U4", "U1", "2021-01-02", "2022-11-19", "U4", null);',
    'INSERT INTO EXPENSE VALUES ("E10", 100, "G1","U1", "2021-07-12", "2022-07-20", "U1", "G1");',
    'INSERT INTO EXPENSE VALUES ("E11", 100, "G2","U1" , "2021-01-12", "2022-09-26", "U1", "G2");',
    'INSERT INTO group_member VALUES("G1", "U1");',
    'INSERT INTO group_member VALUES("G1", "U2");',
    'INSERT INTO group_member VALUES("G1", "U3");',
    'INSERT INTO group_member VALUES("G2", "U4");',
    'INSERT INTO group_member VALUES("G2", "U5");',
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

## GROUP FUNCTIONS
def addGroup():
    create_cursor.execute("SELECT COUNT(groupID) FROM GROUPING")
    row = create_cursor.fetchone()
    groupIDcount = row[0] if row[0] > 0 else 0
    next_id = "G1"
    if groupIDcount > 0:
        sql_statement = "SELECT * from GROUPING order by length(groupID), (substring(groupID, length(groupID)))"
        create_cursor.execute(sql_statement)
        result = create_cursor.fetchall()
        result = result[-1][0][1:]
        next_id =  f"G{int(result) + 1}"

    groupName = input("Enter Group Name: ")
    sql_statement = 'INSERT INTO GROUPING VALUES(%s,%s,%s,%s)'
    insert = (next_id,groupName,0,0)
    create_cursor.execute(sql_statement, insert)
    mariadb_connection.commit()
    print("\nSUCCESSFULLY ADDED NEW GROUP!")

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
    print(f"\nSUCCESSFULLY UPDATED {id}'s GROUP NAME to {new_group_name}!\n")

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
    selected_groupId = input("Enter Group ID: ")
    if (gq.isGroupIDValid(selected_groupId, create_cursor)):
        sql_statement = "DELETE from grouping where groupID = %s"
        try:
            create_cursor.execute(sql_statement, (selected_groupId,))
            mariadb_connection.commit()
            print(f"SUCCESSFULLY DELETED GROUP {selected_groupId}!")
        except:
            print("\nCANNOT DELETE GROUP BECAUSE IT IS REFERENCED AS A FOREIGN KEY")
    else:
        print(f"GROUD ID {selected_groupId} was not found!")
        
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
    selected_expenseId = input("Enter Expense ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
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
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewUserExpenses():
    selected_userId = input("Enter User ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isUserIDValid(selected_userId, create_cursor)):
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
    selected_groupId = input("Enter Group ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isGroupIDValid(selected_groupId, create_cursor)):
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

    #Configure expense amount 
    amount = 0
    while(True):
        try:
            amount = int(input("Enter expense amount: "))
            break
        except:
            print("\nAmount is invalid!")
    
    #Set Receiver to U1 as default recipient
    recipient = "U1"

    #Configure Receiver
    while (recipient == "U1"):
        isGroup = input("\nIs receiver a group? (y/n): ")
        if (isGroup == "n"):
            print("\nRecipient set to U1")
            break
        elif (isGroup == "y"):
            isValid = False
            while (isValid == False):
                recipient = input("\nEnter groupID recipient: ")
                isValid = gq.isGroupIDValid(recipient, create_cursor)
                if (isValid):
                    break
                else:
                    print("\nGroup ID was not found!")
            break
        else:
            print("\nInvalid Choice!")
    
    #Check sender's validity
    sender = None
    while (True):
        sender = input("\nEnter expense sender ID: ")
        if (((sender != "U1" and gq.isUserIDValid(sender, create_cursor)) or gq.isGroupIDValid(sender, create_cursor)) == False):
            print("Sender ID is not a valid ID")
        else:
            break

    #userID and groupID's default values are null
    userID = None
    groupID = None
    senderType = None
    recipientType = None

    #If recipient and sender are groups
    if (gq.isGroupIDValid(recipient, create_cursor) and gq.isGroupIDValid(sender, create_cursor)):
        groupID = sender
        senderType = "group"
        recipientType = "group"
    #If recipient is Group and sender is User
    elif (gq.isGroupIDValid(recipient, create_cursor) and gq.isUserIDValid(sender, create_cursor)):
        groupID = recipient
        userID = sender
        senderType = "user"
        recipientType = "group"
    #If recipient is User and sender is Group
    elif (gq.isUserIDValid(recipient, create_cursor) and gq.isGroupIDValid(sender, create_cursor)):
        groupID = sender
        userID = recipient
        senderType = "group"
        recipientType = "user"
    #If recipient and sender are users
    elif (gq.isUserIDValid(recipient, create_cursor) and gq.isUserIDValid(sender, create_cursor)):
        userID = sender
        senderType = "user"
        recipientType = "user"

    #Validate Date Owed
    dateOwed = None
    while(True):
        dateOwed = input("\nEnter date owed: ")
        if (gq.isValidDate(dateOwed)):
            break
        else:
            print("\nInvalid Date")
    
    #Configure Date Paid
    datePaid = None
    paid = "n"
    while(True):
        paid = input("Transaction was paid? (y/n): ") 
        if (paid == "y"):
            while (True):
                datePaid = input("\nEnter date paid: ")
                if (gq.isValidDate(datePaid)):
                    if (gq.isDateBeyond(datePaid, dateOwed, create_cursor)):
                        break
                    else:
                        print("Cannot set Date Paid before Date Owed!")
                else:
                    print("\nInvalid date!")
            break
        elif (paid == "n"):
            break
        else:
            print("\nInvalid Choice")
    
    
    sql_statement = "INSERT INTO EXPENSE VALUES(%s, %s, %s, %s, str_to_date(%s, '%Y-%m-%d'), str_to_date(%s, '%Y-%m-%d'), %s, %s)"
    create_cursor.execute(sql_statement, (next_id, amount, sender, recipient, dateOwed, datePaid, userID, groupID)   )
    print("AN EXPENSE WAS INSERTED SUCCESSFULLY")

    if paid == "n":
        if (senderType == "group" and recipientType == "group"):
            # update sender values
            sql_statement = "UPDATE grouping SET moneyLent=moneyLent+%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (amount, sender))

            # update recipient values
            sql_statement = "UPDATE grouping SET moneyOwed=moneyOwed+%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (amount, recipient))

        elif (senderType == "user" and recipientType == "group"):
            # update group values
            sql_statement = "UPDATE grouping SET moneyOwed=moneyOwed+%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (amount, recipient))

        elif (senderType == "group" and recipientType == "user"):
            # update group values
            sql_statement = "UPDATE grouping SET moneyLent=moneyLent+%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (amount, sender))

        elif (senderType == "user" and recipientType == "user"):
            # update sender values
            sql_statement = "UPDATE person SET moneyLent=moneyLent+%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (amount, sender))

            # update recipient values
            sql_statement = "UPDATE person SET moneyOwed=moneyOwed+%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (amount, recipient))

    mariadb_connection.commit()
    
def deleteExpense():
    selected_expenseId = input("Enter Expense ID: ")
    if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
        sql_statement = "DELETE from expense where expenseID = %s"
        create_cursor.execute(sql_statement, (selected_expenseId,))
        mariadb_connection.commit()
        print(f"EXPENSE ID {selected_expenseId} has been successfully deleted!")
    else:
        print(f"EXPENSE ID {selected_expenseId} was not found!")

def updateExpenseAmount(id):
    statement = "SELECT amount from EXPENSE where expenseID = %s"
    create_cursor.execute(statement, (id,))
    result = create_cursor.fetchone()
    print(f"CURRENT EXPENSE AMOUNT: {result[0]}")
    new_amount = int(input("Update new expense amount: "))
    statement = "UPDATE EXPENSE SET amount = %s where expenseID = %s"
    create_cursor.execute(statement, (new_amount, id))
    mariadb_connection.commit()

def updateExpenseSender(id):
    statement = "SELECT sender, recipient from EXPENSE where expenseID = %s"
    create_cursor.execute(statement, (id,))
    result = create_cursor.fetchone()
    sender = result[0]
    recipient = result[1]
    print(f"CURRENT EXPENSE SENDERID: {result[0]}")
    
    while (True):
        new_sender = input("Update new senderID: ")
        if (not gq.isGroupIDValid(new_sender, create_cursor) and not gq.isUserIDValid(new_sender, create_cursor)):
            print("\nInvalid senderID!")
        elif (new_sender == recipient): 
            print("\nCannot set senderID equal to recipientID!")
        elif (gq.isUserIDValid(new_sender, create_cursor)):
            if (gq.isUserIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, id))
                mariadb_connection.commit()
            elif (gq.isGroupIDValid(sender, create_cursor) and gq.isUserIDValid(recipient, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, None, id))
                mariadb_connection.commit()
            else:
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, recipient, id))
                mariadb_connection.commit()
            print("\nSUCCESSFULLY UPDATED SENDER!")
            break
        else:
            if (gq.isGroupIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, id))
                mariadb_connection.commit()
            elif (gq.isUserIDValid(sender, create_cursor) and gq.isGroupIDValid(recipient, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, None, new_sender, id))
                mariadb_connection.commit()
            else:
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, recipient, new_sender, id))
                mariadb_connection.commit()
            print("\nSUCCESSFULLY UPDATED SENDER!")
            break

def updateExpenseRecipient(id):
    statement = "SELECT sender, recipient from EXPENSE where expenseID = %s"
    create_cursor.execute(statement, (id,))
    result = create_cursor.fetchone()
    sender = result[0]
    recipient = result[1]
    print(f"CURRENT EXPENSE RECPIENTID: {result[1]}")
    while (True):
        new_recipient = input("Update new recipientID: ")
        if (not gq.isGroupIDValid(new_recipient, create_cursor) and not gq.isUserIDValid(new_recipient, create_cursor)):
            print("\nInvalid recipientID!")
        elif (new_recipient == sender): 
            print("\nCannot set recepientID equal to senderID!")
        elif (gq.isUserIDValid(new_recipient, create_cursor)):
            if (gq.isGroupIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET recipient = %s, userID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, new_recipient, id))
                mariadb_connection.commit()
            elif (gq.isUserIDValid(sender, create_cursor) and gq.isGroupIDValid(recipient, create_cursor)):
                statement = "UPDATE EXPENSE SET recipient = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, None, id))
                mariadb_connection.commit()
            else:
                statement = "UPDATE EXPENSE SET recipient = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, id))
                mariadb_connection.commit()
            print("\nSUCCESSFULLY UPDATED RECIPIENT!")
            break
        else:
            if (gq.isUserIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET recipient = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, new_recipient, id))
                mariadb_connection.commit()
            elif (gq.isGroupIDValid(sender, create_cursor) and gq.isUserIDValid(recipient, create_cursor)):
                statement = "UPDATE EXPENSE SET recipient = %s, userID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, None, id))
                mariadb_connection.commit()
            else:
                statement = "UPDATE EXPENSE SET recipient = %s where expenseID = %s"
                create_cursor.execute(statement, (new_recipient, id))
                mariadb_connection.commit()
            print("\nSUCCESSFULLY UPDATED RECIPIENT!")
            break

def updateDateOwed(id):
    new_date_owed = None
    sql_statement = "SELECT datePaid, dateOwed from EXPENSE where expenseID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()
    print(f"DATE PAID: {result[0]}")
    print(f"DATE OWED: {result[1]}")
    while (True):
        new_date_owed = input("\nEnter new date owed: ")
        if (gq.isValidDate(new_date_owed)):
            if result[0] == None or gq.isDateBehind(new_date_owed, result[0], create_cursor):
                print("UPDATED DATE OWED SUCCESSFULLY!")
                break
            else:
                print("\nCannot set Date Owed After Date Paid!")
        else:
            print("Invalid date!")
    sql_statement = "UPDATE EXPENSE SET dateOwed = %s where expenseID = %s"
    create_cursor.execute(sql_statement, (new_date_owed, id))
    mariadb_connection.commit()

def updateDatePaid(id):
    new_date_paid = None
    sql_statement = "SELECT datePaid, dateOwed from EXPENSE where expenseID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()
    print(f"DATE PAID: {result[0]}")
    print(f"DATE OWED: {result[1]}")
    while (True):
        new_date_paid = input("\nEnter new date paid: ")
        if (gq.isValidDate(new_date_paid)):
            if gq.isDateBeyond(new_date_paid, result[0], create_cursor):
                print("UPDATED DATE PAID SUCCESSFULLY!")
                break
            else:
                print("\nCannot set Date Paid Before Date Owed!")
        else:
            print("Invalid date!")
    sql_statement = "UPDATE EXPENSE SET datePaid = %s where expenseID = %s"
    create_cursor.execute(sql_statement, (new_date_paid, id))
    mariadb_connection.commit()

def updateExpense():
    while True:
        print("\n****SELECT UPDATE****")
        print("[1] Update Amount")
        print("[2] Update Sender")
        print("[3] Update Recipient")
        print("[4] Update Date Owed")
        print("[5] Update Date Paid")
        print("[0] Return")

        choice = input("\nPlease enter your choice: ")

        if (choice not in ["1", "2", "3", "4", "5", "0"]):
            print("Invalid choice!")
        elif (choice == "0"):
            break
        else:
            while True:
                selected_expenseId = input("\nEnter Expense ID: ")
                if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
                    if (choice == "1"):
                        updateExpenseAmount(selected_expenseId)
                    elif (choice == "2"):
                        updateExpenseSender(selected_expenseId)
                    elif (choice == "3"):
                        updateExpenseRecipient(selected_expenseId)
                    elif (choice == "4"):
                        updateDateOwed(selected_expenseId)
                    elif (choice == "5"):
                        updateDatePaid(selected_expenseId)
                    break
                else:
                    print(f"EXPENSE ID {selected_expenseId} was not found!")

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
            p.userMenu(create_cursor, create_cursor_commit)
        elif choice == "2":
            groupMenu()
        elif choice == "3":
            expenseMenu()
        elif choice == "4":
            reports()
        elif choice == "0":
            print("Thank you!\n")
            break
        else:
            print("Invalid Choice!!!")
            continue


menu()

create_cursor.close()   
mariadb_connection.close()