import os                                                       # to access environement variables

from dotenv import load_dotenv
import sqlalchemy                                               # to load environment variables
load_dotenv()

# To create Flask Applications and access request body and headers
from flask import Flask, request, jsonify

# To facilitate ORM
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

# To read dummy data
def read_contacts_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Skip the header line
    lines = lines[1:]

    contacts = []
    for line in lines:
        data = line.strip().split(',', maxsplit=3)
        name, phone_number, email_address, address = data
        contact = Contact(name=name, phone_number=phone_number, email_address=email_address, address=address)
        contacts.append(contact)

    return contacts

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
    name= db.Column(db.String(50), nullable= False, unique= True)
    phone_number= db.Column(db.String(15), nullable= False, unique= True)
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

# To provide constraint for not taking empty phone number
Contact.__table__.append_constraint(db.CheckConstraint('LENGTH(phone_number) >= 1'))

# To fetch all the contacts
@app.route('/view_contacts', methods= ["GET"])
def view_contacts():
    contact_list= [contact.get_json() for contact in Contact.query.all()]
    if len(contact_list)<0:
        contact_list= "No contacts found!!"
        return jsonify({"message": contact_list}), 404
    return contact_list

# To add a new contact
@app.route('/add_contact', methods= ["POST"])
def add_contact():
    body= request.get_json()
    try:
        new_contact= Contact(body['name'], body['phone_number'], body['email_address'], body['address'])
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact Added Successfully"}), 201
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"message":"Duplicate name or phone numbers are not allowed"}), 409
    except sqlalchemy.exc.OperationalError:
        return jsonify({"message":"Phone number should not be empty"}), 422
    except KeyError:
        return jsonify({"Invalid data format. Make sure to include all required fields (name, phone_number, email, address)."}), 400
    except Exception as e:
        return jsonify({"mesage": "An Error Occurred "+e})

# To find a contact by name or phone number
@app.route('/find_contact', methods= ["GET"])
def find_contact():
    value= request.headers.get("value")
    search_results= []
    print("Name",value)
    if value.istitle():
        print("coming here")
        print("checking",Contact.query.filter(Contact.name.like(f'%{value}%')).all())
        search_results.extend(Contact.query.filter(Contact.name.like(f'%{value}%')).all())
    else:
        search_results.extend(Contact.query.filter(Contact.phone_number.like(f'%{value}%')).all())
    res= [result.get_json() for result in search_results]
    if len(res)>0:
        return res
    else:
        return jsonify({"message":"No Contacts Found"}), 404

# To delete a contact by name
@app.route('/delete_contact/<name>', methods=['DELETE'])
def delete_contact(name):
    contact_delete= Contact.query.filter_by(name=name).first()
    try:
        db.session.delete(contact_delete)
        db.session.commit()
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return jsonify({"Contact to be deleted not found."}), 404
    except Exception as e:
        return jsonify({"mesage": "An Error Occurred "+e})
    return jsonify({"message": "Contact Deleted"}), 201

if __name__== "__main__":
    with app.app_context():
        # Initialize the database
        db.create_all()

        if(len(view_contacts())==0):
            # Read contacts from the text file
            contacts = read_contacts_from_file('./backend/samples/dummy_contacts.txt')

            # Save contacts to the database
            for contact in contacts:
                db.session.add(contact)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=3003)