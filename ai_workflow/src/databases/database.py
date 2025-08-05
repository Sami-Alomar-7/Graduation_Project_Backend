import sqlite3
import json
import uuid
from typing import Dict, List, Optional, Any


class CharacterDatabase:
    """
    SQLite database for storing character profiles in a NoSQL-like setup.
    Uses JSON storage for flexible document structure.
    """
    
    def __init__(self, db_path: str = "characters.sqlite"):
        """
        Initialize the character database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with the required table structure."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY,    -- A unique ID we generate (e.g., a UUID)
                    name TEXT NOT NULL,               -- The character's common name (e.g., "Ali")
                    profile_json TEXT                 -- JSON document containing the character profile (including hint)
                );
            """)
            # Table for book chunks
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chunk_index INTEGER NOT NULL,
                    chunk_text TEXT NOT NULL
                );
            """)
            # Table for per-chunk character profiles (no character_name column)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunk_character_profiles (
                    id TEXT PRIMARY KEY,
                    chunk_id INTEGER NOT NULL,
                    profile_json TEXT,
                    FOREIGN KEY(chunk_id) REFERENCES chunks(chunk_id)
                );
            """)
            # Remove character_profile_history table if it exists
            cursor.execute("DROP TABLE IF EXISTS character_profile_history;")
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_chunk_index ON chunks(chunk_index);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunk_character_profiles_chunk_id ON chunk_character_profiles(chunk_id);")
            
            conn.commit()
    
    def insert_character(self, name: str, profile: Dict[str, Any], ) -> str:
        """
        Insert a new character profile into the database.
        
        Args:
            name: Character's name
            profile: Character profile as a dictionary
            
        Returns:
            The generated id
        """
        id = str(uuid.uuid4())
        
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO characters (id, name, profile_json)
                VALUES (?, ?, ?)
            """, (id, name, json.dumps(profile, ensure_ascii=False)))
            conn.commit()
        
        return id
    
    def update_character(self, id: str, profile: Dict[str, Any]) -> bool:
        """
        Update an existing character profile.
        
        Args:
            id: The character's unique ID
            profile: Updated character profile
            
        Returns:
            True if update was successful, False if character not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE characters 
                SET profile_json = ?
                WHERE id = ?
            """, (json.dumps(profile, ensure_ascii=False), id))
            
            conn.commit()
            return cursor.rowcount > 0

    def get_character(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a character profile by ID.
        
        Args:
            id: The character's unique ID
            
        Returns:
            Character profile as dictionary, or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, profile_json
                FROM characters
                WHERE id = ?
            """, (id,))
            
            row = cursor.fetchone()
            if row:
                name, profile_json = row
                profile = json.loads(profile_json)
                return {
                    'id': id,
                    'name': name,
                    'profile': profile
                }
            return None
    
    def find_characters_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Find characters by name (handles multiple characters with same name).
        
        Args:
            name: Character name to search for
            
        Returns:
            List of character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, profile_json
                FROM characters
                WHERE name = ?
            """, (name,))
            
            characters = []
            for row in cursor.fetchall():
                id, name, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'id': id,
                    'name': name,
                    'profile': profile
                })
            
            return characters
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """
        Retrieve all character profiles.
        
        Returns:
            List of all character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, profile_json
                FROM characters
                ORDER BY name
            """)
            
            characters = []
            for row in cursor.fetchall():
                id, name, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'id': id,
                    'name': name,
                    'profile': profile
                })
            
            return characters
    
    def delete_character(self, id: str) -> bool:
        """
        Delete a character profile.
        
        Args:
            id: The character's unique ID
            
        Returns:
            True if deletion was successful, False if character not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM characters WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_characters(self, query: str) -> List[Dict[str, Any]]:
        """
        Search characters by name or hint in profile.
        
        Args:
            query: Search query
            
        Returns:
            List of matching character profiles
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, profile_json
                FROM characters
                WHERE name LIKE ? OR JSON_EXTRACT(profile_json, '$.hint') LIKE ?
                ORDER BY name
            """, (f'%{query}%', f'%{query}%'))
            
            characters = []
            for row in cursor.fetchall():
                id, name, profile_json = row
                profile = json.loads(profile_json)
                characters.append({
                    'id': id,
                    'name': name,
                    'profile': profile
                })
            
            return characters
    
    def get_character_count(self) -> int:
        """
        Get the total number of characters in the database.
        
        Returns:
            Number of characters
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM characters")
            return cursor.fetchone()[0]
    
    def clear_database(self):
        """Clear all character data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM characters")
            conn.commit()

    def insert_chunk(self, chunk_index: int, chunk_text: str) -> int:
        """
        Insert a chunk of the book into the chunks table.
        Args:
            chunk_index: The index of the chunk
            chunk_text: The text of the chunk
        Returns:
            The chunk_id (autoincremented)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chunks (chunk_index, chunk_text)
                VALUES (?, ?)
            """, (chunk_index, chunk_text))
            conn.commit()
            return cursor.lastrowid

    def insert_chunk_character_profile(self, chunk_id: int, profile: Dict[str, Any]) -> str:
        """
        Insert a character profile extracted from a specific chunk.
        Args:
            chunk_id: The chunk's unique ID
            profile: The profile data as a dictionary
        Returns:
            The generated id for the record
        """
        id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chunk_character_profiles (id, chunk_id, profile_json)
                VALUES (?, ?, ?)
            """, (id, chunk_id, json.dumps(profile, ensure_ascii=False)))
            conn.commit()
        return id


# Global database instance
character_db = CharacterDatabase()


def get_character_db() -> CharacterDatabase:
    """Get the global character database instance."""
    return character_db 