from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QueryInput(BaseModel):
    question: str
    schema: Optional[Dict[str, Any]] = None
    context: Optional[str] = None
    examples: Optional[List[Dict[str, str]]] = None

class QueryResponse(BaseModel):
    success: bool
    question: str
    sql: str
    data: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    dashboard: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    error: Optional[str] = None
