from langchain.chat_models import init_chat_model
from src.schemas.output_structures import NameQuerier, ProfileRefresher, Summary

profile_update_llm = init_chat_model('google_genai:gemini-2.5-flash', temperature=0.0).with_structured_output(ProfileRefresher)
name_query_llm = init_chat_model('google_genai:gemini-2.5-flash', temperature=0.0).with_structured_output(NameQuerier)
summary_llm = init_chat_model('google_genai:gemini-2.5-flash', temperature=1.0).with_structured_output(Summary)
