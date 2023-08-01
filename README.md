# Contact-Management-System
A web application to view, add, find and delete contact information. Developed using Flask (Python) and MySQL with ORM support.

## Prerequisites

- Python and pip should be installed on your machine.
- MySQL Command Line Client and Workbench should be installed in your machine.

## Getting Started

1. Clone the repository/Unzip the repo:
2. Navigate to the backend directory inside project directory:

### Database Setup

3. Open MySQL Command Line Client Client and provide password.
         
            create newolen_it_service;
            use neolen_it_service;

            create table contacts(
                contact_id int auto_increment primary key,
                name varchar(50) not null unique,
                phone_number varchar(15) not null,
                email_address varchar(100),
                address varchar(200),
                CONSTRAINT non_empty_phone_number CHECK (CHAR_LENGTH(phone_number) > 0)
            );

### Backend Setup

4. Open a terminal in the backend folder and install the libraries:

             pip install -r requirements.txt
5. Create an env file in the backend folder and provide the database details and credentials as below

             DB_PASSWORD= "Enter Your MySQL Password"
             DB_USER= "Enter Your MySQL Username"
             DB_NAME= "neolen_it_service"
             DB_HOST= "localhost"

6.  Start the Flask backend server. The server will run at `http://localhost:3003`.

# Functionality and Implementations

1. Contact Class

         The Contact class is the foundation of the contact management system. It contains the following attributes:
         
         Name
         Phone number
         Email address
         Address

         These attributes are then specified with settings similar to the "contacts" table schema.

2. add_contact()

         -The add_contact() function allows users to add a new contact to the system.
         -HTTP POST method is used.
         -User has to provide the following details in JSON format in the request body:
                     "name", "phone_number", "email_address", "address"
         -The value of name and phone_number should be unique and not null/empty.
         -The data given by user is used to instantiate Contact Class and SQL Alchemy library is used to map the data to database.
         -Upon insertion, the changes are commited to finalize the addition of a new contact.

         -If there is any duplicate data or invalid data format in request, then corresponding messages will be sent as response.

3. view_contact()

         -The view_contact() function allows users to view all contacts saved in the table.
         -HTTP GET method is used.
         -Using ORM tools, Contact class is synced with the database.
         -Query and filter functions are used on Contact class to perform "Select * from contacts" query.
         -A list of all contacts will be given as response to user unless there are no contacts available, in which case, a message will be sent.

4. find_contact()

         -The find_contact() function allows users to find a contact based on either name or phone number.
         -HTTP GET method is used.
         -The search parameter is checked to know if it is a Title (Name) or a comnination of number and symbols (phone number).
         -A partial search similar to SQL's "like" operator is used to fetch a list of contacts with similar name/number.

5. delete_contact()

         -The delete_contact() function allows users to delete an existing contact by its name.
         -HTTP DELETE method is used.
         -Contact.query is used to find the contact by its name.
         -ORM tool is then used to delte the identified contact.
         -In case of any issues like deleting a contact not existing in the table, corresponding error messages will be provided.

6. Dummy Values

         -In order to showcase the working of the backend, a text file containing dummy contacts is created.
         -When the server starts running, The table will be checked to examine whether, there is any record or not.
         -In case there are no records or table present, the dummy values will be read and Contact Class will populate the table.

# Challenges Faced

- This was my first time to use ORM tool in the backend. I learned about Flask-SQLAlchemy, an ORM tool using online sources. 
- Setting up the URI for connecting to MySQL DB while taking consideration of the fact that the password may contain "@" symbol.
- Splitting the password on "@" and providing "%40" in its place helps in making a working URI.
