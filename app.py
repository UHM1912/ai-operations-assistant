from fastapi import FastAPI
from pydantic import BaseModel
from agent import operations_agent

app = FastAPI(title="AI Operations Assistant")

class Query(BaseModel):
    question: str
    customer_id: str | None = None

@app.post("/ask")
def ask(query: Query):
    response = operations_agent(
        query.question,
        query.customer_id
    )
    return {"response": response}
