import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_table():
    database_url = os.getenv("DATABASE_URL")

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    # Create the recipes table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS recipes (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        making_time VARCHAR(50) NOT NULL,
        serves VARCHAR(50) NOT NULL,
        ingredients TEXT NOT NULL,
        cost INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cur.execute(create_table_query)

    # Create a function for updating `updated_at`
    create_function_query = '''
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    '''
    cur.execute(create_function_query)

    # Create a trigger to update `updated_at` on row updates
    create_trigger_query = '''
    CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    '''
    cur.execute(create_trigger_query)

    conn.commit()
    print("Table `recipes` and triggers created successfully!")
    conn.close()

if __name__ == "__main__":
    create_table()

