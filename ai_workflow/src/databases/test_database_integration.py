#!/usr/bin/env python3
"""
Test script to verify the database integration with LangGraph nodes.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.databases.database import CharacterDatabase
from src.schemas.states import State


def test_database_integration():
    """Test the database integration with the LangGraph state."""
    print("=== Testing Database Integration ===")
    
    # Initialize database
    db = CharacterDatabase("test_integration.sqlite")
    
    # Create a test state
    test_state = State({
        'file_path': 'resources/texts/نـادي المـوت_djvu.txt',
        'chunk_generator': None,
        'current_chunk': 'This is a test chunk with some Arabic text.',
        'last_profile': None,
        'character_db': db,
        'current_character_ids': [],
        'processed_characters': []
    })
    
    print("1. Testing state initialization with database...")
    print(f"Database instance: {test_state['character_db']}")
    print(f"Initial character count: {db.get_character_count()}")
    
    # Simulate storing a character profile
    print("\n2. Testing character profile storage...")
    test_profile = {
        "name": "أحمد",
        "age": 35,
        "role": "detective",
        "raw_response": "This is a test response from the LLM",
        "chunk_text": "This is a test chunk...",
        "chunk_index": 0
    }
    
    character_id = db.insert_character("أحمد", test_profile, "test character")
    print(f"Inserted character with ID: {character_id}")
    
    # Update the state
    test_state['current_character_ids'] = [character_id]
    test_state['processed_characters'] = [character_id]
    
    print(f"Updated state with character ID: {test_state['current_character_ids']}")
    print(f"Processed characters: {test_state['processed_characters']}")
    
    # Test retrieving the character
    print("\n3. Testing character retrieval...")
    retrieved = db.get_character(character_id)
    if retrieved:
        print(f"Retrieved character: {retrieved['name']} - {retrieved['disambiguation_hint']}")
        print(f"Profile data: {retrieved['profile']['role']}, {retrieved['profile']['age']} years old")
    
    # Test getting all characters
    print("\n4. Testing get all characters...")
    all_characters = db.get_all_characters()
    print(f"Total characters in database: {len(all_characters)}")
    for char in all_characters:
        print(f"  - {char['name']} ({char['disambiguation_hint']}): {char['profile']['role']}")
    
    # Clear test database
    db.clear_database()
    print(f"\nFinal character count after clear: {db.get_character_count()}")
    
    print("\n=== Database integration tests completed successfully! ===")


def test_no_sql_storage():
    """Test the NoSQL-like storage capabilities."""
    print("\n=== Testing NoSQL-like Storage ===")
    
    db = CharacterDatabase("test_nosql_storage.sqlite")
    
    # Test storing complex nested data
    complex_profile = {
        "basic_info": {
            "name": "فاطمة",
            "age": 25,
            "occupation": "teacher"
        },
        "story_development": {
            "chapter_1": {
                "introduction": "First appearance",
                "key_events": ["met the detective", "witnessed crime"],
                "character_traits": ["nervous", "helpful"]
            },
            "chapter_2": {
                "development": "Grew more confident",
                "key_events": ["provided testimony", "helped investigation"],
                "character_traits": ["confident", "determined", "helpful"]
            }
        },
        "relationships": {
            "friends": ["أحمد", "علي"],
            "enemies": [],
            "romantic": "none mentioned"
        },
        "metadata": {
            "importance_level": "major character",
            "first_appearance": "page 15",
            "last_appearance": "page 245",
            "total_mentions": 47
        }
    }
    
    character_id = db.insert_character("فاطمة", complex_profile, "the teacher from Alexandria")
    print(f"Inserted complex profile with ID: {character_id}")
    
    # Retrieve and verify the complex structure
    retrieved = db.get_character(character_id)
    if retrieved:
        profile = retrieved['profile']
        print(f"Retrieved complex profile:")
        print(f"  - Name: {profile['basic_info']['name']}")
        print(f"  - Age: {profile['basic_info']['age']}")
        print(f"  - Chapters: {len(profile['story_development'])}")
        print(f"  - Friends: {len(profile['relationships']['friends'])}")
        print(f"  - Importance: {profile['metadata']['importance_level']}")
        print(f"  - Total mentions: {profile['metadata']['total_mentions']}")
        
        # Test nested data access
        chapter_2_traits = profile['story_development']['chapter_2']['character_traits']
        print(f"  - Chapter 2 traits: {', '.join(chapter_2_traits)}")
    
    # Clear test database
    # db.clear_database()
    print("\n=== NoSQL storage tests completed! ===")


def main():
    """Run all database integration tests."""
    print("Testing Database Integration with LangGraph")
    print("=" * 60)
    
    test_database_integration()
    test_no_sql_storage()
    
    print("\n" + "=" * 60)
    print("All database integration tests completed successfully!")


if __name__ == "__main__":
    main() 