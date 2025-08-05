#!/usr/bin/env python3
"""
Test script to verify the SQLite database setup and functionality.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.databases.database import CharacterDatabase


def test_database_functionality():
    """Test the database functionality."""
    print("=== Testing Character Database ===")
    
    # Initialize database
    db = CharacterDatabase("test_characters.sqlite")
    
    # Test 1: Insert a character
    print("\n1. Testing character insertion...")
    profile1 = {
        "name": "أحمد",
        "age": 35,
        "role": "detective",
        "physical_characteristics": "tall, dark hair, sharp eyes",
        "personality": "suspicious, intelligent, determined",
        "events": ["discovered the murder weapon", "questioned the suspect"],
        "relationships": ["partner of Fatima", "suspect of Ali"]
    }
    
    character_id1 = db.insert_character("أحمد", profile1, "the detective from Cairo")
    print(f"Inserted character with ID: {character_id1}")
    
    # Test 2: Insert another character with same name
    print("\n2. Testing character with same name...")
    profile2 = {
        "name": "أحمد",
        "age": 28,
        "role": "witness",
        "physical_characteristics": "short, light hair, nervous",
        "personality": "nervous, helpful, honest",
        "events": ["saw the suspect running", "provided alibi"],
        "relationships": ["neighbor of victim", "friend of suspect"]
    }
    
    character_id2 = db.insert_character("أحمد", profile2, "the witness from the market")
    print(f"Inserted second character with ID: {character_id2}")
    
    # Test 3: Retrieve character by ID
    print("\n3. Testing character retrieval by ID...")
    character = db.get_character(character_id1)
    if character:
        print(f"Retrieved character: {character['name']} - {character['disambiguation_hint']}")
        print(f"Profile: {character['profile']['role']}, {character['profile']['age']} years old")
    else:
        print("Failed to retrieve character")
    
    # Test 4: Find characters by name
    print("\n4. Testing character search by name...")
    characters = db.find_characters_by_name("أحمد")
    print(f"Found {len(characters)} characters named أحمد:")
    for char in characters:
        print(f"  - {char['name']} ({char['disambiguation_hint']}): {char['profile']['role']}")
    
    # Test 5: Update character profile
    print("\n5. Testing character profile update...")
    updated_profile = profile1.copy()
    updated_profile["events"].append("found new evidence")
    updated_profile["personality"] = "suspicious, intelligent, determined, experienced"
    
    success = db.update_character(character_id1, updated_profile)
    print(f"Profile update successful: {success}")
    
    # Test 6: Search characters
    print("\n6. Testing character search...")
    search_results = db.search_characters("detective")
    print(f"Found {len(search_results)} characters matching 'detective':")
    for char in search_results:
        print(f"  - {char['name']} ({char['disambiguation_hint']})")
    
    # Test 7: Get all characters
    print("\n7. Testing get all characters...")
    all_characters = db.get_all_characters()
    print(f"Total characters in database: {len(all_characters)}")
    for char in all_characters:
        print(f"  - {char['name']} ({char['disambiguation_hint']}): {char['profile']['role']}")
    
    # Test 8: Get character count
    print("\n8. Testing character count...")
    count = db.get_character_count()
    print(f"Character count: {count}")
    
    # Test 9: Delete a character
    print("\n9. Testing character deletion...")
    success = db.delete_character(character_id2)
    print(f"Character deletion successful: {success}")
    
    # Verify deletion
    remaining_count = db.get_character_count()
    print(f"Remaining characters: {remaining_count}")
    
    # Test 10: Clear database
    print("\n10. Testing database clear...")
    db.clear_database()
    final_count = db.get_character_count()
    print(f"Characters after clear: {final_count}")
    
    print("\n=== Database tests completed successfully! ===")


def test_no_sql_functionality():
    """Test the NoSQL-like functionality with flexible JSON storage."""
    print("\n=== Testing NoSQL-like Functionality ===")
    
    db = CharacterDatabase("test_nosql.db")
    
    # Test flexible JSON storage
    flexible_profile = {
        "basic_info": {
            "name": "فاطمة",
            "age": 25,
            "occupation": "teacher"
        },
        "appearance": {
            "height": "medium",
            "hair": "black",
            "eyes": "brown",
            "distinguishing_features": ["small scar on left cheek"]
        },
        "personality": {
            "traits": ["kind", "intelligent", "curious"],
            "strengths": ["good listener", "patient"],
            "weaknesses": ["sometimes too trusting"]
        },
        "background": {
            "origin": "Alexandria",
            "education": "university graduate",
            "family": {
                "parents": "deceased",
                "siblings": "one brother"
            }
        },
        "relationships": {
            "friends": ["أحمد", "علي"],
            "romantic": "none mentioned",
            "professional": ["colleagues at school"]
        },
        "story_arc": {
            "introduction": "chapter 1",
            "key_events": [
                "met the detective",
                "witnessed the crime",
                "helped with investigation"
            ],
            "character_development": "grew more confident"
        },
        "metadata": {
            "first_appearance": "page 15",
            "last_appearance": "page 245",
            "importance_level": "major character"
        }
    }
    
    character_id = db.insert_character("فاطمة", flexible_profile, "the teacher from Alexandria")
    print(f"Inserted flexible profile for فاطمة with ID: {character_id}")
    
    # Retrieve and verify the flexible structure
    retrieved = db.get_character(character_id)
    if retrieved:
        profile = retrieved['profile']
        print(f"Retrieved flexible profile:")
        print(f"  - Name: {profile['basic_info']['name']}")
        print(f"  - Age: {profile['basic_info']['age']}")
        print(f"  - Occupation: {profile['basic_info']['occupation']}")
        print(f"  - Personality traits: {', '.join(profile['personality']['traits'])}")
        print(f"  - Story importance: {profile['metadata']['importance_level']}")
        print(f"  - Key events: {len(profile['story_arc']['key_events'])} events recorded")
    
    # Clear test database
    db.clear_database()
    print("\n=== NoSQL functionality tests completed! ===")


def main():
    """Run all database tests."""
    print("Testing SQLite Character Database")
    print("=" * 50)
    
    test_database_functionality()
    test_no_sql_functionality()
    
    print("\n" + "=" * 50)
    print("All database tests completed successfully!")


if __name__ == "__main__":
    main() 