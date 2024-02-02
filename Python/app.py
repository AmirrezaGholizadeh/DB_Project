from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pyodbc, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Amirreza:Amirreza?!1381@localhost/db_name?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Amirbyhimself;DATABASE=BANK;')
cursor = conn.cursor()

db = SQLAlchemy(app)

USERNAME = []
PASSWORD = []


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

@app.route('/transactionsdate', methods = ['GET', 'POST'])
def transactionsDate():
    if request.method == 'POST':
        startDate = request.form.get('start')
        endDate = request.form.get('end')
        accountNumber = request.form.get('account')

        cursor.execute("SELECT * FROM Transactions_byDate(?, ?, ?)", accountNumber, startDate, endDate)
    
        data_from_db = cursor.fetchall()
        return render_template("transactionsDate.html", data_from_db = data_from_db)
    
    return render_template("transactionsDate.html")

@app.route('/transactionsnumber', methods = ['GET', 'POST'])
def transactionsNumber():
    if request.method == 'POST':
        number = request.form.get('number')
        accountNumber = request.form.get('account')

      
       
        cursor.execute("SELECT * FROM Transactions_byNumber(?, ?)", accountNumber, number)
        data_from_db = cursor.fetchall()
        return render_template("transactionsNumber.html", data_from_db = data_from_db)
    
    return render_template("transactionsNumber.html")

@app.route('/accountinformationuserid', methods = ['GET', 'POST'])
def accountinformationUserID():
    if request.method == 'POST':
        userID = request.form.get('userID')

        cursor.execute(f"SELECT * FROM Accounts_Info_byID(?)", userID)
        data_from_db = cursor.fetchall()
        return render_template("accountinformationUserID.html", data_from_db = data_from_db)
    
    return render_template("accountinformationUserID.html")

@app.route('/accountinformationnumber', methods = ['GET', 'POST'])
def accountinformationNumber():
    if request.method == 'POST':
        number = request.form.get('account')


        cursor.execute(f"SELECT * FROM Accounts_Info_byNumber({number})")
        data_from_db = cursor.fetchall()
        return render_template("accountinformationNumber.html", data_from_db = data_from_db)
    
    return render_template("accountinformationNumber.html")
        
@app.route('/moneytransfer', methods = ['GET', 'POST'])
def moneytransfer():
    try:
        if request.method == 'POST':
            source = request.form.get('source')
            destination = request.form.get('destination')
            amount = request.form.get('amount')
            password = request.form.get('password') 
        
            result = ""
            if(str(password) == str(PASSWORD[-1])):
                cursor.execute(f"EXECUTE TransactionProcedure @P_Source_AccountNumber = {source}, @P_Destination_AccountNumber = {destination}, @P_Amount = {amount}")
                conn.commit()
                cursor.execute('select * from Messages')

                for row in cursor.fetchall():
                    print(row[0])
                    result = row[0]

                cursor.execute('DELETE from Messages')
                conn.commit()

            if(result == "Correct"):
                PASSWORD.clear()
                message = "Successful"
                return render_template('moneytransfer.html', message = message)
            else: 
                PASSWORD.clear()
                message = "Unsuccessful"
                return render_template('moneytransfer.html', message = message)
    except Exception as e:
        message = "Unsuccessful"
        return render_template('moneytransfer.html',  message = message)

    return render_template('moneytransfer.html')

@app.route('/generatepass', methods = ['GET', 'POST'])
def generatepass():
    if request.method == 'POST':
        random_number = random.randint(100000,999999)
        PASSWORD.append(random_number)
        passwordMessage = random_number
        return render_template('moneytransfer.html', passwordMessage = passwordMessage)

if __name__ == "__main__":
    app.run(debug=True)