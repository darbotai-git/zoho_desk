import requests, time
import db

TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
API_BASE = "https://desk.zoho.com/api/v1"

def get_fresh_access_token(client):
    """Return a valid Zoho access token, refreshing if expired"""
    if client["access_token"] and time.time() < client["expires_at"]:
        return client["access_token"]

    data = {
        "refresh_token": client["refresh_token"],
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "grant_type": "refresh_token"
    }
    resp = requests.post(TOKEN_URL, data=data)
    tokens = resp.json()
    if "access_token" not in tokens:
        raise Exception(f"Failed to refresh token: {tokens}")

    access_token = tokens["access_token"]
    expires_in = tokens.get("expires_in_sec", 3600)
    db.update_access_token(client["name"], access_token, expires_in)
    return access_token

def create_ticket(client, subject, description, contact_email):
    token = get_fresh_access_token(client)
    url = f"{API_BASE}/tickets"
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "subject": subject,
        "description": description,
        "contact": {"email": contact_email},
        "departmentId": client["department_id"]
    }
    resp = requests.post(url, headers=headers, json=payload)

    # Debugging: return both status code and response
    if resp.status_code != 200:
        return {
            "error": "Zoho API call failed",
            "status_code": resp.status_code,
            "response": resp.text
        }

    return resp.json()

def list_tickets(client, limit=10):
    """List recent tickets"""
    token = get_fresh_access_token(client)
    url = f"{API_BASE}/tickets?limit={limit}"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    resp = requests.get(url, headers=headers)
    return resp.json()

def get_ticket(client, ticket_id):
    """Get details of a specific ticket"""
    token = get_fresh_access_token(client)
    url = f"{API_BASE}/tickets/{ticket_id}"
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    resp = requests.get(url, headers=headers)
    return resp.json()

def add_comment(client, ticket_id, comment, is_public=True):
    """Add a comment to a ticket (is_public = True shows to customer, False is internal note)"""
    token = get_fresh_access_token(client)
    url = f"{API_BASE}/tickets/{ticket_id}/comments"
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    payload = {"content": comment, "isPublic": is_public}
    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()
