from typing import TypedDict
from langgraph.graph.message import add_messages
from src.databases.database import CharacterDatabase
from src.schemas.data_classes import Profile, LastAppearingCharacter

class State(TypedDict):
    file_path: str
    chunk_generator: object
    current_chunk: str
    previous_chunk: str
    last_profiles: list[Profile] | None
    last_appearing_characters: list[LastAppearingCharacter] | None
    no_more_chunks: bool
    last_summary: str
    chunk_index: int

initial_state = {
    'file_path': 'resources/texts/بياض الثلج.txt',
    'chunk_generator': None,
    'current_chunk': '',
    'previous_chunk': '',
    'last_profiles': None,
    'last_appearing_characters': None,
    'no_more_chunks': False,
    'last_summary': '',
    'chunk_index': 0
}