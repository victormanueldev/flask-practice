from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import logging as logger
import yaml

# App instantiation
app = Flask(__name__)

# Logger activation
logger.basicConfig(level='DEBUG')

# Load environment file
db  = yaml.load(open('env.yml'), Loader=yaml.FullLoader)

# Updating app config
app.config['MYSQL_HOST']        = db['mysql_host']
app.config['MYSQL_USER']        = db['mysql_user']
app.config['MYSQL_PASSWORD']    = db['mysql_password'] 
app.config['MYSQL_DB']          = db['mysql_db']

# MySQL Init
mysql = MySQL(app)

# ------------ ROUTES --------------

# Register Users
@app.route('/register', methods=['POST'])
def register():
    user = {
        'name'  : request.json['name'],
        'age'   : request.json['age'],
        'job'   : request.json['job']
    }

    with mysql.connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (name,age,job) VALUES (%(name)s, %(age)s, %(job)s);", user)
        mysql.connection.commit()
        cursor.close()

    return jsonify(user) 

# Get Users
@app.route('/users', methods=['GET'])
def get_users():
    with mysql.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users;')
        result = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return jsonify(result)


#  Get One User
@app.route('/user/<id_user>', methods=['GET'])
def get_user(id_user):
    with mysql.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE id = %s;', (id_user,))
        result = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)