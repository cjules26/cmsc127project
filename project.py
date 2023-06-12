import mysql.connector as mariadb
import person as p
import group as g
import expense as e
import reports as r

def run_sql_file(file_path, create_cursor, create_cursor_commit):
    # Read the contents of the SQL file
    with open(file_path, 'r') as sql_file:
        sql_script = sql_file.read()

    # Split the SQL script into individual statements
    statements = sql_script.split(';')
    statements = statements[:-1]  # need to remove last element

    # Execute each SQL statement
    for statement in statements:
        statement = statement + ";"
        create_cursor.execute(statement)

    create_cursor_commit()


def menu():
    print("User: root")
    pword = input("Enter password: ")
    mariadb_connection = mariadb.connect(
        user='root', password=pword, host='localhost', port='3306')
    create_cursor = mariadb_connection.cursor(buffered=True)

    def create_cursor_commit():
        mariadb_connection.commit()

    sql_file_path = 'app_mysql.sql'
    run_sql_file(sql_file_path, create_cursor, create_cursor_commit)

    #t.createDatabase(create_cursor, create_cursor_commit)

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
