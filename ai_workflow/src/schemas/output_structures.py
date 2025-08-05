from pydantic import BaseModel, Field

class Character(BaseModel):
    """Single character with name and hint."""
    name: str = Field(description="اسم الشخصية")
    hint: str = Field(description="تلميح عن الشخصية")

class NameQuerier(BaseModel):
    """Use this schema to format the name query output."""
    characters: list[Character] = Field(description="قائمة بالشخصيات الموجودة في النص")

class ProfileData(BaseModel):
    """Single profile data for a character."""
    name: str = Field(description="اسم الشخصية")
    hint: str = Field(description="تلميح عن الشخصية")
    age: str = Field(description="العمر")
    role: str = Field(description="الدور")
    physical_characteristics: list[str] = Field(description="الصفات الجسدية للشخصية")
    personality: str = Field(description="وصف الشخصية للشخصية")
    events: list[str] = Field(description="الأحداث التي حدثت في حياة الشخصية")
    relations: list[str] = Field(description="العلاقات التي لدى الشخصية")
    aliases: list[str] = Field(description="اسماء اخرى للشخصية")
    id: str = Field(description="الـid للشخصية")

class ProfileRefresher(BaseModel):
    """Use this schema to format the profile refresher output."""
    profiles: list[ProfileData] = Field(description="قائمة من البروفايلات المحدثة للشخصيات")

class Summary(BaseModel):
    """Use this schema to format the summary output."""
    summary: str = Field(description="ملخص النص")