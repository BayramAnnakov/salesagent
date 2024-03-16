import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('crm.db')

# Create a cursor object
c = conn.cursor()


def init_db():
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            full_name TEXT,
            company TEXT,
            sales_call_score INTEGER,
            lead_score INTEGER
        )
    ''')

    # Save (commit) the changes
    conn.commit()
# Create table

def insert_customer(customer_id: str, customer_full_name: str, customer_company:str, sales_call_score: int, lead_score: int):
    c.execute('''
        INSERT INTO customers (id, full_name, company, sales_call_score, lead_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, customer_full_name, customer_company, sales_call_score, lead_score))

    conn.commit()

def update_customer(customer_id: str, sales_call_score: int, lead_score: int):

    c.execute('''
        UPDATE customers
        SET sales_call_score = ?, lead_score = ?
        WHERE id = ?
    ''', (sales_call_score, lead_score, customer_id))

    conn.commit()

def insert_or_update_customer(customer_id: str, customer_full_name: str, customer_company:str, sales_call_score: int, lead_score: int):
    c.execute('''
        SELECT * FROM customers WHERE id = ?
    ''', (customer_id,))

    customer = c.fetchone()

    if customer:
        update_customer(customer_id, sales_call_score, lead_score)
    else:
        insert_customer(customer_id, customer_full_name, customer_company, sales_call_score, lead_score)