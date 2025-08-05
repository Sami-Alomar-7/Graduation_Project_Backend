from src.language_models.prompts import name_query_prompt, profile_update_prompt, summary_prompt
from src.language_models.llms import name_query_llm, profile_update_llm, summary_llm
from src.schemas.states import State
from src.preprocessors.text_splitters import TextChunker
from src.databases.database import character_db
from src.schemas.data_classes import Profile
import os

def chunker(state: State):
    """
    Node that takes the file path from the state and yields chunks using a generator for memory efficiency.
    Only the current chunk is kept in the state.
    Also stores each chunk in the database and tracks chunk_id mapping.
    """
    file_path = state['file_path']
    
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    chunker = TextChunker(chunk_size=5000, chunk_overlap=200)
    
    chunks = chunker.chunk_text_arabic_optimized(text)
    
    # Store each chunk in the database and keep mapping from chunk_index to chunk_id
    chunk_index_to_id = {}
    for idx, chunk in enumerate(chunks):
        chunk_id = character_db.insert_chunk(idx, chunk)
        chunk_index_to_id[idx] = chunk_id
    # Re-create the generator for actual processing
    def chunk_generator():
        for chunk in chunks:
            yield chunk
    gen = chunk_generator()
    return {
        'chunk_generator': gen,
        'chunk_index_to_id': chunk_index_to_id
    }
    
    
def first_name_querier(state: State):
    """
    Node that queries the name of the character in the current chunk.
    """
    third_of_length_of_previous_chunk = len(state['previous_chunk'])//3
    
    context = str(state['previous_chunk'][2 * third_of_length_of_previous_chunk:]) + " " + str(state['current_chunk'])
    
    chain_input = {
        "text": str(context)
    }
    
    chain = name_query_prompt | name_query_llm
    
    response = chain.invoke(chain_input)
    
    characters = response.characters if hasattr(response, 'characters') else []
    
    return {
        'last_appearing_characters': characters,
        'chunk_index_to_id': state.get('chunk_index_to_id', {})
    } 
    
def second_name_querier(state: State):
    """
    Node that queries the name of the character in the last summary.
    """
    context = state['last_summary']
    
    chain_input = {
        "text": str(context)
    }
    
    chain = name_query_prompt | name_query_llm
    
    response = chain.invoke(chain_input)
    
    characters = response.characters if hasattr(response, 'characters') else []
    
    return {
        'last_appearing_characters': characters,
        'chunk_index_to_id': state.get('chunk_index_to_id', {})
    } 


def profile_retriever_creator(state: State):
    """
    Node that creates a new profile or retrieves an existing one.
    Uses last_appearing_characters to create profiles for the current chunk only.
    No longer stores or retrieves from the characters table.
    """
    last_appearing_characters = state['last_appearing_characters']
    profiles = []
    for character in last_appearing_characters:
        name = character.name
        hint = character.hint
        # Only create a new profile for this chunk, do not store in characters table
        profile = Profile(
            name=name,
            hint=hint,
            age='',
            role='',
            physical_characteristics=[],
            personality='',
            events=[],
            relationships=[],
            aliases=[],
            id='',
        )
        profiles.append(profile)
    return {'last_profiles': profiles, 'chunk_index_to_id': state.get('chunk_index_to_id', {})}


def profile_refresher(state: State):
    """
    Node that refreshes the profiles based on the current chunk.
    Stores each extracted character profile for the current chunk in the chunk_character_profiles table only.
    """
    chain_input = {
        "text": str(state['last_summary']),
        "profiles": str(state['last_profiles'])
    }
    chain = profile_update_prompt | profile_update_llm
    response = chain.invoke(chain_input)
    if response is None or not hasattr(response, 'profiles') or response.profiles is None:
        print("Warning: Gemini returned no profiles (possibly due to prohibited content). Skipping this chunk.")
        return {
            'last_profiles': state.get('last_profiles', []),
            'chunk_index_to_id': state.get('chunk_index_to_id', {})
        }
    updated_profiles = []
    chunk_index = state.get('chunk_index', 0)
    chunk_index_to_id = state.get('chunk_index_to_id', {})
    chunk_id = chunk_index_to_id.get(chunk_index, None)
    for profile_data in response.profiles:
        profile = Profile(
            name=profile_data.name,
            hint=profile_data.hint,
            age=profile_data.age,
            role=profile_data.role,
            physical_characteristics=profile_data.physical_characteristics,
            personality=profile_data.personality,
            events=profile_data.events,
            relationships=profile_data.relations,
            aliases=profile_data.aliases,
            id=profile_data.id
        )
        updated_profiles.append(profile)
        updated_profile_dict = {
            'name': profile_data.name,
            'hint': profile_data.hint,
            'age': profile_data.age,
            'role': profile_data.role,
            'physical_characteristics': profile_data.physical_characteristics,
            'personality': profile_data.personality,
            'events': profile_data.events,
            'relationships': profile_data.relations,
            'aliases': profile_data.aliases,
        }
        # Only store in chunk_character_profiles table
        if chunk_id is not None:
            character_db.insert_chunk_character_profile(chunk_id, updated_profile_dict)
    return {
        'last_profiles': updated_profiles,
        'chunk_index_to_id': state.get('chunk_index_to_id', {})
    }

def chunk_updater(state: State):
    """
    Node that updates the previous and current chunks in the state.
    """
    try:
        current_chunk = next(state['chunk_generator'])
        # Increment chunk_index in state
        chunk_index = state.get('chunk_index', 0) + 1
        return {
            'previous_chunk': state.get('current_chunk', ''),
            'current_chunk': current_chunk,
            'no_more_chunks': False,
            'chunk_index': chunk_index,
            'chunk_index_to_id': state.get('chunk_index_to_id', {})
        }
    except StopIteration:
        return {'no_more_chunks': True, 'chunk_index_to_id': state.get('chunk_index_to_id', {})}

    

def summarizer(state: State):
    """
    Node that summarizes the text based on the profiles.
    """
    third_of_length_of_last_summary = len(state['last_summary'])//3
    context = str(state['last_summary'][2 * third_of_length_of_last_summary:]) + " " + str(state['current_chunk'])
    chain_input = {
        "text": context,
        "names": str(state['last_appearing_characters'])
    }
    chain = summary_prompt | summary_llm
    response = chain.invoke(chain_input)
    
    return {'last_summary': response.summary, 'chunk_index_to_id': state.get('chunk_index_to_id', {})}