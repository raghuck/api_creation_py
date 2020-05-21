

Flask==0.12.2
Jinja2==2.9.6
MarkupSafe==1.0
Werkzeug==0.12.2
click==6.7
itsdangerous==0.24


Member API

create a file named api.py

Create the app routes to get, add, update and delete the members using GET, POST, PUT, PATCH and DELETE methods


from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/member', methods=['GET'])
def get_members():
   return 'This returns all the members'

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
	return 'This returns one member by ID'

@app.route('/member', methods=['POST'])
def add_member():
   return 'This adds a new member'

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
   return 'This updates a member by ID'

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
   return 'This removes a member by ID'

if __name__ == '__main__':
	app.run()
    
    
http://127.0.0.1:5000/member
	

===================================================================================================================

Add database helpers

Create a file database.py and add the connect_db and get_db in it

from flask import g
import sqlite3

def connect_db():
    sql = sqlite3.connect('sqlite3/food_log.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
    

Add below in the api.py file

import sqlite3
from database import connect_db, get_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


Test the app to make sure it works fine
http://127.0.0.1:5000/member


===================================================================================================================

Create a Database

create schema

create table members(
      id integer primary key autoincrement,
      name text not null,
      email text not null,
      level text not null
);


sqlite3 members.db < schema.sql


===================================================================================================================

Create a member

{
    "name" : "Raghu",
    "email" : "abc@gmail.com",
    "level" : "Gold"
}


from flask import Flask, g, request
import sqlite3

@app.route('/member', methods=['POST'])
def add_member():
   new_member_data =  request.get_json()
   name = new_member_data['name']
   email = new_member_data['email']
   level = new_member_data['level']
   return 'The name is {}, email is {} and the level is {}'.format(name, email, level)


@app.route('/member', methods=['POST'])
def add_member():
   new_member_data =  request.get_json()
   name = new_member_data['name']
   email = new_member_data['email']
   level = new_member_data['level']
   
   db = get_db()
   db.execute('insert into members(name, email, level) values (?, ?, ?)', [name, email, level])
   db.commit()
   
   return 'The name is {}, email is {} and the level is {}'.format(name, email, level)


===================================================================================================================

Return JSON response of member after creation

from flask import Flask, g, request, jsonify

@app.route('/member', methods=['POST'])
def add_member():
   new_member_data =  request.get_json()
   name = new_member_data['name']
   email = new_member_data['email']
   level = new_member_data['level']
   
   db = get_db()
   db.execute('insert into members(name, email, level) values (?, ?, ?)', [name, email, level])
   db.commit()
   
   member_cur = db.execute('select id, name, email, level from members where name = ?', [name])
   new_member = member_cur.fetchone()
   
   return jsonify({'id' : new_member['id'], 'name' : new_member['name'], 'email' : new_member['email'], 'level' : new_member['level']})


===================================================================================================================

Get all members

@app.route('/member', methods=['GET'])
def get_members():
   db = get_db()
   members_cur = db.execute('select id, name, email, level from members')
   members = members_cur.fetchall()
   
   return_values = []
   for member in members:
       member_dict = {}
       member_dict['id'] = member['id']
       member_dict['name'] = member['name']
       member_dict['email'] = member['email']
       member_dict['level'] = member['level']
       print(member_dict)
       
       return_values.append(member_dict)
       
   return jsonify({'members' : return_values})


GET  http://127.0.0.1:5000/member

===================================================================================================================

Get one member

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select id, name, email, level from members where id = ?', [member_id])
    member = member_cur.fetchone()
    
    return jsonify({'member' : {'id' : member['id'], 'name' : member['name'], 'email' : member['email'], 'level' : member['level']}})


GET  http://127.0.0.1:5000/member/2


===================================================================================================================

Edit a member

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
   new_member_data = request.get_json()
   
   name = new_member_data['name']
   email = new_member_data['email']
   level = new_member_data['level']
   
   db = get_db()
   db.execute('update members set name =?, email = ?, level = ? where id= ?', [name, email, level, member_id])
   db.commit()
   
   member_cur = db.execute('select id, name, email, level from members where id = ?', [member_id])
   member = member_cur.fetchone()
   
   return jsonify({'member' : {'id' : member['id'], 'name' : member['name'], 'email' : member['email'], 'level' : member['level']}})


PUT  http://127.0.0.1:5000/member/2

{
    "name" : "Ramesh",
    "email" : "hhh@gmail.com",
    "level" : "Platinum"
}

===================================================================================================================

Delete a member

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
   db = get_db()
   db.execute('delete from members where id = ?', [member_id])
   db.commit()
   
   return jsonify({'message' : 'The member has been deleted'})

===================================================================================================================

HTTP basic authentication
Select Basic auth and add username and password


@app.route('/member', methods=['GET'])
def get_members():
   db = get_db()
   members_cur = db.execute('select id, name, email, level from members')
   members = members_cur.fetchall()
   
   return_values = []
   for member in members:
       member_dict = {}
       member_dict['id'] = member['id']
       member_dict['name'] = member['name']
       member_dict['email'] = member['email']
       member_dict['level'] = member['level']
       print(member_dict)
       
       return_values.append(member_dict)
    
    username = request.authorization.username
    password = request.authorization.password
       
   return jsonify({'members' : return_values, 'username' : username, 'password' : password})



api_username = 'admin'
api_password = 'password'

@app.route('/member', methods=['GET'])
def get_members():
   db = get_db()
   members_cur = db.execute('select id, name, email, level from members')
   members = members_cur.fetchall()
   
   return_values = []
   for member in members:
       member_dict = {}
       member_dict['id'] = member['id']
       member_dict['name'] = member['name']
       member_dict['email'] = member['email']
       member_dict['level'] = member['level']
       print(member_dict)

       return_values.append(member_dict)

   username = request.authorization.username
   password = request.authorization.password

   if username == api_username and password == api_password:
   	   return jsonify({'members' : return_values, 'username' : username, 'password' : password})
       
   return jsonify({'message' : 'Authentication failed'}), 403
   

===================================================================================================================

Add authenticator route

from functools import wraps

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message' : 'Authentication failed!'}), 403
    return decorated 
        

Add the protected decorator to all the routes

@app.route('/member', methods=['GET'])
@protected
def get_members():     
        

Add the protected decorator to all the routes


===================================================================================================================

Python anywhere

https://www.pythonanywhere.com/


mkvirtualenv --python=/usr/bin/python3.4 env

pip install flask

create a repo in github
git init
add git remote command to the project directory

Next in the console clone the repo
git clone <url>

















