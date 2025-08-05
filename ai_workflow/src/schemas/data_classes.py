from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    hint: str
    age: str
    role: str
    physical_characteristics: list[str]
    personality: str
    events: list[str]
    relationships: list[str]
    aliases: list[str]
    id: str
    
@dataclass
class LastAppearingCharacter:
    name: str
    hint: str
    