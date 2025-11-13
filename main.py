from db_connection import connect_to_db, fetch_requests, update_request_status
from jira_connection import connect_to_jira, create_jira_issue
from dotenv import load_dotenv
import os

load_dotenv()


def sync_requests_to_jira():
    """Main workflow: read DB rows, create Jira issues, update DB."""
    jira_project_key = os.getenv("JIRA_PROJECT_KEY")

    # Connect to Jira and Database
    jira = connect_to_jira()
    conn = connect_to_db()
    cur = conn.cursor()

    # Fetch new requests
    rows = fetch_requests(cur)
    print(f"🔍 Found {len(rows)} unsynced requests to create in Jira...")

    # Process each record
    for row in rows:
        request_id = row[0]
        try:
            jira_key = create_jira_issue(jira, jira_project_key, row)
            update_request_status(cur, conn, request_id, jira_key)
            print(f"✅ Created Jira issue {jira_key} for request ID {request_id}")
        except Exception as e:
            print(f"❌ Error creating Jira issue for ID {request_id}: {e}")

    cur.close()
    conn.close()
    print("🎯 Jira sync complete.")


if __name__ == "__main__":
    sync_requests_to_jira()