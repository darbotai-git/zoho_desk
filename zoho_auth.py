import requests

# Replace with your client credentials
CLIENT_ID = "1000.IDF2BPTFL3XZ1N8SL9KCJISUORC4IS"
CLIENT_SECRET = "6135d02f9eef13d71d00084ea12dde3f8c14e086b3"
REDIRECT_URI = "https://localhost:8080/callback"

# Step 1: Ask user to visit auth URL
auth_url = (
    "https://accounts.zoho.com/oauth/v2/auth"
    f"?scope=Desk.tickets.ALL"
    f"&client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&access_type=offline"
    f"&redirect_uri={REDIRECT_URI}"
)

print("👉 Open this URL in your browser to authorize Zoho Desk access:")
print(auth_url)
print("\nAfter login, copy the 'code' from the redirected URL.\n")

# Step 2: Paste the code
auth_code = input("Paste the code here: ").strip()

# Step 3: Exchange code for access/refresh tokens
token_url = "https://accounts.zoho.com/oauth/v2/token"
data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": auth_code,
}

resp = requests.post(token_url, data=data)
tokens = resp.json()

print("\n✅ Token Response:")
print(tokens)

# Step 4: Save tokens for later use
with open("zoho_tokens.json", "w") as f:
    import json
    json.dump(tokens, f, indent=2)

print("\n💾 Saved tokens into zoho_tokens.json")
