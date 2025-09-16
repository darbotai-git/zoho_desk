from fastapi import FastAPI
from pydantic import BaseModel
import db, zoho_api

app = FastAPI()
db.init_db()

class TicketRequest(BaseModel):
    subject: str
    description: str
    email: str

@app.post("/create_ticket/{client_name}")
def create_ticket(client_name: str, ticket: TicketRequest):
    client = db.get_client(client_name)
    if not client:
        return {"error": "Unknown client"}
    result = zoho_api.create_ticket(
        client,
        ticket.subject,
        ticket.description,
        ticket.email
    )
    return result

@app.post("/add_client")
def add_client(name: str, client_id: str, client_secret: str, refresh_token: str, department_id: str):
    db.add_client(name, client_id, client_secret, refresh_token, department_id)
    return {"status": "Client added", "client": name}
