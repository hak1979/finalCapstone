# A database driven program for a bookstore

## The features of the program

The program allows a user/clerk to:
* item add new books to the database
* item update book information
* item delete books from the database
* item search the database to find a specific book
* item view all books in the database

## Important information before running the program
This program uses the match-case feature and it will only run on python 3.10 and above. 
Otherwise, theprogram will not run and you will see an error. Please update your python
to the latest version.

The program also utilises the sqlite3 and tabulate libraries. These will have to be
installed into your python environment before you run the program. 

## The database
On initial run of the program, it will create a folder called "data" if it doesn't exist
and within it it will create a database called ebookstore_db. 

The database stores the book data in the books table that includes the (unique) id,
Title, Author and quantityas Qty. 

![Image of books table](/images/table_example.jpg)

## How to run the program
* item Clone or download the bookstore.py file onto a local folder of your choice 
* item Start your python environment that includes tabulate and sqlite3
* item In the terminal navigate to the folder where you have stored bookstore.py
* item Run the program by typing "python bookstore.py" or "python3 bookstore.py" depending on your setup
* item the program runs on the terminal, please follow the instructions onscreen. 

## How to use the program
When the program is run the user is presented with a menu as below.

![Image of menu options](/images/menu_example.jpg)

The user can select the option by entering the number only. No other inouts will be accepted. 

### Menu 1: Entering a new book into the data base
The program will ask the user to enter the new book details one by one. If the user has entered
this menu by mistake or changed their mind, they can exit to main menu by entering '-1'.

Once all the required fields for the new book is entered, a new entry will be added to the books table.
The new book will have an automatically generated id number which will follow on from the last book's id.

### Menu 2: Updating a value
The user can select the book by id only. Again there is theoption to enter -1 to exit to main menu.
The book information will be displayed only if the id is valid. Then the user is prompted to sepcify
the field to be updated. Once updated the updated book entry will be displayed. 

### Menu 3: Delete a book
The user can only delete a book by id number only. 

### Menu 4: Search for a book
The user may search for a book by any field of their choice. If the input matches an item in the table
then it will return a valid result, otherwise an error message will be seen. 

### Menu 5: View all books
This menu will display all the books in the table on screen using tabulate.

### Menu 0: Exit
When this option is selected, the database will be closed and the program will exit. 
