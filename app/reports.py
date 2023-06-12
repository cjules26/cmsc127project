from tabulate import tabulate
import expense as e
import group as g

def viewCurrentBalanceFromAllExpenses(create_cursor):
    sql_statement = "SELECT moneyOwed FROM PERSON where userID='U1'"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["Current Balance"]]

    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(f"\nMain User's Current Balance")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewExpenseMadeWithinAMonth(create_cursor):
    months = { "1": "January", "2": "February", "3":"March", "4":"April", "5":"May", "6":"June", "7":"July", "8":"August", "9":"September", "10":"October", "11":"November", "12":"December" }
    month = input("Enter Month in digits:")
    print(f"Month selected: {months[month]}")
    sql_statement = "SELECT* from expense where month(dateOwed) = %s"
    create_cursor.execute(sql_statement,(month,))
    result = create_cursor.fetchall()
    table_data = [["Expense ID", "Amount", "Sender", "Recipient", "Date Owed", "Date Paid", "userID", "groupID"]]
    [table_data.append([expense[i] for i in range(0,len(table_data[0]))]) for expense in result]
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def viewUsersWithOutstandingBalance(create_cursor):
    sql_statement ="SELECT* from person where moneyOwed >0 and userID !='U1'"
    create_cursor.execute(sql_statement)
    result = create_cursor.fetchall()
    table_data = [["userID", "First Name","Last Name", "Money Owed", "Money Lent", "borrowerID"]]
    for res in result:
        person_data = [res[0], res[1], res[2], str(res[3]), str(res[4]), res[5]]
        table_data.append(person_data)
    print("CURRENT PERSON(S) WITH OUTSTANDING BALANCE")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

def reports(create_cursor):
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
            viewExpenseMadeWithinAMonth(create_cursor)
        elif choice == "2":
            e.viewUserExpenses(create_cursor)
        elif choice == "3":
            e.viewGroupExpenses(create_cursor)
        elif choice == "4":
            viewCurrentBalanceFromAllExpenses(create_cursor)
        elif choice == "5":
            viewUsersWithOutstandingBalance(create_cursor)
        elif choice == "6":
            g.viewAllGroups(create_cursor)
        elif choice == "7":
            g.viewGroupsWithOutstandingBalance(create_cursor)
        elif choice == "0":
            print()
            break
        else:
            print("Invalid Choice!!!")
            continue

