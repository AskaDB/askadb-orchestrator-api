import httpx
from typing import Dict, Any
from app.models.query_input import QueryInput

NL_QUERY_URL = "http://askadb-nl-query:8001/translate"

async def translate_question_to_query(request: QueryInput) -> Dict[str, Any]:
    payload = {
        "question": request.question,
        "schema": request.schema,
        "context": request.context,
        "examples": request.examples,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(NL_QUERY_URL, json=payload)
        response.raise_for_status()
        return response.json()
