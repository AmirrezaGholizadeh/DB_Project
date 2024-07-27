
CREATE PROCEDURE Register(
@P_Username varchar(20),
@P_Password VARCHAR(256),
@P_Name VARCHAR(50),
@P_Lastname VARCHAR(50),
@P_Email VARCHAR(50),
@P_Phone_Number VARCHAR(11)
)
AS
BEGIN
    DECLARE @salt UNIQUEIDENTIFIER;
    SET @salt = NEWID();
    DECLARE @hashedPassword VARBINARY(256); 
    SET @hashedPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_Password, @salt) AS varchar(MAX)));

    IF NOT EXISTS(SELECT * FROM Users WHERE @P_Username = username)
        BEGIN 
            INSERT INTO Users
            VALUES (@P_Username, @hashedPassword, @P_Name, @P_Lastname, @P_Email, @P_Phone_Number, @salt);
        END;
    ELSE
        BEGIN
           
            SELECT * FROM Users
            
        END;
END;
-------------------

CREATE PROCEDURE Log_In(
@P_Username VARCHAR(20),
@P_Current_Password VARCHAR(256)
)
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM Users WHERE @P_Username = username)
    BEGIN
        INSERT INTO Messages 
        VALUES('The username doesn''t exist!')
    END;

    ELSE
    BEGIN
        DECLARE @User_Salt UNIQUEIDENTIFIER;
        DECLARE @Stored_Password VARCHAR(256);
        SELECT @User_Salt = salt , @Stored_Password = password FROM Users WHERE @P_Username = username;
        DECLARE @hashedPassword VARBINARY(256); 
        SET @hashedPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_Current_Password, @User_Salt) AS varchar(MAX)));

        IF @Stored_Password = @hashedPassword
        BEGIN
            INSERT INTO Messages 
            VALUES('Correct')
        END;
        ELSE
        BEGIN
            INSERT INTO Messages 
            VALUES('Discorrect!')
        END;
    END;
END;




CREATE PROCEDURE Change_Password(
@P_Username VARCHAR(20),
@P_Current_Password VARCHAR(256),
@P_New_Password VARCHAR(256)
)
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM Users WHERE @P_Username = username)
    BEGIN
        INSERT INTO Messages
        VALUES("Username doesnt exist")
    END;

    ELSE
    BEGIN
        DECLARE @User_Salt UNIQUEIDENTIFIER;
        DECLARE @Stored_Password VARCHAR(256);
        SELECT @User_Salt = salt , @Stored_Password = password FROM Users WHERE @P_Username = username;
        DECLARE @hashedPassword VARBINARY(256); 
        SET @hashedPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_Current_Password, @User_Salt) AS varchar(MAX)));

        IF @Stored_Password = @hashedPassword
        BEGIN
            DECLARE @hashedNewPassword VARBINARY(256); 
            SET @hashedNewPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_New_Password, @User_Salt) AS varchar(MAX)));
            UPDATE Users
            set password = @hashedNewPassword
            WHERE @P_Username = username
            INSERT INTO Messages
            VALUES("Correct")
        END;
        ELSE
        BEGIN
            INSERT INTO Messages
            VALUES("Discorrect")
        END;
    END;
END;

CREATE PROCEDURE New_Account(
@P_Account_Number VARCHAR(16),
@P_Username VARCHAR(25),
@P_Amount DECIMAL(15,2),
@P_Block BIT,
@P_Loan_Status BIT
)
AS
BEGIN
    DECLARE @Current_Date DATE = CAST(GETDATE() AS DATE);
    INSERT INTO Accounts
    VALUES(@P_Account_Number, @P_Username, @P_Amount, @P_Block, @P_Loan_Status,@Current_Date);
END;



CREATE FUNCTION Accounts_Info_byID(
@P_Username VARCHAR(25)
)
RETURNS TABLE
AS 
RETURN (SELECT * FROM Accounts WHERE @P_Username = username);



CREATE FUNCTION Account_Owner(
@P_Account_Nummber VARCHAR(16)
)
RETURNS VARCHAR(100)
AS 
BEGIN
    DECLARE @fullName VARCHAR(100)
    SELECT @fullName = (name +' '+ lastname) 
    FROM Users, Accounts
    WHERE @P_Account_Nummber = account_number AND Accounts.username = Users.username
    RETURN (@fullName)
END;




CREATE FUNCTION Loan_List_byUsername(
@P_username VARCHAR(25)
)
RETURNS TABLE
AS
RETURN (select * from Loans where @P_username = username);




CREATE PROCEDURE Get_New_Loan(
@P_Account_Number VARCHAR(16),
@P_Username VARCHAR(25)
)
AS
BEGIN
    DECLARE @tmp INTEGER;
    @tmp = dbo.Get_LoanScore(@P_Account_Number, @P_Username)
    IF NOT EXISTS(select * from Accounts where @P_Account_Number = account_number  AND @P_Username = username) AND @tmp < 1
        BEGIN
            INSERT INTO Messages
            VALUES('The username doesnt exist or you can not get loan on this account')
        END
    ELSE
        BEGIN
            IF EXISTS (select * 
                from Accounts 
                where @P_Account_Number = account_number and (loan_status = 1 or block =1))
                BEGIN
                    INSERT INTO Messages
                    VALUES('You must finish your payments or your account is block')
                END;
            ELSE
                BEGIN
                    DECLARE @P_amount INTEGER;
                    SET @P_amount = dbo.Get_LoanScore(@P_Account_Number, @P_Username)
                    SET @P_amount = @P_amount + ((@P_amount*20)/100)
                    -- Add new loan
                    UPDATE Accounts
                    set loan_status = 1, amount = @P_amount + amount
                    where @P_Account_Number = account_number;
                    INSERT INTO Loans(username, account_number, amount, remain_payment, date)
                    VALUES (@P_Username, @P_Account_Number, @P_amount, 12, GETDATE());
                    DECLARE @payment_times INTEGER;
                    set @payment_times = 1;
                    while @payment_times < 13
                        BEGIN
                            INSERT INTO Payments
                            VALUES (@P_Account_Number, @P_amount/12, DATEADD(MONTH, @payment_times, GETDATE()), 0);
                            set @payment_times = @payment_times + 1
                        END
                    INSERT INTO Messages
                    VALUES('Successfully')
                END
        END
END;

CREATE FUNCTION Accounts_Info_byNumber(
@P_Account_Nummber VARCHAR(16),
@P_Username VARCHAR(25)
)
RETURNS TABLE
AS 
RETURN (SELECT * FROM Accounts WHERE @P_Account_Nummber = account_number AND @P_Username = username);


CREATE PROCEDURE TransactionProcedure(
@P_Source_AccountNumber VARCHAR(16),
@P_Destination_AccountNumber VARCHAR(16),
@P_Amount DECIMAL(15,2),
@P_Username VARCHAR(25)
)
AS
BEGIN
    DECLARE @Current_Amount DECIMAL(15,2)
    DECLARE @Current_Block BIT
    SELECT @Current_Amount = amount, @Current_Block = block FROM Accounts 
    WHERE @P_Source_AccountNumber = account_number AND @P_Username = username
    IF @Current_Amount IS NOT NULL AND @Current_Amount >= @P_Amount AND @Current_Block = 0 
        BEGIN
        BEGIN TRANSACTION;
        BEGIN TRY
            DECLARE @Current_Date DATE = CAST(GETDATE() AS DATE);
            DECLARE @Current_Time TIME = CAST(GETDATE() AS TIME);
         
            UPDATE Accounts
            set amount = amount - @P_Amount 
            WHERE @P_Source_AccountNumber = account_number

            UPDATE Accounts
            set amount = amount + @P_Amount 
            WHERE @P_Destination_AccountNumber = account_number

            DECLARE @Updated_Amount_Source DECIMAL(15,2)
            DECLARE @Updated_Amount_Destination DECIMAL(15,2)

            SELECT @Updated_Amount_Source = amount FROM Accounts WHERE @P_Source_AccountNumber = account_number
            SELECT @Updated_Amount_Destination = amount FROM Accounts WHERE @P_Destination_AccountNumber = account_number

            INSERT INTO Transactions
            VALUES(@P_Source_AccountNumber,
                @P_Destination_AccountNumber,
                @P_Amount,
                @Current_Date,
                @Current_Time,
                @Updated_Amount_Source,
                @Updated_Amount_Destination
                )

            INSERT INTO Messages 
            VALUES('Correct')

        COMMIT TRANSACTION;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW;
        END CATCH
    END;
    ELSE
    BEGIN
        INSERT INTO Messages 
        VALUES('Wrong!')
    END;
END;

CREATE FUNCTION Transactions_byNumber(
@P_Account_Number VARCHAR(25),
@P_Number INT,
@P_Username VARCHAR(25)
)
RETURNS TABLE
AS 
RETURN (SELECT TOP (@P_Number) * 
FROM Transactions
WHERE (@P_Account_Number = source_AccountNumber OR @P_Account_Number = destination_AccountNumber) AND EXISTS (SELECT * FROM Accounts WHERE @P_Account_Number = account_number AND @P_Username = username)
ORDER BY date DESC, time DESC);

CREATE FUNCTION Transactions_byDate(
@P_Account_Number VARCHAR(25),
@P_StartDate VARCHAR(60),
@P_EndDate VARCHAR(60),
@P_Username VARCHAR(25)
)
RETURNS TABLE
AS
RETURN (SELECT * 
FROM Transactions 
WHERE date BETWEEN @P_StartDate AND @P_EndDate AND 
(@P_Account_Number = source_AccountNumber OR @P_Account_Number = destination_AccountNumber) AND EXISTS (SELECT * FROM Accounts WHERE @P_Account_Number = account_number AND @P_Username = username)) 


CREATE PROCEDURE Block(
@P_Account_Number VARCHAR(16),
@P_Username VARCHAR(25)
)
AS 
BEGIN
    DECLARE @Current_Block BIT
    SELECT @Current_Block = block FROM Accounts WHERE @P_Account_Number = account_number AND @P_Username = username
    IF @Current_Block = 0
    BEGIN
        UPDATE Accounts
        set block = 1
        WHERE @P_Account_Number = account_number
        INSERT INTO Messages 
        VALUES('Correct!')
    END;
    ELSE
    BEGIN
        INSERT INTO Messages 
        VALUES('Wrong!')
    END;
END;

CREATE PROCEDURE UNblock(
@P_Account_Number VARCHAR(16),
@P_Username VARCHAR(25)
)
AS 
BEGIN
    DECLARE @Current_Block BIT
    SELECT @Current_Block = block FROM Accounts WHERE @P_Account_Number = account_number AND @P_Username = username
    IF @Current_Block = 1
    BEGIN
        UPDATE Accounts
        set block = 0
        WHERE @P_Account_Number = account_number
        INSERT INTO Messages 
        VALUES('Correct!')
    END;
    ELSE
    BEGIN
        INSERT INTO Messages 
        VALUES('Wrong!')
    END;
END;

CREATE FUNCTION Info_Payment_byNumber(
    @P_Account_Number VARCHAR(16),
    @P_Username VARCHAR(25)
)
RETURNS TABLE
AS
RETURN (select * from Payments where @P_Account_Number = account_number AND EXISTS(SELECT * FROM Loans WHERE @P_Username = username AND @P_Account_Number = account_number));

CREATE FUNCTION Get_LoanScore(
    @P_Account_Number VARCHAR(16),
    @P_Username VARCHAR(25)
)
RETURNS INTEGER
AS
BEGIN
    IF EXISTS(SELECT * FROM Accounts WHERE @P_Account_Number = account_number AND @P_Username = username)
    BEGIN
        DECLARE @tmp1 INTEGER;
        DECLARE @tmp2 INTEGER;

        SELECT @tmp1 = MIN(source_amount) 
        FROM Transactions 
        WHERE source_AccountNumber = @P_account_number 
            AND Transactions.date BETWEEN DATEADD(MONTH, -2, GETDATE()) AND GETDATE();

        SELECT @tmp2 = MIN(destination_amount)
        FROM Transactions 
        WHERE destination_AccountNumber = @P_account_number 
            AND date BETWEEN DATEADD(MONTH, -2, GETDATE()) AND GETDATE();

        IF @tmp2 IS NOT NULL AND @tmp1 IS NULL
        BEGIN
            RETURN @tmp2
        END

        IF @tmp1 IS NOT NULL AND @tmp2 IS NULL
        BEGIN
            RETURN @tmp1
        END

        IF @tmp1 IS NULL AND @tmp2 IS NULL
        BEGIN
            RETURN -1
        END

        IF @tmp1 = 0 AND @tmp2 = 0
        BEGIN
            RETURN -1
        END

        RETURN CASE WHEN @tmp1 > @tmp2 THEN @tmp2 ELSE @tmp1 END
    END
    ELSE
    BEGIN
        RETURN -1
    END
    RETURN -1
END;

CREATE PROCEDURE Pay_Loan(
    @P_Account_Number VARCHAR(16),
    @P_Username VARCHAR(25)
)
AS
BEGIN
    IF EXISTS (select * 
                from Accounts 
                where @P_Account_Number = account_number and loan_status = 1) AND EXISTS (SELECT * FROM Payments
                WHERE @P_Account_Number = account_number AND is_paid = 0) AND EXISTS (SELECT * FROM Accounts
                WHERE @P_Account_Number = account_number AND @P_Username = username)
        BEGIN
            DECLARE @P_Payment_Amount DECIMAL(15, 2)
            DECLARE @P_Account_Amount DECIMAL(15, 2)
            select @P_Payment_Amount = amount / 12 from Loans where @P_Account_Number = account_number;
            select @P_Account_Amount = amount from Accounts where @P_Account_Number = account_number;
            IF @P_Payment_Amount <= @P_Account_Amount
                BEGIN
                    UPDATE Loans
                    set remain_payment = remain_payment - 1
                    where Loans.account_number = @P_Account_Number;

                    

                    UPDATE TOP (1) Payments 
                    set is_paid = 1
                    WHERE @P_Account_Number = account_number AND is_paid = 0

                    UPDATE Accounts
                    set amount = amount - @P_Payment_Amount
                    WHERE @P_Account_Number = account_number 

                    
                    INSERT INTO Messages
                    VALUES('Successfully Paid')
                END;
            ELSE
                BEGIN
                    INSERT INTO Messages
                    VALUES('Dont have enough money!')
                END;
        END;
        ELSE
            BEGIN
                UPDATE Accounts
                set loan_status = 0
                WHERE @P_Account_Number = account_number
                INSERT INTO Messages
                VALUES('You dont have loans')
            END;
END;