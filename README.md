
# CowJacket Jira Python Automation 🐮

## 📌 Project Overview
CowJacket Jira Python Automation is a Python-based automation tool designed to streamline the integration between CowJacket’s request tracking system and Jira. The project eliminates the need for manual issue creation and CSV uploads by automating Jira ticket creation, updates, and tracking through API interactions.

## 🚀 Features
- Automatically creates Jira tickets from CowJacket requests
- Supports Jira REST API integration
- Handles authentication using environment variables (.env)
- Performs automated field mapping (e.g., summary, description, issue type, assignee)
- Logs all automation activity for traceability and debugging

## ⚙️ Tech Stack
- **Language:** Python 3.10+
- **Libraries:** `jira`,`psycopg2`,  `os`, `dotenv`, `json`
- **Platform:** Jira Cloud REST API
- **Version Control:** Git & GitHub

## 🧠 How It Works
1. **Extracts Request Data** from CowJacket database.
2. **Transforms** request details into Jira-compatible JSON payloads.
3. **Loads** the transformed data into Jira via REST API POST requests.
4. **Logs Responses** for success/failure handling.

## 📸 Demo Output
This shows the successfully created Jira issues using the automation script:
![Jira Automation Output](image.png)

## 🔐 Environment Setup
Create a `.env` file in the project root with your Jira credentials:

```bash
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_generated_token
JIRA_PROJECT_KEY=COWCX
```

## 🧩 Example Usage
```python
from jira_automation import create_jira_ticket

issue_data = {
    "summary": "Automated Bug Report from CowJacket",
    "description": "Detected issue with request ID CJ-1021",
    "issuetype": {"name": "Bug"}
}

response = create_jira_ticket(issue_data)
print(response.status_code)
```

## 🧾 Logging
All API calls and responses are logged automatically to `automation_log.txt` for audit purposes.

## 📊 Future Improvements
- Add webhook integration for real-time updates from Jira.
- Build a dashboard to visualize automation statistics.
- Implement retry logic for failed API calls.

## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss changes.

## 🧑‍💻 Author
**Olusegun Olukayode**  
Python Developer | Data Analyst | Automation Enthusiast

---
_“Automate the routine. Focus on the impactful.”_

