from tabulate import tabulate
import general_queries as gq


def viewExpense(create_cursor):
    selected_expenseId = input("Enter Expense ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient",
                   "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
        sql_statement = "SELECT * from EXPENSE where expenseID = %s"
        create_cursor.execute(sql_statement, (selected_expenseId,))
        expense_info = create_cursor.fetchone()
        table_data.append([expense_info[i]
                          for i in range(0, len(table_data[0]))])
    else:
        print(f"EXPENSE ID {selected_expenseId} was not found!!!")
        return
    print(f"\n{selected_expenseId} EXPENSE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


def viewAllExpenses(create_cursor):
    sql_statement = "SELECT * FROM EXPENSE order by length(expenseID), (substring(expenseID, length(expenseID)))"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Expense ID", "Amount", "Sender", "Recipient",
                   "Date Owed", "Date Paid", "userID", "groupID"]]
    [table_data.append([expense[i] for i in range(0, len(table_data[0]))])
     for expense in result]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


def viewUserExpenses(create_cursor):
    selected_userId = input("Enter User ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient",
                   "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isUserIDValid(selected_userId, create_cursor)):
        sql_statement = "SELECT * FROM EXPENSE where sender = %s"
        create_cursor.execute(sql_statement, (selected_userId,))
        result = create_cursor.fetchall()
        [table_data.append([expense[i] for i in range(
            0, len(table_data[0]))]) for expense in result]
    else:
        print(f"USER ID {selected_userId} was not found!!!")
        return
    print(f"\n{selected_userId}'s EXPENSES")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


def viewGroupExpenses(create_cursor):
    selected_groupId = input("Enter Group ID: ")
    table_data = [["Expense ID", "Amount", "Sender", "Recipient",
                   "Date Owed", "Date Paid", "userID", "groupID"]]
    if (gq.isGroupIDValid(selected_groupId, create_cursor)):
        sql_statement = "SELECT * FROM EXPENSE where sender = %s"
        create_cursor.execute(sql_statement, (selected_groupId,))
        result = create_cursor.fetchall()
        [table_data.append([expense[i] for i in range(
            0, len(table_data[0]))]) for expense in result]
    else:
        print(f"GROUP ID {selected_groupId} was not found!!!")
        return
    print(f"\n{selected_groupId}'s EXPENSES")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


def insertExpense(create_cursor, create_cursor_commit):
    sql_statement = "SELECT * from EXPENSE order by length(expenseID), (substring(expenseID, length(expenseID)))"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    result = result[-1][0][1:]
    next_id = f"E{int(result) + 1}"

    # Configure expense amount
    amount = 0
    while (True):
        try:
            amount = int(input("Enter expense amount: "))
            break
        except:
            print("\nAmount is invalid!")

    # Set Receiver to U1
    recipient = "U1"

    # Check sender's validity
    sender = None
    while (True):
        sender = input("\nEnter expense sender ID: ")
        if (((sender != "U1" and gq.isUserIDValid(sender, create_cursor))) == False):
            if gq.isGroupIDValid(sender, create_cursor):
                print("Group to group expenses are not allowed!")
            else:
                print("Sender ID is not a valid ID")
        else:
            break

    # userID and groupID's default values are null
    userID = None
    groupID = None
    senderType = None

    # If sender is group
    if (gq.isGroupIDValid(sender, create_cursor)):
        groupID = sender
        senderType = "group"
        userID = recipient
    # If sender is user
    else:
        userID = sender
        senderType = "user"

    # Validate Date Owed
    dateOwed = None
    while (True):
        dateOwed = input("\nEnter date owed: ")
        if (gq.isValidDate(dateOwed)):
            break
        else:
            print("\nInvalid Date")

    # Configure Date Paid
    datePaid = None
    paid = "n"
    while (True):
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
    create_cursor.execute(sql_statement, (next_id, amount,
                          sender, recipient, dateOwed, datePaid, userID, groupID))
    print("AN EXPENSE WAS INSERTED SUCCESSFULLY")

    if paid == "n":
        if (senderType == "group"):
            # update sender values
            sql_statement = "UPDATE grouping SET moneyLent=moneyLent+%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (amount, sender))

            # update recipient values
            sql_statement = "UPDATE person SET moneyOwed=moneyOwed+%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (amount, recipient))

        elif (senderType == "user"):
            # update sender values
            sql_statement = "UPDATE person SET moneyLent=moneyLent+%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (amount, sender))

            # update recipient values
            sql_statement = "UPDATE person SET moneyOwed=moneyOwed+%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (amount, recipient))

    create_cursor_commit()


def deleteExpense(create_cursor, create_cursor_commit):
    selected_expenseId = input("Enter Expense ID: ")
    if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
        sql_statement = "SELECT datePaid from expense where expenseID = %s"
        create_cursor.execute(sql_statement, (selected_expenseId,))
        result = create_cursor.fetchone()[0]
        datePaid = True if result[0] else False
        if (datePaid):
            sql_statement = "DELETE from expense where expenseID = %s"
            create_cursor.execute(sql_statement, (selected_expenseId,))
            create_cursor_commit()
            print(
                f"EXPENSE ID {selected_expenseId} has been successfully deleted!")
        else:
            print("CANNOT DELETE AN UNPAID EXPENSE!")
    else:
        print(f"EXPENSE ID {selected_expenseId} was not found!")


def updateExpenseAmount(id, create_cursor, create_cursor_commit):
    statement = "SELECT amount, sender, recipient, datePaid from EXPENSE where expenseID = %s"
    create_cursor.execute(statement, (id,))
    result = create_cursor.fetchone()
    print(f"CURRENT EXPENSE AMOUNT: {result[0]}")
    new_amount = int(input("Update new expense amount: "))
    statement = "UPDATE EXPENSE SET amount = %s where expenseID = %s"
    create_cursor.execute(statement, (new_amount, id))

    # instantiate sender, recipient values
    old_amount = result[0]
    sender = result[1]
    recipient = result[2]
    paid = "y" if result[3] else "n"

    if paid == "n":
        # If sender is group
        if (gq.isGroupIDValid(sender, create_cursor)):
            # update sender values
            sql_statement = "UPDATE grouping SET moneyLent=moneyLent+%s-%s WHERE groupID=%s"
            create_cursor.execute(sql_statement, (new_amount, old_amount, sender))

            # update recipient values
            sql_statement = "UPDATE person SET moneyOwed=moneyOwed+%s-%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (new_amount, old_amount, recipient))
        # If sender is User
        else:
            #update recipient values
            sql_statement = "UPDATE person SET moneyLent=moneyLent+%s-%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (new_amount, old_amount, sender))

            #update sender values
            sql_statement = "UPDATE person SET moneyOwed=moneyOwed+%s-%s WHERE userID=%s"
            create_cursor.execute(sql_statement, (new_amount, old_amount, recipient))
    
    print("\nSUCCESSFULLY UPDATED EXPENSE AMOUNT!")
    create_cursor_commit()


def updateExpenseSender(id, create_cursor, create_cursor_commit):
    statement = "SELECT sender, recipient, amount, datePaid from EXPENSE where expenseID = %s"
    create_cursor.execute(statement, (id,))
    result = create_cursor.fetchone()
    sender = result[0]
    recipient = result[1]
    print(f"CURRENT EXPENSE SENDERID: {result[0]}")
    amount = result[2]
    paid = True if result[3] else False

    while (True):
        new_sender = input("Update new senderID: ")
        if (not gq.isGroupIDValid(new_sender, create_cursor) and not gq.isUserIDValid(new_sender, create_cursor)):
            print("\nInvalid senderID!")
        elif (new_sender == recipient):
            print("\nCannot set senderID equal to recipientID!")
        # new_sender is user
        elif (gq.isUserIDValid(new_sender, create_cursor)):
            # orig_sender is user
            if (gq.isUserIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, id))
                if (not paid):
                    # deduct from orig_sender user
                    statement = "UPDATE person SET moneyLent=moneyLent-%s where userID = %s"
                    create_cursor.execute(statement, (amount, sender))
                    # add to new_sender user
                    statement = "UPDATE person SET moneyLent=moneyLent+%s where userID = %s"
                    create_cursor.execute(statement, (amount, new_sender))
            # orig_sender is group
            elif (gq.isGroupIDValid(sender, create_cursor) and gq.isUserIDValid(recipient, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, None, id))
                if (not paid):
                    # deduct from orig_sender group
                    statement = "UPDATE grouping SET moneyLent=moneyLent-%s where groupID = %s"
                    create_cursor.execute(statement, (amount, sender))
                    # add to new_sender user
                    statement = "UPDATE person SET moneyLent=moneyLent+%s where userID = %s"
                    create_cursor.execute(statement, (amount, new_sender))

            print("\nSUCCESSFULLY UPDATED SENDER!")
            break
        # new_sender is group
        else:
            # orig_sender is group
            if (gq.isGroupIDValid(sender, create_cursor)):
                statement = "UPDATE EXPENSE SET sender = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, new_sender, id))
                if (not paid):
                    # deduct from orig_sender group
                    statement = "UPDATE grouping SET moneyLent=moneyLent-%s where groupID = %s"
                    create_cursor.execute(statement, (amount, sender))
                    # add to new_sender group
                    statement = "UPDATE grouping SET moneyLent=moneyLent+%s where groupID = %s"
                    create_cursor.execute(statement, (amount, new_sender))
            # orig_sender is user
            else:
                statement = "UPDATE EXPENSE SET sender = %s, userID = %s, groupID = %s where expenseID = %s"
                create_cursor.execute(statement, (new_sender, recipient, new_sender, id))
                if (not paid):
                    # deduct from orig_sender user
                    statement = "UPDATE person SET moneyLent=moneyLent-%s where userID = %s"
                    create_cursor.execute(statement, (amount, sender))
                    # add to new_sender group
                    statement = "UPDATE grouping SET moneyLent=moneyLent+%s where groupID = %s"
                    create_cursor.execute(statement, (amount, new_sender))

            print("\nSUCCESSFULLY UPDATED SENDER!")
            break
    
    create_cursor_commit()

def updateDateOwed(id, create_cursor, create_cursor_commit):
    new_date_owed = None
    sql_statement = "SELECT datePaid, dateOwed from EXPENSE where expenseID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()
    print(f"DATE PAID: {result[0]}")
    print(f"DATE OWED: {result[1]}")
    while (True):
        new_date_owed = input("\nEnter new date owed: ")
        #if new date owed is a valid date
        if (gq.isValidDate(new_date_owed)):
            #if expense is not yet paid or date paid comes after date owed
            if result[0] == None or gq.isDateBehind(new_date_owed, result[0], create_cursor):
                print("UPDATED DATE OWED SUCCESSFULLY!")
                break
            else:
                print("\nCannot set Date Owed After Date Paid!")
        else:
            print("Invalid date!")
    sql_statement = "UPDATE EXPENSE SET dateOwed = %s where expenseID = %s"
    create_cursor.execute(sql_statement, (new_date_owed, id))
    create_cursor_commit()

def updateDatePaid(id, create_cursor, create_cursor_commit):
    new_date_paid = None
    sql_statement = "SELECT datePaid, dateOwed, amount, sender, recipient from EXPENSE where expenseID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()
    datePaid = result[0]
    dateOwed = result[1]
    amount = result[2]
    sender = result[3]
    recipient = result[4]

    print(f"DATE PAID: {datePaid}")
    print(f"DATE OWED: {dateOwed}")
    while (True):
        new_date_to_null = input("Set new date paid to null? (y/n): ")

        if (new_date_to_null=="y"):
            print("UPDATED DATE PAID SUCCESSFULLY!")
            sql_statement = "UPDATE EXPENSE SET datePaid = %s where expenseID = %s"
            create_cursor.execute(sql_statement, (None, id))

            # if previous datePaid is not None => add moneyLent of sender, add moneyOwed of recipient
            if (datePaid):
                # If recipient is User and sender is Group
                if (gq.isUserIDValid(recipient, create_cursor) and gq.isGroupIDValid(sender, create_cursor)):
                    statement = "UPDATE person SET moneyOwed=moneyOwed+%s where userID = %s"
                    create_cursor.execute(statement, (amount, recipient))
                    statement = "UPDATE grouping SET moneyLent=moneyLent+%s where groupID = %s"
                    create_cursor.execute(statement, (amount, sender))

                # If recipient and sender are users
                elif (gq.isUserIDValid(recipient, create_cursor) and gq.isUserIDValid(sender, create_cursor)):
                    statement = "UPDATE person SET moneyOwed=moneyOwed+%s where userID = %s"
                    create_cursor.execute(statement, (amount, recipient))
                    statement = "UPDATE person SET moneyLent=moneyLent+%s where userID = %s"
                    create_cursor.execute(statement, (amount, sender))
            break

        #if new date owed is a valid date
        elif (new_date_to_null=="n"):
            while(True):
                new_date_paid = input("\nEnter new date paid: ")

                if (gq.isValidDate(new_date_paid)):
                    #if expense is not yet paid or date paid comes after date owed
                    if result[0] == None and gq.isDateBeyond(new_date_paid, result[1], create_cursor):
                        print("UPDATED DATE PAID SUCCESSFULLY!")
                        sql_statement = "UPDATE EXPENSE SET datePaid = %s where expenseID = %s"
                        create_cursor.execute(sql_statement, (new_date_paid, id))
                        
                        # if previous datePaid is None => deduct moneyLent of sender, deduct moneyOwed of recipient
                        if (not datePaid):

                            # If recipient is User and sender is Group
                            if (gq.isUserIDValid(recipient, create_cursor) and gq.isGroupIDValid(sender, create_cursor)):
                                statement = "UPDATE person SET moneyOwed=moneyOwed-%s where userID = %s"
                                create_cursor.execute(statement, (amount, recipient))
                                statement = "UPDATE grouping SET moneyLent=moneyLent-%s where groupID = %s"
                                create_cursor.execute(statement, (amount, sender))

                            # If recipient and sender are users
                            elif (gq.isUserIDValid(recipient, create_cursor) and gq.isUserIDValid(sender, create_cursor)):
                                statement = "UPDATE person SET moneyOwed=moneyOwed-%s where userID = %s"
                                create_cursor.execute(statement, (amount, recipient))
                                statement = "UPDATE person SET moneyLent=moneyLent-%s where userID = %s"
                                create_cursor.execute(statement, (amount, sender))
                        break
                    else:
                        print("\nCannot set Date Paid Before Date Owed!")
                else:
                    print("Invalid date!")
            break
                
        else:
            print("Invalid choice!")

    create_cursor_commit()


def updateExpense(create_cursor, create_cursor_commit):
    while True:
        print("\n****SELECT UPDATE****")
        print("[1] Update Amount")
        print("[2] Update Sender")
        print("[3] Update Date Owed")
        print("[4] Update Date Paid")
        print("[0] Return")

        choice = input("\nPlease enter your choice: ")

        if (choice not in ["1", "2", "3", "4", "0"]):
            print("Invalid choice!")
        elif (choice == "0"):
            break
        else:
            while True:
                selected_expenseId = input("\nEnter Expense ID: ")
                if (gq.isExpenseIDValid(selected_expenseId, create_cursor)):
                    if (choice == "1"):
                        updateExpenseAmount(
                            selected_expenseId, create_cursor, create_cursor_commit)
                    elif (choice == "2"):
                        updateExpenseSender(
                            selected_expenseId, create_cursor, create_cursor_commit)
                    elif (choice == "3"):
                        updateDateOwed(selected_expenseId,
                                       create_cursor, create_cursor_commit)
                    elif (choice == "4"):
                        updateDatePaid(selected_expenseId,
                                       create_cursor, create_cursor_commit)
                    break
                else:
                    print(f"EXPENSE ID {selected_expenseId} was not found!")


def expenseMenu(create_cursor, create_cursor_commit):
    choice = -1
    while (choice != 0):
        print("\n**********EXPENSE MENU*********")
        print("[1] Insert an expense")
        print("[2] Delete an expense")
        print("[3] Update an expense")
        print("[4] View Expense")
        print("[5] View User Expenses")
        print("[6] View Group Expenses")
        print("[7] View All Expenses")
        print("[0] Return\n")

        choice = input("Please enter choice: ")

        if choice == "1":
            insertExpense(create_cursor, create_cursor_commit)
        elif choice == "2":
            deleteExpense(create_cursor, create_cursor_commit)
        elif choice == "3":
            updateExpense(create_cursor, create_cursor_commit)
        elif choice == "4":
            viewExpense(create_cursor)
        elif choice == "5":
            viewUserExpenses(create_cursor)
        elif choice == "6":
            viewGroupExpenses(create_cursor)
        elif choice == "7":
            viewAllExpenses(create_cursor)
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue
