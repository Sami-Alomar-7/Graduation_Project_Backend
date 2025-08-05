from django.db import models
from chunks.models import Chunk
import uuid


class Profile(models.Model):
    """
    Model for storing character profiles extracted from book chunks by the AI workflow.
    Each profile represents a character's information extracted from a specific chunk.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chunk = models.ForeignKey(Chunk, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=255, help_text="Character's name")
    hint = models.TextField(help_text="Context hint about the character")
    age = models.CharField(max_length=100, blank=True, help_text="Character's age")
    role = models.CharField(max_length=255, blank=True, help_text="Character's role in the story")
    personality = models.TextField(blank=True, help_text="Character's personality traits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # JSON fields for complex data
    physical_characteristics = models.JSONField(
        default=list, 
        help_text="List of physical characteristics"
    )
    events = models.JSONField(
        default=list, 
        help_text="List of events involving this character"
    )
    relationships = models.JSONField(
        default=list, 
        help_text="List of relationships with other characters"
    )
    aliases = models.JSONField(
        default=list, 
        help_text="List of aliases or alternative names"
    )

    class Meta:
        unique_together = ['chunk', 'name']
        ordering = ['chunk', 'name']
        indexes = [
            models.Index(fields=['chunk', 'name']),
            models.Index(fields=['name']),
            models.Index(fields=['chunk']),
        ]

    def __str__(self):
        return f"{self.name} in {self.chunk}"

    @property
    def book(self):
        """Get the book this profile belongs to"""
        return self.chunk.book

    def to_dict(self):
        """Convert profile to dictionary format compatible with AI workflow"""
        return {
            'id': str(self.id),
            'name': self.name,
            'hint': self.hint,
            'age': self.age,
            'role': self.role,
            'physical_characteristics': self.physical_characteristics,
            'personality': self.personality,
            'events': self.events,
            'relationships': self.relationships,
            'aliases': self.aliases,
        }

    @classmethod
    def from_dict(cls, chunk, profile_dict):
        """Create a profile from dictionary format"""
        return cls(
            chunk=chunk,
            name=profile_dict.get('name', ''),
            hint=profile_dict.get('hint', ''),
            age=profile_dict.get('age', ''),
            role=profile_dict.get('role', ''),
            personality=profile_dict.get('personality', ''),
            physical_characteristics=profile_dict.get('physical_characteristics', []),
            events=profile_dict.get('events', []),
            relationships=profile_dict.get('relationships', []),
            aliases=profile_dict.get('aliases', []),
        )
