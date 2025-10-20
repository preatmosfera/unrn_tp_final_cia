from typing import TypedDict, List, Dict, Any

class CookingAgentState(TypedDict):
    """
    Define el estado que fluye a través del grafo.
    """
    recipe_name: str           
    required_ingredients: List[str]
    available_ingredients: List[str]
    missing_ingredients: List[str]
    decision: str              
    notion_report_data: Dict[str, Any]
