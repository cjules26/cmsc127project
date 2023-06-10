import datetime
#GENERAL QUERIES AND FUNCTIONS

#PERSON
def getAllUserIDs(cursor):
    sql_statement = "SELECT userID FROM PERSON"
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    return(list_of_ids)

def isUserIDValid(id, cursor):
    if (id in getAllUserIDs(cursor)):
        return True
    else:
        return False

#GROUPING
def getAllGroupIDs(cursor):
    sql_statement = "SELECT groupID FROM GROUPING"
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    return(list_of_ids)

def isGroupIDValid(id, cursor):
    if (id in getAllGroupIDs(cursor)):
        return True
    else:
        return False

#EXPENSE
def getAllExpenseIDs(cursor):
    sql_statement = "SELECT expenseID FROM EXPENSE"
    cursor.execute(sql_statement)
    result = cursor.fetchall()
    list_of_ids = [id[0] for id in result]
    return(list_of_ids)

def isExpenseIDValid(id, cursor):
    if (id in getAllExpenseIDs(cursor)):
        return True
    else:
        return False
    
#OTHERS
def isValidDate(date):
    regex = datetime.datetime.strptime
    try:
        assert regex(date, '%Y-%m-%d')
        return True
    except:
        return False