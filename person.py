from tabulate import tabulate
import re


def format_decimal(value):
    decimal_part = value % 1
    # no decimal part to print
    if decimal_part == 0:
        return "%.0f" % value
    else:
        return "%.2f" % value


def addUser(create_cursor, commit):
    create_cursor.execute("SELECT COUNT(userID) FROM PERSON")
    row = create_cursor.fetchone()
    userIDcount = row[0] if row else 0
    if userIDcount == 0:
        userID = "U1"
        fName = input("Enter First Name: ")
        lName = input("Enter Last Name: ")
        sql_statement = 'INSERT INTO PERSON VALUES(%s,%s,%s,%s,%s)'
        insert = (userID, fName, lName, 0, 0)
        create_cursor.execute(sql_statement, insert)
    else:
        userID = "U" + str(userIDcount + 1)
        fName = input("Enter First Name: ")
        lName = input("Enter Last Name: ")
        sql_statement = 'INSERT INTO PERSON VALUES(%s,%s,%s,%s,%s,%s)'
        insert = (userID, fName, lName, 0, 0, "U1")
        create_cursor.execute(sql_statement, insert)
    print("\nSuccessfully added Person!\n")
    commit()


def updateFirstName(id, create_cursor, commit):
    sql_statement = "SELECT fName FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} First Name: {result}")
    new_first_name = input("Enter new First Name: ")
    sql_statement = "UPDATE person SET fName = %s WHERE userID = %s"
    insert = (new_first_name, id)
    create_cursor.execute(sql_statement, insert)
    commit()
    print(f"\nSuccessfully updated {id}'s First Name!\n")


def updateLastName(id, create_cursor, commit):
    sql_statement = "SELECT lName FROM person where userID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Last Name: {result}")
    new_last_name = input("Enter new Last Name: ")
    sql_statement = "UPDATE person SET lName = %s WHERE userID = %s"
    insert = (new_last_name, id)
    create_cursor.execute(sql_statement, insert)
    commit()
    print(f"\nSuccessfully updated {id}'s Last Name!\n")


def updatePersonMoneyOwed(id, create_cursor, commit):
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
    try:
        select_money_owed = "SELECT moneyOwed FROM person where userID = %s"
        owed = create_cursor.execute(select_money_owed, (id,))
        owed = create_cursor.fetchone()
        owed = float(owed[0])
        owed_difference = updated_money_owed - owed
        update_statement = "UPDATE person SET moneyOwed = %s WHERE userID = %s"
        insert = (updated_money_owed, id)
        updateMoneyLent = "UPDATE person set moneyLent = moneyLent + %s where userID= 'U1'"
        updateMoneyOwed = "UPDATE person set moneyOwed = moneyOwed - %s where userId = 'U1'"
        create_cursor.execute(update_statement, insert)
        create_cursor.execute(updateMoneyLent, (owed_difference,))
        create_cursor.execute(updateMoneyOwed, (owed_difference,))
        commit()
        print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY OWED!\n")
    except:
        print(f"FAILED TO UPDATE {id}'s MONEY OWED")


def updatePersonMoneyLent(id, create_cursor, commit):
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
    try:
        select_money_lent = "SELECT moneyLent FROM person where userID = %s"
        lent = create_cursor.execute(select_money_lent, (id,))
        lent = create_cursor.fetchone()
        lent = lent[0]
        lent_difference = updated_money_lent - float(lent)
        update_statement = "UPDATE person SET moneyLent = %s WHERE userID = %s"
        insert = (updated_money_lent, id)
        updateMoneyOwed = "UPDATE person set moneyOwed = moneyOwed + %s where userID= 'U1'"
        create_cursor.execute(update_statement, insert)
        create_cursor.execute(updateMoneyOwed, (lent_difference,))
        commit()
        print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY LENT!\n")
    except:
        print(f"FAILED TO UPDATE {id}'s MONEY LENT")

def showUpdatePersonMenu(create_cursor, commit):
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

    while (True):
        print("\n****SELECT UPDATE****")
        print("[1] Update First Name")
        print("[2] Update Last Name")
        print("[3] Update Money Owed")
        print("[4] Update Money Lent")

        choice = input("\nPlease enter choice: ")

        if (choice == "1"):
            updateFirstName(id, create_cursor, commit)
        elif (choice == "2"):
            updateLastName(id, create_cursor, commit)
        elif (choice == "3"):
            updatePersonMoneyOwed(id, create_cursor, commit)
        elif (choice == "4"):
            updatePersonMoneyLent(id, create_cursor, commit)
        else:
            print("INVALID CHOICE!!")
            continue
        print()
        break


def viewAllPerson(create_cursor):
    sql_statement = "SELECT * FROM person"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["userID", "First Name", "Last Name",
                   "Money Owed", "Money Lent", "borrowerID"]]
    for res in result:
        person_data = [res[0], res[1], res[2],
                       str(res[3]), str(res[4]), res[5]]
        table_data.append(person_data)
    print("CURRENT PERSONS")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))


def searchPerson(create_cursor):
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
    person = create_cursor.fetchone()
    print("\nVIEWING PERSON...\n")
    print(" userID:", person[0])
    print(" First Name:", person[1])
    print(" Last Name: ", person[2])
    print(" Money Owed:", format_decimal(person[3]))
    print(" Money Lent:", format_decimal(person[4]))
    print(" borrowerID: ", person[5])


def deletePerson(create_cursor, commit):
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
    try:
        lent_statement = "SELECT moneyLent from person where userID = %s"
        lent = create_cursor.execute(lent_statement,(id,))
        lent = create_cursor.fetchone()
        lent = lent[0]
        updateMoneyOwed = "UPDATE person set moneyOwed = moneyOwed - %s where userID ='U1'"
        sql_statement = "DELETE from person where userID = %s"
        create_cursor.execute(updateMoneyOwed,(lent,))
        create_cursor.execute(sql_statement,(id,))
        commit()
        print("Successfully deleted!")
    except:
        print("\nCANNOT DELETE PERSON BECAUSE IT IS REFERENCED AS A FOREIGN KEY")    


def userMenu(create_cursor, commit):
    choice = -1
    while (choice != 0):
        print("\n**********USER MENU*********")
        print("[1] Add User")
        print("[2] Delete User")
        print("[3] Search User")
        print("[4] Update User")
        print("[5] View All Users")
        print("[0] Return\n")

        choice = input("Please enter choice: ")

        if choice == "1":
            addUser(create_cursor, commit)
        elif choice == "2":
            deletePerson(create_cursor, commit)
        elif choice == "3":
            searchPerson(create_cursor)
        elif choice == "4":
            showUpdatePersonMenu(create_cursor, commit)
        elif choice == "5":
            viewAllPerson(create_cursor)
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue
