import sqlite3
import json
from datetime import datetime


class LuciaMemory:
    def __init__(self):
        # ✅ FIX: check_same_thread=False add kiya
        self.connection = sqlite3.connect(
            'lucia.db', check_same_thread=False
        )
        self.cursor = self.connection.cursor()
        # ✅ FIX: WAL mode — faster writes, safer reads
        self.cursor.execute("PRAGMA journal_mode=WAL")
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0)
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                lucia_response TEXT NOT NULL,
                emotion_detected TEXT DEFAULT 'neutral',
                intent_detected TEXT DEFAULT 'general',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_knowledge(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                contents TEXT NOT NULL,
                source TEXT DEFAULT 'user',
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
        self.connection.commit()

    def save_memory(self, key, value, category='general'):
        self.cursor.execute(
            "SELECT id FROM memories WHERE key = ? AND category = ?",
            (key, category)
        )
        existing = self.cursor.fetchone()

        if existing:
            self.cursor.execute("""
                UPDATE memories
                SET value = ?, updated_at = ?
                WHERE key = ? AND category = ?
            """, (value, datetime.now(), key, category))
            print(f'[MEMORY] Updated: {key} = {value}')
        else:
            self.cursor.execute("""
                INSERT INTO memories(key, value, category)
                VALUES (?, ?, ?)
            """, (key, value, category))
            print(f'[MEMORY] Created: {key} = {value} [{category}]')

        self.connection.commit()
        return True

    def get_memory(self, key, category=None):
        if category:
            self.cursor.execute(
                "SELECT value FROM memories WHERE key=? AND category=?",
                (key, category)
            )
        else:
            self.cursor.execute(
                "SELECT value FROM memories WHERE key=?", (key,)
            )

        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(
                "UPDATE memories SET access_count=access_count+1 WHERE key=?",
                (key,)
            )
            self.connection.commit()
            print(f"[MEMORY] Found: {key} = {result[0]}")
            return result[0]

        print(f"[MEMORY] NOT FOUND: {key}")
        return None

    def search_memory(self, search_term):
        self.cursor.execute("""
            SELECT key, value, category, created_at
            FROM memories
            WHERE key LIKE ? OR value LIKE ? OR category LIKE ?
            ORDER BY updated_at DESC
            LIMIT 10
        """, (
            f"%{search_term}%",
            f"%{search_term}%",
            f"%{search_term}%"
        ))
        results = self.cursor.fetchall()

        if results:
            print(
                f"[MEMORY] Found {len(results)} results "
                f"for '{search_term}'"
            )
            return [
                {
                    "key": r[0],
                    "value": r[1],
                    "category": r[2],
                    "created_at": r[3]
                }
                for r in results
            ]
        return []

    def get_all_memories(self, category=None):
        if category:
            self.cursor.execute(
                "SELECT key, value, category, created_at "
                "FROM memories WHERE category=?",
                (category,)
            )
        else:
            self.cursor.execute(
                "SELECT key, value, category, created_at FROM memories"
            )

        results = self.cursor.fetchall()
        return [
            {
                "key": r[0],
                "value": r[1],
                "category": r[2],
                "created_at": r[3]
            }
            for r in results
        ]

    def save_conversation(
        self, user_message, lucia_response,
        emotion_detected, intent_detected
    ):
        self.cursor.execute("""
            INSERT INTO conversations
            (user_message, lucia_response, emotion_detected, intent_detected)
            VALUES (?, ?, ?, ?)
        """, (user_message, lucia_response, emotion_detected, intent_detected))
        self.connection.commit()

    def save_learned_info(self, topic, contents, verified=False):
        self.cursor.execute("""
            INSERT INTO learned_knowledge (topic, contents, verified)
            VALUES (?, ?, ?)
        """, (topic, contents, 1 if verified else 0))
        self.connection.commit()
        print(f"[LEARNING] Learned: {topic}")

    def get_learned_info(self, topic):
        self.cursor.execute("""
            SELECT contents, verified FROM learned_knowledge
            WHERE topic LIKE ?
            ORDER BY created_at DESC
        """, (f"%{topic}%",))

        results = self.cursor.fetchall()
        return [
            {
                "content": r[0],
                "verified": bool(r[1])
            }
            for r in results
        ]

    def get_recent_conversations(self, limit=5):
        self.cursor.execute("""
            SELECT user_message, lucia_response,
                   emotion_detected, intent_detected, timestamp
            FROM conversations
            ORDER BY timestamp DESC LIMIT ?
        """, (limit,))

        results = self.cursor.fetchall()
        return [
            {
                "user": r[0],
                "lucia": r[1],
                "emotion": r[2],
                "intent": r[3],
                "time": r[4]
            }
            for r in results
        ]

    def delete_memory(self, key):
        self.cursor.execute(
            "DELETE FROM memories WHERE key=?", (key,)
        )
        self.connection.commit()
        print(f"[MEMORY] Deleted: {key}")

    # ✅ FIX: Close se pehle check karo
    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print("[MEMORY] Memory system closed.")
        except Exception as e:
            print(f"[MEMORY] Close error: {e}")