import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "customer_risk_explanations.csv")

data = pd.read_csv(DATA_PATH)
def understand_intent(query):
    query = query.lower()
    
    if "why" in query:
        return "EXPLAIN_RISK"
    elif "who" in query or "which customers" in query:
        return "HIGH_RISK_CUSTOMERS"
    elif "action" in query or "what should we do" in query:
        return "RECOMMEND_ACTIONS"
    else:
        return "GENERAL_INSIGHT"

def run_analysis(intent, customer_id=None):
    """
    Executes data analysis based on the intent identified by the agent.
    Uses risk_score_lr (logistic regression–based risk score).
    """
    
    # Case 1: Identify customers needing immediate attention
    if intent == "HIGH_RISK_CUSTOMERS":
        high_risk_customers = data[data["risk_bucket_lr"] == "High Risk"][
            ["customer_id", "risk_score_lr", "risk_bucket_lr", "risk_drivers"]
        ]
        return high_risk_customers
    
    # Case 2: Explain why a specific customer is risky
    elif intent == "EXPLAIN_RISK" and customer_id is not None:
        customer_row = data[data["customer_id"] == customer_id]
        return customer_row
    
    # Case 3: Recommend actions for today's operations
    elif intent == "RECOMMEND_ACTIONS":
        return data[data["risk_bucket_lr"] == "High Risk"]
    
    # Fallback: Summary statistics
    else:
        return data.describe()

def generate_explanation(row):
    """
    Generates a business-friendly explanation of customer risk
    based on a weighted composite risk score derived from
    logistic regression coefficients.
    """
    
    customer_id = row["customer_id"]
    risk_level = row["risk_bucket_lr"]
    risk_score = round(row["risk_score_lr"], 2)
    drivers = row["risk_drivers"]

    explanation = (
        f"Customer {customer_id} is currently classified as {risk_level.lower()} risk. "
        f"This risk score ({risk_score}) is calculated by combining multiple operational "
        f"and billing factors using weights derived from a logistic regression model "
        f"trained on historical churn data. "
        f"The most influential factors contributing to this score are: {drivers}."
    )
    
    return explanation

def suggest_actions(row):
    """
    Suggests operational actions based on identified risk drivers.
    """
    actions = []
    drivers = row["risk_drivers"].lower()
    
    if "payment" in drivers:
        actions.append("Reach out with a proactive payment reminder or offer flexible payment options.")
    
    if "service" in drivers or "tickets" in drivers:
        actions.append("Assign priority customer support to address service issues.")
    
    if "outage" in drivers:
        actions.append("Investigate infrastructure reliability for this customer.")
    
    if not actions:
        actions.append("Monitor the customer closely for any emerging risk signals.")
    
    return actions

def format_response(customer_id, explanation, actions):
   
    response = f" Customer {customer_id} – Risk Assessment\n\n"
    response += explanation + "\n\nRecommended Actions:\n"
    
    for idx, action in enumerate(actions, 1):
        response += f"{idx}. {action}\n"
    
    return response

def operations_agent(user_query, customer_id=None, top_k=10):
  
    
    intent = understand_intent(user_query)
    top_n = extract_top_n(user_query)
    analysis_result = run_analysis(intent, customer_id)
   
    if intent == "EXPLAIN_RISK" and not analysis_result.empty:
        row = analysis_result.iloc[0]
        explanation = generate_explanation(row)
        actions = suggest_actions(row)
        return format_response(customer_id, explanation, actions)
    
    elif intent == "HIGH_RISK_CUSTOMERS":
        return (
            analysis_result
            .sort_values(by="risk_score_lr", ascending=False)
            .head(top_k)
        )
    
    
    elif intent == "RECOMMEND_ACTIONS":
        return "Focus immediately on high-risk customers with payment delays and repeated service issues."
    
    else:
        return "Please clarify your question so I can assist you better."
