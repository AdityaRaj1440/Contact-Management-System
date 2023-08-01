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
