from db_connection import connect_to_db, fetch_requests
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
    print(f"🔍 Found {len(rows)} requests to create in Jira...")

    # Process each record
    for row in rows:
        requester_name = row[0]
        try:
            jira_key = create_jira_issue(jira, jira_project_key, row)
            print(f"✅ Created Jira issue {jira_key} for {requester_name}")
        except Exception as e:
            print(f"❌ Error creating Jira issue for {requester_name}: {e}")

    cur.close()
    conn.close()
    print("🎯 Jira sync complete.")


if __name__ == "__main__":
    sync_requests_to_jira()