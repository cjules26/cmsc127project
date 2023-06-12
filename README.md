# cmsc127project
This app helps user track their expenses made within a friend, or group

# Prerequisites
1. Mariadb must be installed in device<br>
2. Python must be installed in device<br>
3. Python Packages:
    - mysql.connector 
    - tabulate
    - datetime
    - re

# To run the program:
1. Open your terminal then run pip install my-sql-connector <br>
2. Run pip install tabulate <br>
3. Run app/project.py <br>
4. Enter your mariadb password <br>

# NOTES: 
- Valid Date Format: (YYYY-MM-DD)

# PROGRAM FUNCTIONALITIES

# MENU
- Menu acts as the homepage of the terminal that displays the routes to USER, GROUP, EXPENSE, and Reports Menus as well as the option to exit the program. 

## [1] USER
- User option is the route to access the actions related to USERS.

### USER MENU
- Displays the options for USERS.
- Add, Delete, Search, Update, View All Users

#### [1] ADD USER
- Adds an instance of a user to the database.
- Asks fors USER's first name and lastname.
- Money owed and lent are initilazed to zero.
- Borrower ID's of non-U1 USERS are automatically set to U1, otherwise, null

#### [2] DELETE USER
- Deletes a USER from the database
- Asks for USER ID to find the instance of the user
- A USER cannot be deleted if it is referenced as a foreign key
- Deducts U1's money owed by the USER's money lent 

#### [3] SEARCH USER
- Displays all the information related to a USER
- Ask for a USER ID to locate a user in the database

#### [4] UPDATE USER
- Displays menu to update USER's first name, last name, money owed and money lent.
- Asks for USER ID

##### [1] UPDATE FIRST NAME
- Updates USER's first name
- Asks for USER's new first name

##### [2] UPDATE LAST NAME
- Updates USER's last name
- Asks for USER's new last name

##### [3] UPDATE MONEY OWED
- Updates USER's money
- Asks for USER's new money owed amount

##### [4] UPDATE MONEY LENT
- Updates USER's money
- Asks for USER's new money lent amount

#### [5] VIEW ALL USERS
- Displays all the instances of USER existing in the database in tabular format

## [2] GROUP
- Group option is the route to access the actions related to GROUPS.

### GROUP MENU
- Displays the options for GROUPS.
- Add, Delete, Search, Update, View All GROUPS and View All GROUPS with Outstanding Balance

#### [1] ADD GROUP
- Adds an instance of a GROUP to the database.
- Asks for GROUPS's name only.
- Money owed and lent are initilazed to zero.

#### [2] DELETE GROUP
- Deletes a GROUP from the database
- Asks for GROUP ID to find the instance of the GROUP
- A GROUP cannot be deleted if it is referenced as a foreign key
- Deducts U1's money owed and money lent by the GROUPS's money owed and money lent, respectively

### [3] SEARCH GROUP
-Displays all information about the groupID entered

#### [4] UPDATE GROUP
- Displays menu to update GROUP's name, money owed and money lent.
- Asks for GROUP ID

##### [1] UPDATE NAME
- Updates GROUP's name
- Asks for GROUP's new name

##### [2] UPDATE MONEY OWED
- Updates GROUP's money
- Asks for GROUPS's new money owed amount

##### [3] UPDATE MONEY LENT
- Updates GROUPS's money
- Asks for GROUPS's new money lent amount

#### [5] VIEW ALL GROUPS
- Displays all the instances of GROUP existing in the database in tabular format

#### [6] VIEW ALL GROUPS WITH OUTSTANDING BALANCE
- Displays all the instances of GROUP that has money owed greater than zero

## [3] EXPENSE
- Expense option is the route to access the actions related to EXPENSES.

### EXPENSE MENU
- Displays the options for EXPENSE.
- Add, Delete, Update, View an expense, View all user's expenses, view all groups expenses, and View all expenses

#### [1] INSERT EXPENSE
- Adds a new expense to the database.
- Asks for EXPENSE amount
- Recipient of the expense is always U1
- Asks for sender ID that is either a USER or a GROUP and must not be equal to recipient ID and must not be U1
- Asks for a valid date owed
- If the expense was paid, asks for a valid date paid
- Valid date paid must be a date that took place on or after date owed
- Automatically configures foreign keys after setting inputs
- If the expense is not paid, increases money lent and money owed by sender and recipient, respectively, by the amount of the expense
- User ID foreign key exists if a USER is either a recipient or sender of an expense. If a USER is a sender, User ID foreign key is equal to the sender ID, otherwise, equal to recipient ID
- Group ID foreign key exists if a GROUP is a sender of an expense. If a GROUP is a sender, Group ID foreign key is equal to the sender ID, otherwise, null

#### [2] DELETE EXPENSE
- Deletes an EXPENSE from the database
- An EXPENSE cannot be deleted if it is not yet paid

#### [3] UPDATE EXPENSE
- Updates amount, sender ID, recipient ID, date owed, and date paid of an EXPENSE.
- Asks for Expense ID

##### [1] UPDATE AMOUNT
- Updates an EXPENSE amount to a new amount
- Automatically updates the sender and recipient's money lent and money owed, respectively.

##### [2] UPDATE SENDER
- Updates sender ID of an EXPENSE to a new senderID
- Automatically configures foreign key changes
UPDATE SENDER (U is USER, G is GROUP)

new_sender (sender, recipient) : current_User_ID = ____, current_Group_ID = _____ => Changes on foreign keys 
U (U1, U2) : UID = U1, GID = null => UID = U
U (G1, U1) : UID = U1, GID = G1 => GID = null, UID = U

G (U1, U2) : UID = U1, GID = null => UID = U2, GID = G
G (G1, U1) : UID = U1, GID = G1 => GID = G

##### [3] UPDATE DATE OWED
- Updates date owed of an EXPENSE
- If the expense is already paid, new date owed must be a date on or before date paid  

##### [4] UPDATE DATE PAID
- Updates date paid of an EXPENSE
- If date paid is previously null, sets the expense as paid and automatically updates the money lent and money owed of the sender and receiver, respectively.
- New date paid must be a date on or after date owed

#### [4] VIEW EXPENSE
- Displays an all the information about an expense defined by an expense ID

#### [5] VIEW USER EXPENSES
- Displays all the expenses of a USER defined by a USER ID
- Displays all the expenses where the USER is a sender

#### [6] VIEW GROUP EXPENSES
- Displays all the expenses of a GROUP defined by a group ID
- Displays all the expenses where the sender is the GROUP

#### [7] VIEW ALL EXPENSES
- Displays all the recorded expenses from the database

## [4] GENERATE REPORTS
- Generate reports option is the route to access the actions related to Generating Reports.

### GENERATE REPORTS MENU
- Displays the options to generate a report

#### [1] VIEW ALL EXPENSES MADE WITHIN A MONTH
- Displays all expenses made within a specified month in tabular format
- Asks for month in digits (1-12)
- Date of an expense is the date of when the money is owed

#### [2] VIEW ALL EXPENSES MADE WITH A FRIEND
- Displays all expenses made by a friend

#### [3] VIEW ALL EXPENSES MADE WITH A GROUP
- Displays all expenses made by a group

#### [4] VIEW CURRENT BALANCE FROM ALL EXPENSES
- View Main User's or U1's current balance

#### [5] VIEW ALL FRIEND WITH OUTSTANDING BALANCE
- View all users except U1 that have money owed greater than zero.

#### [6] VIEW ALL GROUPS
- Displays all the instances of GROUP existing in the database in tabular format

#### [7] VIEW ALL GROUPS
- Displays all GROUPS that have money owed greater than zero in tabular format
