create table Users(
username VARCHAR(25) UNIQUE NOT NULL,
password VARCHAR(256) NOT NULL,
name VARCHAR(50),
lastname VARCHAR(50),
email VARCHAR(50),
phone_number VARCHAR(11),
salt UNIQUEIDENTIFIER,
PRIMARY KEY(username)
);

create table Accounts(
account_number VARCHAR(16),
username VARCHAR(25),
amount DECIMAL(15,2),
block BIT,
loan_status BIT,
date DATE,
PRIMARY KEY(account_number),
FOREIGN KEY (username) REFERENCES Users
);

create table Transactions(
source_AccountNumber VARCHAR(16),
destination_AccountNumber VARCHAR(16),
amount DECIMAL(15,2),
date DATE,
time TIME,
source_amount DECIMAL(15,2),
destination_amount DECIMAL(15,2),
PRIMARY KEY(source_AccountNumber, destination_AccountNumber, date, time)
)

create table Messages (message varchar(256))

CREATE TABLE Loans (
    username VARCHAR(25),
    account_number VARCHAR(16),
    amount DECIMAL(15, 2),
    remain_payment INTEGER,
    date DATE,
    PRIMARY KEY (account_number),
    FOREIGN KEY (account_number) REFERENCES Accounts(account_number),
    FOREIGN KEY (username) REFERENCES Users(username)
);

CREATE TABLE Payments (
    account_number VARCHAR(16),
    amount DECIMAL(15, 2),
    date DATE,
    is_paid BIT,
    PRIMARY KEY (account_number, date),
    FOREIGN KEY (account_number) REFERENCES Loans(account_number)
);
