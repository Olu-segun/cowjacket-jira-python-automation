from jira import JIRA
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def connect_to_jira():
    # Get Jira credentials from .env
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_base_url = os.getenv("JIRA_BASE_URL")
    jira_project_key = os.getenv("JIRA_PROJECT_KEY")

    # Check if credentials are loaded correctly
    if not all([jira_email, jira_api_token, jira_base_url]):
        raise ValueError("Missing one or more Jira environment variables. Please check your .env file.")

    # Connect to Jira
    jira = JIRA(
                server=jira_base_url, 
                basic_auth=(jira_email, jira_api_token)

                )
    return jira



def create_jira_issue(jira, project_key, row):
    """Create a Jira issue from a database row."""
    (
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
        comments,
        createdat
    ) = row

    summary = f"Telecom Request - {newusername or samplename} ({departmentname})"
    description = f"""
**Requester:** {newusername or samplename}
**Job Title:** {job}
**Department:** {departmentname}
**Email:** {emailaddress}
**Phone Number:** {phonenumber}
**Cost Center:** {costcenter}

**Request Details:**
- Telephone Lines / Installations: {telephonelinesandinstallations}
- Handsets / Headsets: {handsetsandheadsets}
- Time Frame: {timeframe}
- Date Needed By: {dateneededby}
- Approximate Ending Date: {approximateendingdate}

**Comments:**
{comments or "N/A"}

**Created At:** {createdat}
"""

    issue = jira.create_issue(
        project=project_key,
        summary=summary,
        description=description,
        issuetype={"name": "Submit a request or incident"}  # Match your Jira project setup
    )

    return issue.key