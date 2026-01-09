from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import operations_agent

app = FastAPI(title="AI Operations Assistant")

# -----------------------------
# Request Schema
# -----------------------------
class Query(BaseModel):
    question: str
    customer_id: str | None = None
    top_k: int = 10


# -----------------------------
# Frontend (Landing Page)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Operations Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                padding: 40px;
            }
            .card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                max-width: 700px;
                margin: auto;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
            }
            p {
                color: #555;
            }
            ul {
                line-height: 1.6;
            }
            .footer {
                margin-top: 20px;
                font-size: 14px;
                color: #777;
            }
            .link {
                color: #2c7be5;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AI Operations Assistant</h1>
            <p>
                This internal assistant helps operations teams proactively identify
                risky customers, understand key drivers, and take timely actions.
            </p>

            <h3>What can you ask?</h3>
            <ul>
                <li>Why is this customer risky?</li>
                <li>Which customers need immediate attention?</li>
                <li>What actions should we take today?</li>
            </ul>

            <p>
                👉 Use the interactive API documentation here:
                <br><br>
                <a class="link" href="/docs">Open API Docs (Swagger UI)</a>
            </p>

            <div class="footer">
                Powered by analytics-driven risk scoring & agentic AI workflows.
            </div>
        </div>
    </body>
    </html>
    """


# -----------------------------
# API Endpoint (Existing Logic)
# -----------------------------
@app.post("/ask")
def ask(query: Query):
    response = operations_agent(
        user_query=query.question,
        customer_id=query.customer_id,
        top_k=query.top_k
    )
    return {"response": response}
