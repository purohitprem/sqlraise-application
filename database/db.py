from sqlalchemy import create_engine
import pandas as pd

# Replace with your MySQL details
DB_USER = "root"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_NAME = "practice"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

def run_query(query):
    try:
        df = pd.read_sql(query, engine)
        return df, None
    except Exception as e:
        return None, str(e)

def get_schema():
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
    ORDER BY table_name;
    """

    df = pd.read_sql(query, engine)

    schema = ""
    for table in df['table_name'].unique():
        columns = df[df['table_name'] == table]['column_name'].tolist()
        schema += f"Table: {table}({', '.join(columns)})\n"

    return schema