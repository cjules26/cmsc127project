def createDatabase(create_cursor, create_cursor_commit):

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
        'INSERT INTO EXPENSE VALUES ("E5", 100, "G1","U1", "2019-07-12", null, "U1","G1");',
        'INSERT INTO EXPENSE VALUES ("E6", 100, "G2","U1", "2019-07-12", null, "U1","G2");',
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

    create_cursor_commit()

    create_cursor.execute("SHOW TABLES")

    tables = create_cursor.fetchall()

    if len(tables) == 0:
        print("No tables yet")
    else:
        print("TABLES:")
        for table in tables:
            print(" ", table[0])
        print()
