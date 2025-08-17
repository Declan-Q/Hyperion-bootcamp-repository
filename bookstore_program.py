
import sqlite3

ebookstore = sqlite3.connect("ebookstore.db")
cursor = ebookstore.cursor()

# Dictionary of the table column names.
book_table_columns = {1:"id", 2:"title", 3:"author", 4:"qty"}


def new_book():
    """ Adds a new book to the book table in the ebookstore database.

    Adds a new book to the book table. Asks the user for the book
    name, author and quantity which are saved with a id number to the
    table.
    """
    print("-----------------")
    book_name = input("What is the title of the book you want to add?\n")
    book_author = input("Who is the author of this book?\n")
    # Asks for qty and coverts it to a positive integer.
    while True:
        try:
            qty =  int(input("What is the current inventory amount of these"
                             "books?\n"))
        except ValueError:  # Error produced if qty is not an integer.
            print("Sorry I don't think that's a valid input, please "
                  "enter a integer.\n")
            continue  # Re-asks for qty if it's not an integer.
        if qty >= 0:
            break
        else:
            print("Sorry you can't have a negative number for qty, please "
                  "input a positive qty.")

    # Finds the current highest id number and adds 1 to it for the new
    # id number.
    max_value_object = cursor.execute("""SELECT MAX(id) FROM book""")
    new_id = ""
    for id in max_value_object:  # Gets the number from the object.
        new_id = id[0] + 1  # Takes the max id and adds 1 to it.
    try: # Adds the new book to the database.
        cursor.execute("""INSERT INTO book(id, title, author, qty) VALUES
                       (?,?,?,?)""", (new_id, book_name, book_author, qty))
    except Exception as error:  # If it fails the user is informed.
        ebookstore.rollback()
        print("Sorry that book couldn't be uploaded due to the information"
              f"you inputted. The error you have created is {error}")

    ebookstore.commit()
    print(f"The book {book_name} has been added.")


def update_book():
    """ Adds a new book to the book table in the ebookstore database.
    
    This updates a book by asking the user what information
    they want to update and then updating the database.
    """
    while True:
        print_book_table()  # Shows user the book table info.
        try:  # User selects a book to update via selecting the ID.
            book_id = int(input("-----------------\n"
                "Please select a book ID from the current"
                " books on record to update?\n"))
        except ValueError:
            print("Sorry that isn't a valid value. Please use a integer.\n")
            continue
        if id_in_table(book_id) is False:  # Checks if id in the table.
            print("Sorry that's not a valid id, please try again.")
            continue

        # This prints the book table columns and asks the user to pick
        # one.
        while True:
            for key, value in book_table_columns.items():
                print(f"{key}. {value}")  # Prints numbered columns.
            column_number = input("What about this book would you like to"
                                 " update?\n")
            try:
                # Finds the column name which the number belongs to.
                column_name = book_table_columns[int(column_number)]
                break
            except ValueError:
                print("Sorry that's not on the list of columns.")
                continue

        # Asks the user for the new value to update into the table. If
        # the user is updating ID or qty then the input is checked if
        # its a int and is positive.
        while True:
            update_value = input("What value do you want to change "
                                 f"{column_name} to?\n")
            if (column_name == "id" or column_name == "qty"):
                try:
                    update_value =  int(update_value)
                except ValueError:  # Error produced if not int.
                    print("\nSorry I don't think that's a valid input, "
                          "please enter an integer.")
                    continue
                if update_value >= 0:  # Checks number is positive.
                    break
                else:
                    print("Sorry you can't have a negative number, please "
                           "input a positive number.")
            else:  # Int checking skipped if column isn't id or qty.
                break

        # If statements are used to select the appropriate column and
        # the value to updated.
        try:
            if column_name == "id":  # Updates id.
                cursor.execute("""UPDATE book SET id = ? WHERE id = ?""",
                            (update_value, book_id))
            elif column_name == "title":  # Updates title.
                cursor.execute("""UPDATE book SET title = ? WHERE id = ?""",
                            (update_value, book_id))
            elif column_name == "author":  # Updates author.
                cursor.execute("""UPDATE book SET author = ? WHERE id =?""",
                            (update_value, book_id))
            elif column_name == "qty":  # Updates qty.
                cursor.execute("""UPDATE book SET qty = ? WHERE id = ?""",
                            (update_value, book_id))
            ebookstore.commit()
            print("Book details updated!")
        except:  # If the update errors the user is told.
            print("Sorry the value you added isn't valid. Please try again.")
        return


def print_book_table():
    """This shows the current books in the book table to the user"""
    print("-----------------\n"
          "This is a list of the current information stored on the\n"
          "database, showing (in order) book id, book title, book author\n"
          "and amount in current inventory.\n")
    # This selects the info from book table.
    book_table = cursor.execute("SELECT * FROM book")
    for row in book_table:  # Prints book table to user.
        print(row)


def delete_book():
    """Deletes a specified ID number in the book table on the ebookstore DB.
    
    Asks user for a ID number, checks that ID number is in the book table and 
    then deletes that number.
    """
    while True:
        print_book_table()  # Shows user the books and their information.
        # Asks the user for a ID number and tries to convert it to a
        # integer.
        try:
            delete_id = int(input("Please state the book ID want to "
                                  "delete:\n"))
        except ValueError:  # Errors if the user didn't input an int.
            print("Sorry I don't think that's a valid number.")
            continue  # User has to re-enter id if not an integer.

        # The id is compared to all the id's in the table to check it
        # exists.
        if id_in_table(delete_id) is True:  # Checks if id in table.
            cursor.execute("""DELETE FROM book WHERE id=?""",
                              (delete_id,))
            ebookstore.commit()  # Id is deleted and user told.
            print(f"The book with ID number: {delete_id} has been "
                   "deleted")
            return
        else:
            print("Sorry there is no book with that ID number.")
            return


def id_in_table(id_to_check):
    """Checks to see if the id is in the book table."""
    book_ids = cursor.execute("""SELECT id FROM book""")
    for id in book_ids:
        if id[0] == id_to_check:  # If table has id then returns True.
            return True
    return False  # If id can't be found in table returns False.


def search():
    """ Searches for a specified value in a specified column
    
    Searches for a value in a column in the book table, the value and 
    column are specified by the user.
    """
    print("-----------------\n"
          "This is a list of columns you can search from.")
    # Asks the user to pick a column to search by providing a numbered\\
    # list of columns.
    while True:
        for key, value in book_table_columns.items():
            print(f"{key}. {value}")  # Prints numbered columns.
        # User inputs column number which is converted to the column
        # name.
        column_number = input("Please state what column you want to search.\n")
        try:
            column_name = book_table_columns[int(column_number)]
            break
        except:
            print("Sorry you need to enter the number of the "
            "column you want.")
            continue
    search_info = input("What information would you like to search for?\n")

    # Searches the column specified by the user.
    if column_name == "id":
        cursor.execute("""SELECT * FROM book WHERE id = ?""",
                       (search_info,))
    elif column_name == "title":
        cursor.execute("""SELECT * FROM book WHERE title = ?""",
                       (search_info,))
    elif column_name == "author":
        cursor.execute("""SELECT * FROM book WHERE author = ?""",
                       (search_info,))
    elif column_name == "qty":
        cursor.execute("""SELECT * FROM book WHERE qty = ?""",
                       (search_info,))
    else:
        print("Sorry you haven't entered a correct column.")
    # Pulls all the rows with matches for the searched info.
    answer = cursor.fetchall()
    if answer == []:  # If there are no matches the user is told.
        print("\nSorry there are no rows with that information.")
    else:  # If there are matches the user is told.
        print(f"\nHere are the rows which have {search_info} in the "
              f"{column_name}:\n")
        for row in answer:  # Pulls each row (record) from the answer.
            counter = 0
            for info in row:  # Pulls individual info from the record.
                counter += 1
                # Results printed to the user.
                print(f"{book_table_columns[counter]}: {info}, ")
            print("")

# Creates table called book to store book information.
cursor.execute("""CREATE TABLE IF NOT EXISTS book
             (id INT NOT NULL,
             title VARCHAR,
             author VARCHAR, 
             qty INT, 
             PRIMARY KEY (id))""")
ebookstore.commit()



# Inserts into the book table 6 books
cursor.execute('''INSERT OR IGNORE INTO book (id, title, author, qty) VALUES
                    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
                    (3002, "Harry Potter and the Philosopher's Stone", 
                    "J.K. Rowling", 40),
                    (3003, "The Lion, the Witch and the Wardrobe",
                    "C. S. Lewis", 25),
                    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
                    (3006, "The Great Gatsby", "F. Scott Fitzgerald", 25)''')
ebookstore.commit()


# Menu allowing the user to select their desired action.
while True:
    try:
        option = int(input("-----------------\n"
        "Welcome to the ebookstore database. Please select an option from the\n"
        "list below:\n"
        "1. Add a new book to the ebookstore.\n"
        "2. Update a book's information.\n"
        "3. Delete a book from the ebookstore.\n"
        "4. Search for a book.\n"
        "5. Show all current books in file.\n"
        "0. Quit\n"))
    except ValueError:
        print("Sorry you need to enter a integer.")
        continue
    if option == 1:
        new_book()
    elif option == 2:
        update_book()
    elif option == 3:
        delete_book()
    elif option == 4:
        search()
    elif option == 5:
        print_book_table()
    elif option == 0:
        exit()
    else:
        print("Sorry you need to enter a number from the list")

