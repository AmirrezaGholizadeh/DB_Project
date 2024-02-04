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
                USERNAME.clear()
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
    
    return render_template('main.html')

@app.route('/changepassword', methods = ['GET', 'POST'])
def changePassword():
    if request.method == 'POST':
        currentPassword = request.form.get('current_password')
        newPassword = request.form.get('new_password')
      
        cursor.execute(f"EXECUTE Change_Password @P_Username = {USERNAME[0]}, @P_Current_Password = {currentPassword}, @P_New_Password = {newPassword}")
        conn.commit()
      
        cursor.execute('select * from Messages')

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]

        cursor.execute('DELETE from Messages')
        conn.commit()

        if(result == 'Correct'):
            message = "Successful"
            return render_template('changepass.html', message = message)
        else:
            message = "Unsuccessful"
            return render_template('changepass.html', message = message)
     

    return render_template('changepass.html')

@app.route('/newaccount', methods = ['GET', 'POST'])
def newaccount():
    if request.method == 'POST':
    
        number = request.form.get('account')
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

        cursor.execute("SELECT * FROM Transactions_byDate(?, ?, ?, ?)", accountNumber, startDate, endDate, USERNAME[0])
    
        data_from_db = cursor.fetchall()
        return render_template("transactionsDate.html", data_from_db = data_from_db)
    
    return render_template("transactionsDate.html")

@app.route('/transactionsnumber', methods = ['GET', 'POST'])
def transactionsNumber():
    if request.method == 'POST':
        number = request.form.get('number')
        accountNumber = request.form.get('account')

      
       
        cursor.execute("SELECT * FROM Transactions_byNumber(?, ?, ?)", accountNumber, number, USERNAME[0])
        data_from_db = cursor.fetchall()
        return render_template("transactionsNumber.html", data_from_db = data_from_db)
    
    return render_template("transactionsNumber.html")

@app.route('/accountinformationuserid', methods = ['GET', 'POST'])
def accountinformationUserID():

    cursor.execute(f"SELECT * FROM Accounts_Info_byID(?)", USERNAME[0])
    data_from_db = cursor.fetchall()
    return render_template("accountinformationUserID.html", data_from_db = data_from_db)
    

@app.route('/accountinformationnumber', methods = ['GET', 'POST'])
def accountinformationNumber():
    if request.method == 'POST':
        number = request.form.get('account')


        cursor.execute(f"SELECT * FROM Accounts_Info_byNumber(?, ?)",number, USERNAME[0])
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
                cursor.execute(f"EXECUTE TransactionProcedure @P_Source_AccountNumber = {source}, @P_Destination_AccountNumber = {destination}, @P_Amount = {amount}, @P_Username = {USERNAME[0]}")
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

@app.route('/accountowner', methods = ['GET', 'POST'])
def accountowner():
    if request.method == 'POST':
        number = request.form.get('account')
    cursor.execute(f"SELECT dbo.Account_Owner(?)", number)

    for row in cursor.fetchall():
        print(row[0])
        result = row[0]


    if(result == None):
        ownerMessage = 'Not found'
        return render_template('moneytransfer.html', ownerMessage = ownerMessage)
    else:
        ownerMessage = result
        return render_template('moneytransfer.html', ownerMessage = ownerMessage)
            
   
    
@app.route('/generatepass', methods = ['GET', 'POST'])
def generatepass():
    if request.method == 'POST':
        random_number = random.randint(100000,999999)
        PASSWORD.append(random_number)
        passwordMessage = random_number
        return render_template('moneytransfer.html', passwordMessage = passwordMessage)

@app.route('/loans', methods = ['GET', 'POST'])
def loans():
    return render_template('loans.html')

@app.route('/getloan', methods = ['GET', 'POST'])
def getloan():
    try:
        if request.method == 'POST':
            number = request.form.get('account')


            cursor.execute(f"EXECUTE Get_New_Loan @P_Account_Number = {number}, @P_Username = {USERNAME[0]}")
            conn.commit()
            cursor.execute('select * from Messages')

            for row in cursor.fetchall():
                print(row[0])
                result = row[0]

            cursor.execute('DELETE from Messages')
            conn.commit()

            if(result == 'Successfully'):
                message = "Successful"
                return render_template('getloan.html', message = message)
            elif (result == 'You must finish your payments or your account is block'):
                message = "You must finish your payments or your account is block"
                return render_template('getloan.html', message = message)
            else:
                message = "Unsuccessful"
                return render_template('getloan.html', message = message)
    except Exception as e:
        message = "Unsuccessful"
        return render_template('getloan.html',  message = message)
            
    
    return render_template("getloan.html")

@app.route('/loanscore', methods = ['GET', 'POST'])
def loanscore():
    if request.method == 'POST':
        number = request.form.get('loanscore_account')


        cursor.execute(f"SELECT dbo.Get_LoanScore(?, ?)", number, USERNAME[0])

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]


        if(result > 0):
            loanscore = result
            return render_template('getloan.html', loanscore = loanscore)
        else:
            loanscore = "Unsuccessful"
            return render_template('getloan.html', loanscore = loanscore)
            
    
    return render_template("getloan.html")

@app.route('/loaninformationuserid', methods = ['GET', 'POST'])
def loaninformationUserID():


    cursor.execute(f"SELECT * FROM Loan_List_byUsername(?)", USERNAME[0])
    data_from_db = cursor.fetchall()
    return render_template("loaninformationUserID.html", data_from_db = data_from_db)
    

@app.route('/paymentinformation', methods = ['GET', 'POST'])
def paymentinformation():
    if request.method == 'POST':
        number = request.form.get('account')


        cursor.execute(f"SELECT * FROM Info_Payment_byNumber(?, ?)", number, USERNAME[0])
        data_from_db = cursor.fetchall()
        return render_template("paymentinfo.html", data_from_db = data_from_db)
    
    return render_template("paymentinfo.html")

@app.route('/payinstallment', methods = ['GET', 'POST'])
def payinstallment():
    if request.method == 'POST':
        number = request.form.get('account')

        cursor.execute(f"EXECUTE Pay_Loan @P_Account_Number = {number}, @P_Username = {USERNAME[0]}")
        conn.commit()
        cursor.execute('select * from Messages')

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]

        cursor.execute('DELETE from Messages')
        conn.commit()

        if(result == 'Successfully Paid'):
            message = "Successful"
            return render_template('paymentinfo.html', message = message)
        elif (result == 'Dont have enough money!'):
            message = 'Dont have enough money!'
            return render_template('paymentinfo.html', message = message)
        else:
            message = "Unsuccessful"
            return render_template('paymentinfo.html', message = message)
            
    
    return render_template("loaninformationNumber.html")

@app.route('/blockaccount', methods = ['GET', 'POST'])
def blockaccount():
    if request.method == 'POST':
        number = request.form.get('account')

        UNBLOK_ACCOUNTNUMBER.append(number)

        cursor.execute(f"EXECUTE Block @P_Account_Number = {number}, @P_Username = {USERNAME[0]}")
        conn.commit()
        cursor.execute('select * from Messages')

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]

        cursor.execute('DELETE from Messages')
        conn.commit()

        if(result == 'Correct!'):
            message = "Successfully blocked"
            return render_template('blockaccount.html', message = message)
        elif (result == 'Wrong!'):
            message = "Unsuccessful"
            return render_template('blockaccount.html', message = message)
    
    return render_template("blockaccount.html")

@app.route('/unblockaccount', methods = ['GET', 'POST'])
def Unblockaccount():
    if request.method == 'POST':
        number = request.form.get('accountToUnblock')
        print(number)
        cursor.execute(f"EXECUTE UNblock @P_Account_Number = {number}, @P_Username = {USERNAME[0]}")
        conn.commit()
        cursor.execute('select * from Messages')

        for row in cursor.fetchall():
            print(row[0])
            result = row[0]

        cursor.execute('DELETE from Messages')
        conn.commit()

        if(result == 'Correct!'):
            unblockMessage = "Successfully unblocked"
            return render_template('blockaccount.html', unblockMessage = unblockMessage)
        elif (result == 'Wrong!'):
            unblockMessage = "Unsuccessful"
            return render_template('blockaccount.html', unblockMessage = unblockMessage)
    
    return render_template("blockaccount.html")

if __name__ == "__main__":
    app.run(debug=True)