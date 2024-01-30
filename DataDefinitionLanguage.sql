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
PRIMARY KEY(account_number),
FOREIGN KEY (username) REFERENCES Users
);

create table Transactions(
source_AccountNumber VARCHAR(16),
destination_AccountNumber VARCHAR(16),
amount DECIMAL(15,2),
date DATE,
time TIME,
PRIMARY KEY(source_AccountNumber, destination_AccountNumber, date, time)
)

