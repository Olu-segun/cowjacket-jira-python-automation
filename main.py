from db_connection import connect_to_db, fetch_requests
from jira_connection import connect_to_jira, create_jira_issue
from dotenv import load_dotenv
import os
import logging


load_dotenv()

""" Logging Configuration """

LOG_FILE = "logs/automation_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def start_new_log_section():
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write("\n" +  "=" * 100  + "\n")

def sync_requests_to_jira():
    """Main workflow: read DB rows, create Jira issues, update DB."""
    jira_project_key = os.getenv("JIRA_PROJECT_KEY")

    start_new_log_section()
    
    logging.info("Start jira sync process")

    """ Connect to Jira """
    try:
        jira = connect_to_jira()
        logging.info(" ✅ Connected to jira successfully")
    except Exception as e:
        logging.info("Failed to connect to jira: {e}")
        print(f"❌ Jira connection fail: {e}")
        return
    
    """ Connect to database """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        logging.info("✅ Connected to database successfully")
    except Exception as e:
        logging(f"Failed to connect to database: {e}")
        print(f"❌ Database connection failed: {e}")


    """ Fetch new requests from database """
    rows = fetch_requests(cur)
    print(f"🔍 Found {len(rows)} requests to create in Jira...")
    logging.info(f"Fetched {len(rows)} requests from database.")

    """ Process each record fetched from database """
    for row in rows:
        requester_name = row[0]
        try:
            jira_key = create_jira_issue(jira, jira_project_key, row)
            print(f"✅ Created Jira issue {jira_key} for {requester_name}")
            logging.info(f"Created jira issue {jira_key} for {requester_name}")
        except Exception as e:
            print(f"❌ Error creating Jira issue for {requester_name}: {e}")
            logging.info(f"❌ Failed to create jira issue for {requester_name}: {e}")

    cur.close()
    conn.close()

    logging.info(f"Jira Sync Completed Successfully✅. ")
    print("🎯 Jira sync complete.")


if __name__ == "__main__":
    sync_requests_to_jira()