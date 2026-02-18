"""
Multilingual support through prompt engineering
Uses local Mistral model for translations via prompting
"""
from typing import Dict
from backend.config import SUPPORTED_LANGUAGES


def get_language_instruction(language_code: str) -> str:
    """
    Get language instruction for prompt
    
    Args:
        language_code: ISO language code (en, hi, es, fr, de)
        
    Returns:
        Instruction string for the LLM
    """
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = "en"
    
    language_name = SUPPORTED_LANGUAGES[language_code]
    
    if language_code == "en":
        return "Respond in English."
    else:
        return f"""IMPORTANT: Respond ENTIRELY in {language_name}. 
Translate your complete response to {language_name}.
Do not use English in your response."""


def get_supported_languages() -> Dict[str, str]:
    """Get dictionary of supported languages"""
    return SUPPORTED_LANGUAGES.copy()


def validate_language(language_code: str) -> bool:
    """Check if language is supported"""
    return language_code in SUPPORTED_LANGUAGES
