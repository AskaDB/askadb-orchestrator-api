import httpx
from app.models.query_input import QueryRequest

NL_QUERY_URL = "http://nl-query:8001/translate"

async def translate_question_to_query(request: QueryRequest) -> str:
    payload = {
        "question": request.question,
        "schema": request.schema
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(NL_QUERY_URL, json=payload)
        response.raise_for_status()
        return response.json()["query"]
