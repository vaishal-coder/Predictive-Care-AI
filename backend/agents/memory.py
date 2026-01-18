
import os
import sqlite3
import json
import datetime
from dotenv import load_dotenv

load_dotenv()

class MemoryAgent:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '../data/health_memory.db')
        self.use_supabase = False
        self.supabase = None
        
        # 1. Ensure Data Dir
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 2. Initialize Local SQLite
        self._init_sqlite()
        
        # 3. Try to Initialize Supabase (Optional Cloud)
        self._init_supabase()

    def _init_sqlite(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_id TEXT,
                    risk_level TEXT,
                    data TEXT
                )
            ''')
            conn.commit()
            conn.close()
            print("Memory Agent: SQLite initialized.")
        except Exception as e:
            print(f"Memory Agent SQLite Error: {e}")

    def _init_supabase(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            try:
                from supabase import create_client
                self.supabase = create_client(url, key)
                self.use_supabase = True
                print("Memory Agent: Supabase Connected.")
            except Exception as e:
                print(f"Memory Agent: Supabase connection failed: {e}")

    def store_interaction(self, user_data, risk_level, plan):
        timestamp = datetime.datetime.now().isoformat()
        payload = {
            "user_data": user_data,
            "risk_level": risk_level,
            "plan": plan
        }
        
        # 1. Local Persistence (Always)
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO interactions (timestamp, risk_level, data) VALUES (?, ?, ?)",
                (timestamp, risk_level, json.dumps(payload))
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Local storage error: {e}")

        # 2. Cloud Persistence (If configured)
        status = "Stored locally"
        if self.use_supabase:
            try:
                self.supabase.table("health_interactions").insert({
                    "timestamp": timestamp,
                    "risk_level": risk_level,
                    "payload": payload
                }).execute()
                status = "Stored in Cloud (Supabase)"
            except Exception as e:
                status = f"Cloud storage failed: {e}"
        
        return status

    def get_history(self):
        # Prefer SQLite for quick retrieval
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM interactions ORDER BY timestamp DESC LIMIT 5")
            rows = cursor.fetchall()
            conn.close()
            return [json.loads(row[0]) for row in rows]
        except Exception as e:
            print(f"History retrieval error: {e}")
            return []
