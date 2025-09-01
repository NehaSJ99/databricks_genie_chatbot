import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
import requests
import time
import json

# Databricks Genie Conversation API endpoints and credentials
databricks_instance = os.getenv("DATABRICKS_INSTANCE")
space_id = os.getenv("SPACE_ID")
auth_token = os.getenv("AUTH_TOKEN")

api_base = f"https://{databricks_instance}/api/2.0/genie/spaces/{space_id}"
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

def fetch_query_result(conversation_id: str, message_id: str, attachment_id: str):
    """
    Fetches the result of the Genie query using the attachment_id and returns it as a pretty-printed string.
    """
    url = f"{api_base}/conversations/{conversation_id}/messages/{message_id}/query-result/{attachment_id}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    print("Genie Query Result:", data)  # Debug log

    # Check for tabular results (data_array + schema)
    schema = None
    data_array = None
    # Look for schema and data_array in possible locations
    if "result" in data:
        result = data["result"]
        data_array = result.get("data_array")
        schema = result.get("schema")
    elif "statement_response" in data:
        sr = data["statement_response"]
        if "result" in sr:
            result = sr["result"]
            data_array = result.get("data_array")
        if "manifest" in sr and "schema" in sr["manifest"]:
            schema = sr["manifest"]["schema"]
    # If tabular, format as column_name: value
    if data_array and schema and "columns" in schema:
        col_names = [col.get("name", f"col{i}") for i, col in enumerate(schema["columns"])]
        lines = []
        for row in data_array:
            pairs = [f"{col}: {val}" for col, val in zip(col_names, row)]
            lines.append(", ".join(pairs))
        return "\n".join(lines)
    # If text content is present, display it
    if "attachments" in data and data["attachments"]:
        att = data["attachments"][0]
        if "text" in att and "content" in att["text"]:
            return att["text"]["content"]
    # Fallback: show raw JSON
    return json.dumps(data, indent=2)

def start_conversation(message: str):
    url = f"{api_base}/start-conversation"
    payload = {"content": message}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    conversation_id = data["conversation"]["id"]
    message_id = data["message"]["id"]
    return conversation_id, message_id

def send_followup(conversation_id: str, message: str):
    url = f"{api_base}/conversations/{conversation_id}/messages"
    payload = {"content": message}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if "message" in data and "id" in data["message"]:
        message_id = data["message"]["id"]
        return message_id
    elif "message_id" in data:
        return data["message_id"]
    else:
        print("Genie follow-up response (no 'message' or 'message_id' key):", data)
        raise KeyError(f"No 'message' or 'message_id' key in Genie follow-up response: {data}")

def poll_message(conversation_id: str, message_id: str, timeout=60, poll_interval=5):
    url = f"{api_base}/conversations/{conversation_id}/messages/{message_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        print("Genie API response:", data)  # Debug log
        status = data.get("status")
        if status == "COMPLETED":
            attachments = data.get("attachments", [])
            if attachments and attachments[0].get("attachment_id"):
                attachment_id = attachments[0]["attachment_id"]
                # Fetch and return the actual query result
                return fetch_query_result(conversation_id, message_id, attachment_id)
            # If no attachments, check for error or content
            if data.get("error"):
                return f"Error: {data['error']}"
            if data.get("content"):
                return f"Content: {data['content']}"
            return f"No response content. Full response: {data}"
        elif status in ["FAILED", "CANCELLED"]:
            return f"Genie message status: {status}"
        time.sleep(poll_interval)
    return "Timeout waiting for Genie response."

class GenieConversation:
    def __init__(self):
        self.conversation_id = None
        self.last_message_id = None

    def send_message(self, message: str) -> str:
        if not self.conversation_id:
            # Start new conversation
            self.conversation_id, self.last_message_id = start_conversation(message)
        else:
            # Send follow-up
            self.last_message_id = send_followup(self.conversation_id, message)
        # Poll for completion
        return poll_message(self.conversation_id, self.last_message_id)