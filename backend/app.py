import os                                                       # to access environement variables

from dotenv import load_dotenv                                  # to load environment variables
load_dotenv()

# To create Flask Applications and access request body and headers
from flask import Flask, request

# To facilitate ORM
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

app= Flask(__name__)


# Accessing the MySQL Database details
host= os.getenv('DB_HOST')
username= os.getenv('DB_USER')
password= os.getenv('DB_PASSWORD')
database= os.getenv('DB_NAME')

# To deal with "@" symbol in password that may pose an issue in the URI
at_symbol_index = password.find('@')                                    # Find the position of the "@" symbol in the password
password_part1 = password[:at_symbol_index]                             # Split the password into two parts before and after the "@"
password_part2 = password[at_symbol_index + 1:]
encoded_password = f"{password_part1}%40{password_part2}"               # Encode the "@" symbol in the password

# To create a MySQL URI from the above details
mysql_uri= f"mysql://{username}:{encoded_password}@{host}:3306/{database}"

app.config['SQLALCHEMY_DATABASE_URI']= mysql_uri                        # Configure Flask establish ORM with MySQL database
app.config['SQL_TRACK_MODIFICATIONS']= False                            # Configure Flask app to not track any modifications

# Creates a Database Engine
db= SQLAlchemy(app)

# Data Model
class Contact(db.Model):

    # To connect the data model to an existing table in the database
    __tablename__= 'contacts'

    # Providing a schema to the data model class matching to that of table schema
    contact_id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(50))
    phone_number= db.Column(db.String(15))
    email_address= db.Column(db.String(100))
    address= db.Column(db.String(200))

    # constructor
    def __init__(self, name, phone_number, email_address, address):
        self.name= name
        self.phone_number= phone_number
        self.email_address= email_address
        self.address= address
    
    # Transforms Contact object to dictionary/json
    def get_json(self):
        return {"Name": self.name, "Phone Number": self.phone_number, "Address": self.address, "Email Address": self.email_address}

@app.route('/view_contacts', methods= ["GET"])
def view_contacts():
    contact_list= [contact.get_json() for contact in Contact.query.all()]
    return contact_list

@app.route('/add_contact', methods= ["POST"])
def add_contact():
    body= request.get_json()
    new_contact= Contact(body['name'], body['phone_number'], body['email_address'], body['address'])
    db.session.add(new_contact)
    db.session.commit()
    return "Successful"

@app.route('/find_contact', methods= ["GET"])
def find_contact():
    value= request.headers.get("value")
    search_results= []
    if value.isalnum():
        search_results.extend(Contact.query.filter_by(name=value).all())
    else:
        search_results.extend(Contact.query.filter_by(phone_number= value).all())
    return [result.get_json() for result in search_results]

@app.route('/delete_contact/<name>', methods=['DELETE'])
def delete_contact(name):
    contact_delete= Contact.query.filter_by(name=name).first()
    db.session.delete(contact_delete)
    db.session.commit()
    return "Done"

if __name__== "__main__":
    app.run(debug=True, host='0.0.0.0', port=3003)