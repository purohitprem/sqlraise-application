import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ API key load
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Model
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# Clean SQL
def clean_sql(response):
    return response.replace("```sql", "").replace("```", "").strip()


# Generate SQL
def generate_sql(question, schema):
    prompt = f"""
    You are an expert MySQL developer.

    STRICT RULES:
    - Only use tables given in schema
    - Do NOT guess table names
    - If question refers to unknown table, return: INVALID_QUERY
    - Only generate SELECT query
    - No explanation

    Schema:
    {schema}

    Question:
    {question}

    Output:
    Only SQL or INVALID_QUERY
    """

    response = model.generate_content(prompt)

    return clean_sql(response.text)


# Explain SQL
def explain_sql(query):
    response = model.generate_content(f"Explain this SQL:\n{query}")
    return response.text


# Fix SQL
def fix_sql(query):
    response = model.generate_content(f"Fix this SQL:\n{query}")
    return clean_sql(response.text)