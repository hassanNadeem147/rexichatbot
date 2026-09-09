from typing import TypedDict
class State(TypedDict):
    """
    This class contains all of the information about the current state of the application.
    """
    text: str
    summarized_text: str
    explain_text: str
    translate_text: str
    podcast: str
    target_language: str
    operation: str