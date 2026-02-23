import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sql(question, schema):
    prompt = f"""
    You are an expert MySQL developer.

    Rules:
    - Only generate SELECT queries
    - Do not use DELETE, UPDATE, DROP
    - Use correct table and column names
    - Return only SQL, no explanation

    Database Schema:
    {schema}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


def explain_sql(query):
    prompt = f"Explain this SQL query in simple words:\n{query}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def fix_sql(query):
    prompt = f"Fix this SQL query:\n{query}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

