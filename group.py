from tabulate import tabulate
import general_queries as gq
import re   


def format_decimal(value):
    decimal_part = value % 1
    # no decimal part to print
    if decimal_part == 0:
        return "%.0f" % value
    else:
        return "%.2f" % value

## GROUP FUNCTIONS
def addGroup(create_cursor, commit):
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
    commit()
    print("\nSUCCESSFULLY ADDED NEW GROUP!")

def updateGroupName(id,create_cursor, commit):
    sql_statement = "SELECT groupName FROM GROUPING where groupID = %s"
    create_cursor.execute(sql_statement, (id,))
    result = create_cursor.fetchone()[0]
    print(f"\nCurrent {id} Group Name: {result}")
    new_group_name = input("Enter new group name: ")
    sql_statement = "UPDATE grouping SET groupName = %s WHERE groupID = %s"
    insert = (new_group_name, id)
    create_cursor.execute(sql_statement, insert)
    commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s GROUP NAME to {new_group_name}!\n")

def updateGroupMoneyOwed(id,create_cursor, commit):
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
    commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY OWED!\n")

def updateGroupMoneyLent(id,create_cursor, commit):
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
    commit()
    print(f"\nSUCCESSFULLY UPDATED {id}'s MONEY LENT!\n")

def showUpdateGroupMenu(create_cursor, commit):
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
            updateGroupName(id,create_cursor, commit)
        elif (choice == "2"):
            updateGroupMoneyOwed(id,create_cursor, commit)
        elif (choice == "3"):
            updateGroupMoneyLent(id,create_cursor, commit)
        else:
            print("INVALID CHOICE!!")
            continue
        break

def deleteGroup(create_cursor, commit):
    selected_groupId = input("Enter Group ID: ")
    if (gq.isGroupIDValid(selected_groupId, create_cursor)):
        groupMoneyLent = "SELECT moneyLent from grouping where groupID = %s"
        personMoneyOwed = "SELECT moneyOwed from person where userID = 'U1'"
        update = "UPDATE person set moneyOwed = %s - %s"
        del_statement = "DELETE from grouping where groupID = %s"
        try:
            # create_cursor.execute(update, (personMoneyOwed,),(groupMoneyLent, (selected_groupId,)))
            create_cursor.execute(del_statement, (selected_groupId,))
            commit()
            print(f"SUCCESSFULLY DELETED GROUP {selected_groupId}!")
        except:
            print("\nCANNOT DELETE GROUP BECAUSE IT IS REFERENCED AS A FOREIGN KEY")
    else:
        print(f"GROUD ID {selected_groupId} was not found!")
        
def viewAllGroups(create_cursor):
    sql_statement = "SELECT * FROM GROUPING"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Group ID", "Group Name", "Money Owed", "Money Lent"]]
    for res in result:
        group_data = [res[0], res[1], str(res[2]), str(res[3])]
        table_data.append(group_data)
    print("\nCURRENT GROUPS")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewGroupsWithOutstandingBalance(create_cursor):
    sql_statement = "SELECT * FROM grouping WHERE moneyOwed>0;"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Group ID", "Group Name", "Money Owed", "Money Lent"]]
    for res in result:
        group_data = [res[0], res[1], str(res[2]), str(res[3])]
        table_data.append(group_data)
    print("\nGROUPS WITH OUTSTANDING BALANCE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    
def searchGroup(create_cursor):
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


def groupMenu(create_cursor, commit):
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
            addGroup(create_cursor, commit)
        elif choice == "2":
            deleteGroup(create_cursor, commit)
        elif choice == "3":
            searchGroup(create_cursor)
        elif choice == "4":
            showUpdateGroupMenu(create_cursor,commit)
        elif choice == "5":
            viewAllGroups(create_cursor)
        elif choice == "6":
            viewGroupsWithOutstandingBalance(create_cursor)
        elif choice == "0":
            break
        else:
            print("Invalid Choice!!!")
            continue

