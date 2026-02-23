import streamlit as st
from services.ai_service import generate_sql
from database.db import run_query, get_schema
from utils.helpers import is_safe_query

st.set_page_config(page_title="SQL ChatBot", layout="wide")

st.title("🤖 SQL AI ChatBot")

# Get DB schema
schema = get_schema()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask about your database...")

if user_input:

    # Show user message
    st.chat_message("user").markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Thinking..."):

        # 🔥 Step 1: Generate SQL
        sql = generate_sql(user_input, schema)

        # 🔥 Step 2: Safety check
        if not is_safe_query(sql):
            response = "❌ Unsafe query detected!"
        else:
            # 🔥 Step 3: Run query
            df, error = run_query(sql)

            if error:
                response = f"❌ Error: {error}"
            else:
                response = f"### 🧠 SQL\n```sql\n{sql}\n```"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

        # 🔥 Show data separately
        if "df" in locals() and error is None:
            st.dataframe(df, use_container_width=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    sql = generate_sql(user_input, schema)

    # ❗ NEW CHECK
    if "INVALID_QUERY" in sql:
        st.error("❌ This data does not exist in database!")

    if not is_valid_table(sql, schema):
        st.error("❌ Invalid table used in query")