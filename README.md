# Web Based Banking Application

## Description

  A web-based banking application with three roles: customers, tellers, and admin. The application would allow for account management such as checking balances, making deposits and withdrawals, and transferring funds with other users. Tellers would be able to open accounts and flag transactions, and admin would be able to do system edits, delete transactions, and check the logs. We will use Python, SQL, Java, and React.

## Responsibilities

  - Anton:  Authentication and Security and Frontend
  - Billy: Backend
  - Rachel: frontend
  - Caleb: Databasing

## TODO list

  - Design a detailed project plan
  - Start the project

## Database

To use "database setup.py you will need to:
1. Install PostgreSQL
2. Ensure username = postgres, password = !12345
3. Run database setup.py

Required libraries:
psycopg2

This file:
Creates five tables: users, client, account, debit_card, and transactions.
Creates three roles: client, teller, and admin
Enforces Role Based Access Control

Role Based Access Control Overview:
Client:
Users - clients have permission to create, view and update a username and password
Client - Clients can insert their profile information, they can view their information, and can update every field except for UserId, TaxID, Date of Birth, and ClientId.
Account - clients can view all info except for the client id
Debit Card - Clients can view their CardNumber, CardStatus, and ExpirationDate, and they can update their CardStatus (whether its lost or inactive)
Transactions - Clients can view their transaction history (everything in transaction table except Flagged.) They can create new transactions via deposits, withdrawals, or transfers.

Teller:
Users - tellers can view a client's username and update their password
Client - Tellers can view all of a client’s info except for UserId and ClientID, and they can update all of a client’s info except for UserId, TaxId, and ClientID.
Account - tellers can view all info except for the client id, can create new accounts, and can update the status of an account
Debit Card - Tellers can issue a new card, they can view the CardNumber, CardStatus, and ExpirationDate, and they can update the CardStatus.
Transactions - Tellers can view a client’s transaction history, and they can flag suspicious transactions (Flagged) and update the Status of a transaction (reverse it)

Admin:
Users - admins can create new users and roles, view all data in users including UserId and Role,  update the Role of a user, and delete any user.
Client - Admins can create new client profiles, can view all client records, can update any client field except user id and client id, and can delete any client profile.
Account - Admins can create new accounts, can view all accounts, update any account field (except for client id and account id, and delete any account
Debit Card - Admins can issue a new card, can view and update a cards data, and can delete a card.
Transactions - Admins can view all transactions and can update them.

## Frontend and Backend
run "python manage.py runserver" to set up the backend
run these lines in a seperate terminal to set up the frontend
"cd frontend
npm start"
