
import psycopg2

#connects to default database "postgres" with password !12345
conn = psycopg2.connect(dbname = 'postgres', user = 'postgres', password = '!12345', host = 'localhost', port = '5432')
print("opened database successfully")

cur = conn.cursor()

#creates roles, makes sure they don't already exist
roles = ['client','teller','admin']
for role in roles:
    try:
        cur.execute(f"CREATE ROLE {role}")
    except psycopg2.errors.DuplicateObject:
        conn.rollback()
conn.commit()


#creates table for Users
cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(50) NOT NULL, user_role VARCHAR(50) NOT NULL DEFAULT 'client' CHECK (user_role IN ('client','teller','admin'))
) ''')

#ROLE BASED ACCESS FOR USERS TABLE
try:
    # grants clients permission to insert or update a username and password
    cur.execute('GRANT INSERT (username, password) ON users TO client')
    cur.execute('GRANT UPDATE (username, password) ON users TO client')
    cur.execute('GRANT SELECT (username, password) ON users TO client')

    #grants tellers ability to view a client's username and update their password
    cur.execute('GRANT SELECT (username) ON USERS TO TELLER')
    cur.execute('GRANT UPDATE (password) ON USERS TO TELLER')

    #grants admins ability to create new users and roles, view all data in users including UserId and Role,  update the Role of a user, and delete any user.
    cur.execute('GRANT INSERT ON users TO ADMIN')
    cur.execute('GRANT SELECT ON users TO ADMIN')
    cur.execute('GRANT UPDATE (user_role) ON USERS TO ADMIN')
    cur.execute('GRANT DELETE ON users TO ADMIN')
    cur.execute('ALTER ROLE admin CREATEROLE')

    conn.commit()

except psycopg2.Error as e:
    conn.rollback()


#creates table for Clients
cur.execute('CREATE TABLE IF NOT EXISTS client(client_id SERIAL PRIMARY KEY, '
            'user_id INTEGER NOT NULL REFERENCES users(user_id),'
            'first_name VARCHAR(100) NOT NULL,'
            'last_name VARCHAR(100) NOT NULL,'
            'address VARCHAR(100) NOT NULL,'
            'city VARCHAR(30) NOT NULL,'
            'state VARCHAR(30) NOT NULL,'
            'zipcode VARCHAR(10) NOT NULL,'
            'date_of_birth DATE NOT NULL,'
            'email VARCHAR(100) NOT NULL,'
            'phone_number VARCHAR(20) NOT NULL,'
            'tax_id VARCHAR(20) NOT NULL) ')

#ROLE BASED ACCESS FOR Client TABLE
try:
    #Clients can insert their profile information, they can view their information, and can update every field except for UserId, TaxID, Date of Birth, and ClientId.
    cur.execute('GRANT INSERT (first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number, tax_id) ON client TO client')
    cur.execute('GRANT UPDATE (first_name, last_name, address, city, state, zipcode, email, phone_number, tax_id) ON client TO client')
    cur.execute('GRANT SELECT (first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number, tax_id) ON client TO client')

    #Tellers can view all of a client’s info except for UserId and ClientID, and they can update all of a client’s info except for UserId, TaxId, and ClientID.
    cur.execute('GRANT SELECT (first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number, tax_id) ON client TO teller')
    cur.execute('GRANT UPDATE (first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number) ON client TO teller')

    #Admins can create new client profiles, can view all client records, can update any client field except user id and client id, and can delete any client profile.
    cur.execute('GRANT INSERT ON client TO admin')
    cur.execute('GRANT SELECT ON client TO admin')
    cur.execute('GRANT UPDATE (first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number, tax_id) ON client TO admin')
    cur.execute('GRANT DELETE ON client TO admin')

    conn.commit()

except psycopg2.Error as e:
    conn.rollback()

#creates table for Account; accounts have 3 statuses: open, closed, and frozen, and they have two types: checking and saving
cur.execute('CREATE TABLE IF NOT EXISTS account (account_id SERIAL PRIMARY KEY,'
            'client_id INTEGER NOT NULL REFERENCES client(client_id),'
            'balance BIGINT NOT NULL,'
            'account_status VARCHAR(30) NOT NULL CHECK (account_status IN (\'open\', \'closed\', \'frozen\')),'
            'account_type VARCHAR(30) NOT NULL CHECK (account_type IN (\'checking\', \'savings\')),'
            'creation_date DATE NOT NULL,'
            'termination_date DATE)')


#ROLE BASED ACCESS FOR account TABLE
try:
    # clients can view all info except for the client id
    cur.execute('GRANT SELECT (account_id, balance, account_type, account_status, creation_date, termination_date) ON account TO client')

    #tellers can view all info except for the client id, can create new accounts, and can update the status of an account
    cur.execute('GRANT SELECT (account_id, balance, account_type, account_status, creation_date, termination_date) ON account TO teller')
    cur.execute('GRANT INSERT ON account TO teller')
    cur.execute('GRANT UPDATE (account_status) ON account TO teller')

    #Admins can create new accounts, can view all accounts, update any account field (except for client id and account id, and delete any account
    cur.execute('GRANT INSERT ON account TO admin')
    cur.execute('GRANT SELECT ON account TO admin')
    cur.execute('GRANT UPDATE (balance, account_type, account_status, creation_date, termination_date) ON account TO admin')
    cur.execute('GRANT DELETE ON account TO admin')

    conn.commit()

except psycopg2.Error as e:
    conn.rollback()

#creates table for Debit Card. Cards can have 5 statuses: active, inactive, blocked, issued, or lost
cur.execute('CREATE TABLE IF NOT EXISTS debit_card(card_number VARCHAR(30) PRIMARY KEY,'
            'account_id INTEGER NOT NULL REFERENCES account(account_id),'
            'client_id INTEGER NOT NULL REFERENCES client(client_id),'
            'card_status VARCHAR(30) NOT NULL CHECK (card_status IN (\'active\', \'inactive\', \'blocked\', \'issued\', \'lost\')),'
            'expiration_date DATE NOT NULL)')

#ROLE BASED ACCESS FOR debit card TABLE
try:

    #Clients can view their CardNumber, CardStatus, and ExpirationDate, and they can update their CardStatus (whether its lost or inactive)
    cur.execute('GRANT SELECT (card_number, card_status, expiration_date) ON debit_card TO client')
    cur.execute('GRANT UPDATE (card_status) ON debit_card TO client')

    #Tellers can issue a new card, they can view the CardNumber, CardStatus, and ExpirationDate, and they can update the CardStatus.
    cur.execute('GRANT INSERT ON debit_card TO teller')
    cur.execute('GRANT SELECT (card_number, card_status, expiration_date) ON debit_card TO teller')
    cur.execute('GRANT UPDATE (card_status) ON debit_card TO teller')

    #Admins can issue a new card, can view and update a cards data, and can delete a card.
    cur.execute('GRANT INSERT ON debit_card TO admin')
    cur.execute('GRANT SELECT (account_id, card_number, card_status, expiration_date) ON debit_card TO admin')
    cur.execute('GRANT UPDATE (card_status, expiration_date) ON debit_card TO admin')
    cur.execute('GRANT DELETE ON debit_card TO admin')

    conn.commit()

except psycopg2.Error as e:
    conn.rollback()

#creates table for Transactions. Transactions can have the statuses pending, failed, success, and reversed and can be flagged yes or no.
cur.execute('CREATE TABLE IF NOT EXISTS transactions(transaction_id SERIAL PRIMARY KEY,'
            'recipient_id INTEGER NOT NULL REFERENCES client(client_id),'
            'sender_id INTEGER NOT NULL REFERENCES client(client_id),'
            'transaction_type VARCHAR(30) NOT NULL,'
            'amount BIGINT NOT NULL,'
            'transaction_time TIMESTAMP NOT NULL,'
            'status VARCHAR(15) NOT NULL CHECK (status IN (\'pending\', \'failed\', \'success\', \'reversed\')),'
            'flagged VARCHAR(5) NOT NULL CHECK (flagged IN (\'yes\', \'no\')))')

#ROLE BASED ACCESS FOR transactions TABLE
try:

    #Clients can view their transaction history (everything in transaction table except Flagged.) They can create new transactions via deposits, withdrawals, or transfers.
    cur.execute('GRANT SELECT (transaction_id, recipient_id, sender_id, transaction_type, amount, transaction_time, status) ON transactions TO client')
    cur.execute('GRANT INSERT ON transactions TO client')

    #Tellers can view a client’s transaction history, and they can flag suspicious transactions (Flagged) and update the Status of a transaction (reverse it)
    cur.execute('GRANT SELECT ON transactions TO teller')
    cur.execute('GRANT UPDATE (status, flagged) ON transactions TO teller')

    #Admins can view all transactions and can update them.
    cur.execute('GRANT SELECT ON transactions TO admin')
    cur.execute('GRANT UPDATE ON transactions TO admin')

    conn.commit()

except psycopg2.Error as e:
    conn.rollback()



#DEBUGGING USED TO INSERT A ROW
#cur.execute('INSERT INTO users (username, password, user_role) VALUES(%s, %s, %s)', ('bob','pass123','client'))

print("table created successfully")
conn.commit()
cur.close()
conn.close()