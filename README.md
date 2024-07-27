# Bank Simulator

## Overview

This project is a Bank Simulator application developed as part of a database course. It uses SQL for database operations, Flask for the backend web framework, and HTML/CSS for the frontend interface. The simulator allows users to perform basic banking operations like account creation, deposits, withdrawals, and viewing account balances.

## Features

- **Account Management**: Create and manage bank accounts.
- **Transactions**: Perform deposits and withdrawals.
- **Balance Inquiry**: Check account balances.
- **Transaction History**: View transaction history for accounts.

## Technologies Used

- **Backend**:
  - Flask (Python)
  - SQL (for database operations)

- **Frontend**:
  - HTML
  - CSS

## Project Structure

```sh
BankSimulator/
├── .git/                    # Version control directory
├── DataDefinitionLanguage.sql    # SQL script for data definition (creating tables)
├── DataManipulationLanguage.sql  # SQL script for data manipulation (inserting data)
├── Python/                  # Backend source files
│   ├── app.py               # Main Flask application
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS, images)
│   └── ...                  # Other Python files
├── README.md                # Project README file
```

## Installation

Follow these steps to set up and run the project locally:

### Prerequisites

- Python 3.x installed
- SQL database (e.g., MySQL, PostgreSQL)

### Setup

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/AmirrezaGholizadeh/DB_Project.git
    cd BankSimulator
    ```

2. **Set Up the Database**:
    - Open your SQL database client and execute the contents of `DataDefinitionLanguage.sql` to create the necessary tables.
    - Execute the contents of `DataManipulationLanguage.sql` to insert initial data.

3. **Set Up the Backend**:
    - Navigate to the `Python` directory:
      ```sh
      cd Python
      ```
    - Create a virtual environment:
      ```sh
      python -m venv venv
      ```
    - Activate the virtual environment:
      - On Windows:
        ```sh
        venv\Scripts\activate
        ```
      - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
    - Install dependencies:
      ```sh
      pip install -r requirements.txt
      ```

4. **Run the Application**:
    ```sh
    flask run
    ```

### Accessing the Application

- Open your browser and go to `http://localhost:5000` to access the Bank Simulator.

## Usage

1. **Create an Account**:
   - Navigate to the account creation page and fill out the required details.

2. **Perform Transactions**:
   - Use the deposit and withdrawal forms to perform transactions on your account.

3. **Check Balance**:
   - View your account balance on the balance inquiry page.

4. **View Transaction History**:
   - Access the transaction history page to view all transactions for your account.



## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQL](https://www.w3schools.com/sql/)
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
