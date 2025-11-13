import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def connect_to_db():
    """
    Establish a connection to the PostgreSQL database using environment variables,
    execute a simple query, and return the results.
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("HOST_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        print("✅ Connected to the database successfully!")
    except Exception as e:
        print("Failed to connect to the database.")
        print(f"Error: {e}")
        return None
    
    return conn

def fetch_requests(cur):

    cur.execute("""
        SELECT 
            newusername,
            samplename,
            phonenumber,
            departmentname,
            job,
            emailaddress,
            costcenter,
            telephonelinesandinstallations,
            handsetsandheadsets,
            timeframe,
            dateneededby,
            approximateendingdate,
            "Comments",
            createdat
        FROM phonerequest;
    """)
    return cur.fetchall()

def update_request_status(cur, conn, request_id, jira_key):
    """Mark request as synced with Jira ticket info."""
    cur.execute("""
        UPDATE phonerequest
        SET jira_ticket_id = %s, jira_created_at = NOW()
        WHERE id = %s;
    """, (jira_key, request_id))
    conn.commit()