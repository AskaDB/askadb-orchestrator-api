from pydantic import BaseModel
from typing import List, Dict

class QueryRequest(BaseModel):
    question: str
    schema: List[Dict[str, List[str]]]  # Ex: [{"table": "vendas", "columns": ["regiao", "valor", "ano"]}]
