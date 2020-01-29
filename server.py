from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)
app.secret_key = "secretstuff"


@app.route('/')
def index():
    mysql = connectToMySQL("basic_registration")
    users = mysql.query_db("SELECT * FROM users;")
    print(users)
    return render_template("index.html", all_users = users)


@app.route('/register', methods=['POST'])
def register():
    mysql = connectToMySQL("basic_registration")
    users = mysql.query_db("SELECT * FROM users;")
    print(users)

    firstName = request.form['first_name']
    lastName = request.form['last_name']
    password = request.form['password']
    conPassword = request.form['passwordConfirm']
    isValid = True

    if len(firstName) <= 0:
        isValid = False
        flash('Please enter a first name')

    if not firstName.isalpha():
        isValid = False
        flash('Please enter a first name using only alphabetic characters')

    if len(lastName) <= 0:
        isValid = False
        flash('Please enter a last name using only alphabetic characters')

    if not lastName.isalpha():
        isValid = False

    if len(password) <= 4:
        isValid = False
        flash('Please enter a valid password (minimum 5 characters)')

    if not password == conPassword:
        isValid = False
        flash('Password doesnt match confirm password')

    
    
    if isValid == True:
        mysql = connectToMySQL("basic_registration")
        query = "INSERT INTO users (first_name, last_name, password) VALUES (%(fname)s, %(lname)s, %(pw)s);"
        data = {
            "fname": firstName,
            "lname": lastName,
            "pw": password
        }
        new_user_id = mysql.query_db(query, data)

        mysql = connectToMySQL("basic_registration")
        users = mysql.query_db("SELECT * FROM users;")
        print(users)
        flash('Success!')
        return redirect('/')
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)