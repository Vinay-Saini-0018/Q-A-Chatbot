# implementing short term memory

from langgraph.checkpoint.postgres import PostgresSaver

DB_URL = "postgresql://postgres:postgres@localhost:5432/chatbot"

memory = PostgresSaver.from_conn_string(DB_URL)

