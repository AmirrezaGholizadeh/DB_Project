
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
    SET @salt = NEWID();-- Generating the salt for hashing the password
    DECLARE @hashedPassword VARBINARY(256); -- adjust the length as needed
    SET @hashedPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_Password, @salt) AS varchar(MAX)));--Final hashed password

    IF NOT EXISTS(SELECT * FROM Users WHERE @P_Username = username)
        BEGIN 
            INSERT INTO Users
            VALUES (@P_Username, @hashedPassword, @P_Name, @P_Lastname, @P_Email, @P_Phone_Number, @salt);
        END;
    ELSE
        BEGIN
            -- Aware the python program
            SELECT * FROM Users
            -- above line is just something TEMPORARY for skipping the error
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
        DECLARE @hashedPassword VARBINARY(256); -- adjust the length as needed
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

---------------------


CREATE PROCEDURE Change_Password(
@P_Username VARCHAR(20),
@P_Current_Password VARCHAR(256),
@P_New_Password VARCHAR(256)
)
AS
BEGIN
    IF NOT EXISTS (SELECT * FROM Users WHERE @P_Username = username)
    BEGIN
        PRINT 'The username doesn''t exist!'
    END;

    ELSE
    BEGIN
        DECLARE @User_Salt UNIQUEIDENTIFIER;
        DECLARE @Stored_Password VARCHAR(256);
        SELECT @User_Salt = salt , @Stored_Password = password FROM Users WHERE @P_Username = username;
        DECLARE @hashedPassword VARBINARY(256); -- adjust the length as needed
        SET @hashedPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_Current_Password, @User_Salt) AS varchar(MAX)));

        IF @Stored_Password = @hashedPassword
        BEGIN
            DECLARE @hashedNewPassword VARBINARY(256); -- adjust the length as needed
            SET @hashedNewPassword = HASHBYTES('SHA2_256', CAST(CONCAT(@P_New_Password, @User_Salt) AS varchar(MAX)));
            UPDATE Users
            set password = @hashedNewPassword
            WHERE @P_Username = username
            PRINT'Correct';
        END;
        ELSE
        BEGIN
            PRINT 'Discorrect';
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



CREATE FUNCTION Acounts_Info_byID(
@P_Username VARCHAR(25)
)
RETURNS TABLE
AS 
RETURN (SELECT * FROM Accounts WHERE @P_Username = username);

CREATE FUNCTION Accounts_Info_byNumber(
@P_Account_Nummber VARCHAR(16)
)
RETURNS TABLE
AS 
RETURN (SELECT * FROM Accounts WHERE @P_Account_Nummber = account_number);

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

CREATE PROCEDURE TransactionProcedure(
@P_Source_AccountNumber VARCHAR(16),
@P_Destination_AccountNumber VARCHAR(16),
@P_Amount DECIMAL(15,2)
)
AS
BEGIN
    DECLARE @Current_Amount DECIMAL(15,2)
    SELECT @Current_Amount = amount FROM Accounts WHERE @P_Source_AccountNumber = account_number
    IF @Current_Amount >= @P_Amount
        BEGIN
        BEGIN TRANSACTION;
        BEGIN TRY
            DECLARE @Current_Date DATE = CAST(GETDATE() AS DATE);
            DECLARE @Current_Time TIME = CAST(GETDATE() AS TIME);
            INSERT INTO Transactions
            VALUES(@P_Source_AccountNumber,
                @P_Destination_AccountNumber,
                @P_Amount,
                @Current_Date,
                @Current_Time
                )
            UPDATE Accounts
            set amount = amount - @P_Amount 
            WHERE @P_Source_AccountNumber = account_number

            UPDATE Accounts
            set amount = amount + @P_Amount 
            WHERE @P_Destination_AccountNumber = account_number

        COMMIT TRANSACTION;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW;
        END CATCH
    END;
    ELSE
    BEGIN
        PRINT 'Not successful!'
    END;
END;

CREATE FUNCTION Transactions_byNumber(
@P_Account_Number VARCHAR(25),
@P_Number INT
)
RETURNS TABLE
AS 
RETURN (SELECT TOP (@P_Number) * 
FROM Transactions 
WHERE @P_Account_Number = source_AccountNumber OR @P_Account_Number = destination_AccountNumber
ORDER BY date DESC, time DESC);

CREATE FUNCTION Transactions_byDate(
@P_Account_Number VARCHAR(25),
@P_StartDate DATE,
@P_EndDate DATE
)
RETURNS TABLE
AS 
RETURN (SELECT * 
FROM Transactions 
WHERE date BETWEEN @P_StartDate AND @P_EndDate AND 
@P_Account_Number = source_AccountNumber OR @P_Account_Number = destination_AccountNumber);




-- EXECUTE TransactionProcedure @P_Source_AccountNumber = '5859831103511167',
-- @P_Destination_AccountNumber = '5810121345678092', @P_Amount = 10000

-- SELECT TOP 2 * FROM Transactions ORDER BY date DESC, time  DESC 

-- -- EXECUTE New_Account @P_Account_Number = '5810121345678090',@P_Username = 'Mohsen', 
-- -- @P_Amount = '556000000', @P_Block = 1 , @P_Loan_Status = 1

-- -- -- EXECUTE Change_Password @P_Username = 'Amiir', @P_Current_Password = '456', @P_New_Password = '789'

-- SELECT * FROM Transactions_byDate('5859831103511167', '2024-01-30', '2024-01-30')
-- SELECT * FROM Accounts
-- SELECT * FROM Users
-- PRINT dbo.Account_Owner ('5810121345678092')









