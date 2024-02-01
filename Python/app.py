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
    try:
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
                message = "Unsuccessful"
                return render_template('login.html', message = message)
    except Exception as e:
        message = "Unsuccessful"
        return render_template('login.html', message = message)


    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    message = ""
    try:
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
    except Exception as e:
        message = "Unsuccessful"
        return render_template('signup.html', message = message)


    return render_template('signup.html', message = message)
            
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
    try:
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
    except Exception as e:
        return render_template('main.html')
    
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

@app.route('/transactions', methods = ['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        number = request.form.get('number')
        startDate = request.form.get('start')
        endDate = request.form.get('end')
        NaccountNumber = request.form.get('Naccount')
        DaccountNumber = request.form.get('Daccount')

        if(startDate and endDate):
            # cursor.execute(f"SELECT * FROM Transactions_byDate({DaccountNumber}, {startDate}, {endDate})")
            cursor.execute("SELECT * FROM Transactions_byDate(?, ?, ?)", DaccountNumber, startDate, endDate)
            # cursor.execute("SELECT * FROM Transactions_byDate('5859831103511166', '2024-02-01', '2024-02-01')")
            for row in cursor.fetchall():
                print(row)
        if(number and NaccountNumber):
            cursor.execute("SELECT * FROM Transactions_byNumber(?, ?)", NaccountNumber, number)
            # cursor.execute("SELECT * FROM Transactions_byDate('5859831103511166', '2024-02-01', '2024-02-01')")
            for row in cursor.fetchall():
                print(row)
    
    return render_template("transactions.html")

@app.route('/accountinformationuserid', methods = ['GET', 'POST'])
def accountinformationUserID():
    if request.method == 'POST':
        userID = request.form.get('userID')

        # if(number):
        #     cursor.execute(f"SELECT * FROM Accounts_Info_byNumber({str(number)})")
        #     # cursor.execute("SELECT * FROM Transactions_byDate('5859831103511166', '2024-02-01', '2024-02-01')")
        #     for row in cursor.fetchall():
        #         print(row)
        cursor.execute(f"SELECT * FROM Accounts_Info_byID(?)", userID)
        data_from_db = cursor.fetchall()
        return render_template("accountinformationUserID.html", data_from_db = data_from_db)
    
    return render_template("accountinformationUserID.html")

@app.route('/accountinformationnumber', methods = ['GET', 'POST'])
def accountinformationNumber():
    if request.method == 'POST':
        number = request.form.get('account')

        # if(number):
        #     cursor.execute(f"SELECT * FROM Accounts_Info_byNumber({str(number)})")
        #     # cursor.execute("SELECT * FROM Transactions_byDate('5859831103511166', '2024-02-01', '2024-02-01')")
        #     for row in cursor.fetchall():
        #         print(row)
        cursor.execute(f"SELECT * FROM Accounts_Info_byNumber({number})")
        data_from_db = cursor.fetchall()
        return render_template("accountinformationNumber.html", data_from_db = data_from_db)
    
    return render_template("accountinformationNumber.html")
        
@app.route('/moneytransfer', methods = ['GET', 'POST'])
def moneytransfer():
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        amount = request.form.get('amount')

        
        cursor.execute(f"EXECUTE TransactionProcedure @P_Source_AccountNumber = {source}, @P_Destination_AccountNumber = {destination}, @P_Amount = {amount}")
        conn.commit()
        
      

    return render_template('moneytransfer.html')

if __name__ == "__main__":
    app.run(debug=True)