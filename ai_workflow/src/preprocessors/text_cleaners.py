import re

def clean_text(text):
    # 1. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # 2. Remove extra newlines and replace with single space, then strip leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    # 3. Convert to lowercase (optional, depending on the LLM and task)
    # text = text.lower()
    # 4. Remove Arabic diacritics (harakat) - common in Arabic text preprocessing
    text = re.sub(r'[\u064B-\u0652]', '', text)
    # 5. Remove non-Arabic and non-space characters (keep only Arabic letters, numbers and spaces)
    # This regex keeps Arabic letters, digits, and basic punctuation. Adjust as needed.
    # For a stricter approach, only keep Arabic letters and spaces:
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text) # Keeps only Arabic letters and spaces

    # 6. Normalize some Arabic characters (optional, but good for consistency)
    text = re.sub(r'[\u0622\u0623\u0625]', '\u0627', text) # Normalize Alif forms to bare Alif
    text = re.sub(r'\u0649', '\u064A', text) # Normalize Alif Maqsura to Ya

    return text

with open('resources/texts/أرض زيكولا.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

cleaned_text = clean_text(file_content)