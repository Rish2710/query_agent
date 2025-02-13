import datetime
import requests
import json
import chromadb
from config import CHROMADB_PATH, SLACK_WEBHOOK_URL


client = chromadb.PersistentClient(path=CHROMADB_PATH)
ticket_collection = client.get_or_create_collection(name="support_tickets")

def send_slack_notification(query, reports, probing_details):
    """Sends a notification to Slack when a ticket is logged."""
    message = (
        f"New Ticket Logged!\n"
        f"Query: {query}\n"
        f"Suggested Reports: {reports if reports else 'None'}\n"
        f"Probing Details: {probing_details}\n"
    )

    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        slack_reference = response.headers.get("X-Slack-Req-Id", "N/A")
        print("Slack notification sent successfully!")
    else:
        slack_reference = "Failed"
        print(f"Failed to send Slack notification: {response.text}")

    return slack_reference


def log_ticket(query, reports, probing_details):
    """Logs unresolved queries in ChromaDB with metadata validation."""
    
    timestamp = datetime.datetime.now().isoformat()
    slack_ref = send_slack_notification(query, reports, probing_details)
    escalation_status = "Pending"  # Default status

    safe_metadata = {
        "timestamp":timestamp,
        "query": query,
        "suggested_reports": json.dumps(reports) if isinstance(reports, list) else reports,
        "probing_details": json.dumps(probing_details) if isinstance(probing_details, dict) else probing_details,
        "slack_reference":slack_ref,
        "escalation_status": escalation_status
    }

    ticket_collection.add(
        ids=[query], 
        metadatas=[safe_metadata],
        documents=[query]
    )

    print("Ticket logged in database!")