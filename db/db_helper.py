import sqlite3

class SQLiteHelper:
    def __init__(self, db_path="db/assistant.db"):
        self.conn = sqlite3.connect(db_path)
    
    def query_database(self, intent, slots):
        # Simplified example — adapt based on your DB schema & intents
        cursor = self.conn.cursor()
        if intent == "GetContainerStatus":
            container_name = slots.get("container_name", "")
            cursor.execute("SELECT status FROM containers WHERE name=?", (container_name,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown container"
        else:
            return "Intent not handled."

    def close(self):
        self.conn.close()
