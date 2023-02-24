'''
A program that can be used by a bookstore clerk to add new books to 
the database, update book information, delete books from the database,
and search the database to find a specific book.

!!! IMPORTANT !!!
This program will only run on python 3.10 and above. Otherwise, the
program will not run and you will see an error. Please update your python
to the latest version.
'''

# import libraries
import sqlite3
import sys
from os import mkdir
from tabulate import tabulate

# Functions


def populate_table(table_name, table_values, column_names):
    ''' A function to insert values into the table 
        specify the table_name, the list of table_values and column_names'''

    # the insert command to be run by sqlite
    insert = f'''INSERT OR IGNORE INTO {table_name}{column_names}
            VALUES (?,?,?,?)'''

    # populate the table with the values.
    cursor.executemany(insert, table_values)

    # print final message if all items have been inserted
    if cursor.rowcount == len(table_values):
        print(f"\nAll books have been inserted into the {table_name} table.")
    elif cursor.rowcount < len(table_values) and cursor.rowcount > 0:
        print(
            f"\nSome new items inserted into the {table_name} table.")
    else:
        print(f"\nNo new items inserted into the {table_name} table.")

    db.commit()


def verify_input(column_name):
    '''A function that verifies user input by given column name'''

    # if the column name given is valid then proceed otherwise, ask
    # the user to enter a valid column name
    while True:

        # apart from the column name id, capitalize it to match the ones in
        # the table_columns list
        if column_name != 'id':
            column_name = column_name.capitalize()

        # break from loop if entered column name is valid
        if column_name in table_columns:
            break

        # if -1 entered return -1 to be able to return to main menu
        if column_name == '-1':
            return -1

        # print error message if no valid column entered
        print("No such column.")

        # ask user to re-enter th column
        column_name = input(
            f"Choose from {table_columns} or -1 for main menu: ").strip().lower()

    # Once the column name has been entered correctly, now checks
    # if that user given value exists in the table
    while True:
        # ask user to enter the data for book
        user_input = input(
            f"Please enter the {column_name} of the book or -1 for main menu: ").strip()

        # if user selects -1 return -1 to go bakc to main menu
        if user_input == '-1':
            return -1

        # use select to find out if the data exists
        cursor.execute(
            f'''SELECT {column_name} FROM books WHERE {column_name}=?''', (
                user_input,)
        )

        # if the data exists the select operation will return a list
        # when fetchall is called
        if len(cursor.fetchall()) != 0:
            return (column_name, user_input)

        print(f"No item with value {user_input} in {column_name}.")


def print_book(value="", selected_column=""):
    ''' Function that prints out the book details in a tabulate table.
        if a column and it's value is specified then it will print out that row.
        The parameters value and selected_column is set to "", where the whole books
        table will be printed.'''

    # if no parameters entered select all books in table
    if selected_column == "":
        cursor.execute('''SELECT * FROM books''')

    # if parameters entered then select selection only
    else:
        cursor.execute(
            f'''SELECT * FROM books WHERE {selected_column}=?''', [value])

    # print the books on screen using tabulate. Added a new line for better
    # on screen visuals.
    print("\n")
    print(tabulate(cursor.fetchall(),
                   headers=table_columns, tablefmt="fancy_grid"))


# main program
# try to connect to the databae ebookstore_db
try:
    db = sqlite3.connect('data/ebookstore_db')

# if the file does not exist in selected path
except sqlite3.OperationalError:
    # cretae a folder called data
    mkdir('data')

finally:
    # connect/create the database in the path
    db = sqlite3.connect('data/ebookstore_db')

    # get cursor object
    cursor = db.cursor()

    # create a table called books and populate it with the data only if it does
    # not exist.
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            Qty INTEGER
        )'''
    )

    # the column names in the book table
    table_columns = ('id', 'Title', 'Author', 'Qty')

    # populate the table with these values
    book_values = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                   (3002, 'Harry Potter and the Philosopher\'s Stone',
                    'J.K. Rowling', 40),
                   (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                   (3004, 'The Lord of The Rings', 'J.R.R Tolkien', 37),
                   (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

    # call the populate_table function to populate the books table
    populate_table('books', book_values, table_columns)


# the string of options to be displayed on screen
options_string = """
         Menu
--------------------------
    1.  Enter book
    2.  Update book
    3.  Delete book
    4.  Search books
    5.  View all books
    0.  Exit
--------------------------
"""

# menu items, user interaction section
while True:
    # display menu options on screen
    print(options_string)

    # ask user to enter their choice from the menu
    user_choice = input("Please enter your choice number: ").strip()

    # check that the input is a digit to be able to select a menu item
    # otherwise an erro will be displayed and ask the user to re-enter
    if user_choice.isdigit() is True:

        # match the user choice to run different cases
        match(user_choice):
            case '1':
                # Enter book

                # ask the user to enter the book title
                book_title = input(
                    "Please enter the book title or -1 for main menu: ").strip()

                # if the user chooses to return to main menu
                if book_title == "-1":
                    print("\nGoing back to main menu.")
                    continue

                # ask the user to enter the author of the book
                book_author = input(
                    "Please enter the author of the book: ").strip()

                # select the id value of the last row in table
                cursor.execute(
                    '''SELECT id FROM books WHERE id=(SELECT MAX(id) FROM books)'''
                )

                # the new book id is set to be last row id value + 1
                book_id = cursor.fetchall()[0][0] + 1

                # check that the qunatity entered by the user is a digit/number
                while True:
                    book_qty = input(
                        "Please enter the quantity of the book: ").strip()

                    if book_qty.isdigit():
                        book_qty = int(book_qty)
                        break

                    print("Please enter a number.")

                # call the populate_table function to insert into the books table
                populate_table('books', [(book_id, book_title,
                               book_author, book_qty)], table_columns)

                # displays the details of book entered on screen by calling print_book function
                print_book(book_id, 'id')

            case '2':
                # Update book

                # call search_table function to select valid id
                print("Please select the book to update by id.")
                update_book = verify_input('id')

                # if the user chooses to return to main menu
                if update_book == -1:
                    print("\nGoing back to main menu.")
                    continue

                # print informative messege along with the book detials in tabulate format
                print("\nPlease select the attribute to update.")
                print_book(update_book[1], 'id')

                # user specifies the column to be updated
                while True:
                    # ask user for the column
                    what_to_update = input(
                        f"\nChoose from {table_columns} or -1 for main menu: ").strip().lower()

                    # if the user chooses to return to main menu
                    if what_to_update == '-1':
                        print("\nGoing back to main menu.")
                        break

                    # id is unique, so user is not allowed to select the id column
                    if what_to_update == 'id':
                        print("\nYou cannot modify the id.")
                        continue

                    # checks that the column is valid
                    if what_to_update.capitalize() not in table_columns:
                        print("\nInvalid column.")
                        continue

                    # if all is satisfied, breaks out of loop
                    break

                # if the user chooses to return to main menu
                if what_to_update == '-1':
                    continue

                # ask user to enter the new data for the field selected
                new_field_data = input(
                    f"Please enter the updated data for book {what_to_update.lower()}: ")

                # update the book
                cursor.execute(
                    f'''UPDATE books SET {what_to_update}=? 
                    WHERE {update_book[0]}=?''', (new_field_data, update_book[1])
                )

                # check that it has been updated - rowcount should equal to 1
                # print out message and the details of book just updated
                if cursor.rowcount == 1:
                    print(
                        f"\n{what_to_update} has been updated to {new_field_data}")

                    print_book(new_field_data, what_to_update)

                db.commit()

            case '3':
                # Delete book

                # call search_table function to select valid id
                print("Please select the book to delete by id.")

                # verify user inputs for selected column id
                delete_book = verify_input('id')

                # if the user chooses to return to main menu
                if delete_book == -1:
                    print("\nGoing back to main menu.")
                    continue

                # execute delete in sqlite
                cursor.execute(
                    f'''DELETE FROM books WHERE {delete_book[0]}=?''', (
                        delete_book[1],)
                )

                # if item deleted rowcount woudl be 1, to double check the
                #  existence of the record, and print success or error message
                if cursor.rowcount == 1:
                    print(
                        f"\nThe book with {delete_book[0]} {delete_book[1]} has been deleted.")
                    db.commit()
                else:
                    print(
                        f"\nThe book with {delete_book[0]} {delete_book[1]} could not be deleted.")

            case '4':
                # Search books

                # ask user to specify column name to search book by
                print("Please specify by the attribute you would like to search by.")
                select_column = input(
                    f"Choose from {table_columns} or -1 for main menu: ").strip().lower()

                # verify that user inputs exist and are valid
                search_books = verify_input(select_column)

                # if -1 was selected return back to main menu
                if search_books == -1:
                    print("\nGoing back to main menu.")
                    continue

                # print the result - found book/s in tabulate format by calling
                # the print_book function
                print_book(search_books[1], search_books[0])

            case '5':
                # View all books

                # call print_book function with defualt values to print all books
                print_book()

            case '0':
                # Exits the program

                # close the connection to the ebookstore_db database
                db.close()
                print("\nConnection to the database closed.")

                # display exit message
                print("\nProgram now exiting, goodbye!")

                # Exit the program
                sys.exit()

            case _:
                # default option; if wrong option entered, error message displayed
                print("\nIncorrect entry.")

    else:
        # error message if the user did not enter a number when choosing a menu item
        print("\nPlease enter the choice as a number.")
