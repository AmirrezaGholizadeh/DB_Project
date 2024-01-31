from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Amirreza:Amirreza?!1381@localhost/db_name?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Amirbyhimself;DATABASE=BANK;')
cursor = conn.cursor()

db = SQLAlchemy(app)

USERNAME = []

# class User(db.Model):
#     username = db.Column(db.String(25),unique=True ,primary_key=True, nullable=False)
#     password = db.Column(db.String(256), nullable=False)
#     name = db.Column(db.String(50))
#     lastname = db.Column(db.String(50))
#     email = db.Column(db.String(50))
#     phone_number = db.Column(db.String(11))
#     salt = db.Column(db.String(36), primary_key=True,unique=True, nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute(f"EXECUTE Log_In @P_Username = {username}, @P_Current_Password = {password}")
        conn.commit()
        cursor.execute('select * from Messages')

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]

        cursor.execute('DELETE from Messages')
        conn.commit()

        if(result == 'Correct'):
            USERNAME.append(username)
            return redirect('/')
        else:
            print("Try again")


    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        cursor.execute(f"EXECUTE Register @P_Username = {username}, @P_Password = {password}, @P_Name = {name}, @P_Lastname = {lastname}, @P_Email = {email}, @P_Phone_Number = {phone}")
        conn.commit()
        return redirect('/login')

    return render_template('signup.html')
            
# @app.route('/signup', methods = ['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         name = request.form.get('name')
#         lastname = request.form.get('lastname')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         password = request.form.get('password')

#         cursor.execute(f"EXECUTE Register @P_Username = {username}, @P_Password = {password}, @P_Name = {name}, @P_Lastname = {lastname}, @P_Email = {email}, @P_Phone_Number = {phone}")
#         conn.commit()
#         return redirect('main.html')

#     return render_template('signup.html')

@app.route('/', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        cursor.execute(f"EXECUTE Register @P_Username = {username}, @P_Password = {password}, @P_Name = {name}, @P_Lastname = {lastname}, @P_Email = {email}, @P_Phone_Number = {phone}")
        conn.commit()
        return redirect('/')

    return render_template('main.html')

@app.route('/newaccount', methods = ['GET', 'POST'])
def newaccount():
    global USERNAME
    if request.method == 'POST':
        print("SADSADASDasd")
        number = request.form.get('account')
        print(USERNAME[0])
        print("SADSADASDasd")
        cursor.execute(f"EXECUTE New_Account @P_Account_Number = {str(number)}, @P_Username = {USERNAME[0]}, @P_Amount = {0}, @P_Block = {0}, @P_Loan_Status = {0}")
        conn.commit()
        return redirect('/')
     

    return render_template('newaccount.html')

@app.route('/accountinformation', methods = ['GET', 'POST'])
def accountinformation():
    if request.method == 'POST':
        number = request.form.get('number')
        startDate = request.form.get('start')
        endDate = request.form.get('end')
        NaccountNumber = request.form.get('Naccount')
        DaccountNumber = request.form.get('Daccount')

        print(startDate)

        if(startDate and endDate):
            cursor.execute(f"SELECT * FROM Transactions_byDate({DaccountNumber}, {startDate}, {endDate})")
            for row in cursor.fetchall():
                print(row)
        
      

    return render_template('accountinformation.html')
if __name__ == "__main__":
    app.run(debug=True)