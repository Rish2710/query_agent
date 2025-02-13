# Analytics Query Agent

The **Analytics Query Agent** is an intelligent assistant that helps users find relevant analytics reports from internal and external sources. It uses **ChromaDB** for vector-based searching, **Gina API** for embedding generation, and an external API for additional report retrieval. If a query remains unresolved, the agent asks **probing questions** and escalates the issue via **Slack notifications** while logging it for future reference.

---

## Features
- **Internal Knowledge Base Search**: Finds reports stored in ChromaDB.
- **External API Fetching**: Queries external analytics report APIs.
- **Conversational Intelligence**: Asks intelligent probing questions for better query resolution.
- **Slack Escalations**: Notifies Customer Success Managers (CSMs) if a report is unavailable.
- **Support Ticket Logging**: Logs unresolved queries in ChromaDB for future improvements.

---

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Pip package manager

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Rish2710/query_agent.git
cd analytics-query-agent
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Edit `config.py` and update the following values:
```python
GINA_API_URL = "https://api.gina.com/v1/embedding"
GINA_API_KEY = "your_api_key_here"

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/slack/webhook"

CHROMADB_PATH = "data/chromadb_store"
```

---

## Running the Agent

### 1. Initialize ChromaDB Storage
This step loads sample reports into the internal knowledge base.
```bash
python load_knowledgebase.py
```

### 2. Start the Query Agent
```bash
python main.py
```

### 3. Ask for an Analytics Report
Once running, enter queries like:
```
Enter your analytics report request: Win/Loss Ratio by Sales Region
```

- If a **matching report** is found, it will be displayed.
- If not, the agent will **search an external API**.
- If no external results exist, it will ask **probing questions**.
- If still unresolved, it **logs the issue** and **notifies the team on Slack**.

---

## Check Ticket in Database

Check if the ticket is logged in database or not.

```bash
python -c "import chromadb; db = chromadb.PersistentClient(path='data/chromadb_store'); col = db.get_collection('support_tickets'); print(col.get())"
```
**Note:** Recheck the path and collection name in the command before running it.
---

## Troubleshooting

### Issue: No Reports Found in ChromaDB
**Solution:** Ensure `reports.json` exists and rerun:
```bash
python load_knowledgebase.py
```

### Issue: Slack Notifications Not Working
**Solution:** Check if `SLACK_WEBHOOK_URL` is correctly set in `config.py`.

### Issue: External API Not Returning Results
**Solution:** Ensure `EXTERNAL_API_URL` in `external_apibase.py` is correct and accessible.

---

