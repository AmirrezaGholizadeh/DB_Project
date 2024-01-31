import pyodbc

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Amirbyhimself;DATABASE=Bank;')

print("db connect")
cursor = conn.cursor()
cursor.execute("EXECUTE Register @P_Username = 'RAZ', @P_Password = '123', @P_Name = 'Abas', @P_Lastname = 'Rezaei', @P_Email = 'Soltani@gmail', @P_Phone_Number = '09133865044'")
conn.commit()
cursor.execute("select * from Users")
for row in cursor.fetchall():
    print(row)