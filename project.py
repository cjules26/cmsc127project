import mysql.connector as mariadb
import person as p
import group as g
import expense as e
import reports as r
import tables as t


def menu():
    print("User: root")
    pword = input("Enter password: ")
    mariadb_connection = mariadb.connect(
        user='root', password=pword, host='localhost', port='3306')
    create_cursor = mariadb_connection.cursor(buffered=True)

    def create_cursor_commit():
        mariadb_connection.commit()

    t.createDatabase(create_cursor, create_cursor_commit)

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
            g.groupMenu(create_cursor, create_cursor_commit)
        elif choice == "3":
            e.expenseMenu(create_cursor, create_cursor_commit)
        elif choice == "4":
            r.reports(create_cursor)
        elif choice == "0":
            print("Thank you!\n")
            break
        else:
            print("Invalid Choice!!!")
            continue

    create_cursor.close()
    mariadb_connection.close()


menu()
