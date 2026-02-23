import streamlit as st
from services.ai_service import generate_sql, explain_sql, fix_sql
from database.db import run_query, get_schema
from utils.helpers import is_safe_query

st.title("💡 SQL RAISE (MySQL AI Assistant)")

# Fetch schema dynamically
schema = get_schema()

tab1, tab2, tab3 = st.tabs(["Generate SQL", "Explain SQL", "Fix SQL"])

# --- Generate SQL ---
with tab1:
    question = st.text_area("Ask question from your database")

    if st.button("Generate SQL"):
        sql = generate_sql(question, schema)

        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        if not is_safe_query(sql):
            st.error("❌ Unsafe query detected! Only SELECT queries are allowed.")
        else:
            df, error = run_query(sql)

            if error:
                st.error(error)
            else:
                st.dataframe(df)
        
        if not sql.lower().startswith("select"):
            st.error("Only SELECT queries are allowed!")

def is_safe_query(query):
    dangerous = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT", "TRUNCATE"]

    query_upper = query.upper()

    for word in dangerous:
        if word in query_upper:
            return False

    return query_upper.strip().startswith("SELECT")


# --- Explain SQL ---
with tab2:
    query = st.text_area("Enter SQL query")

    if st.button("Explain"):
        explanation = explain_sql(query)
        st.write(explanation)

# --- Fix SQL ---
with tab3:
    bad_query = st.text_area("Enter wrong SQL")

    if st.button("Fix Query"):
        fixed = fix_sql(bad_query)
        st.code(fixed, language="sql")
