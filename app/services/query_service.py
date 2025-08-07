import httpx

QUERY_ENGINE_URL = "http://query-engine:8002/execute"

async def execute_query(sql_query: str) -> dict:
    payload = {"query": sql_query}

    async with httpx.AsyncClient() as client:
        response = await client.post(QUERY_ENGINE_URL, json=payload)
        response.raise_for_status()
        return response.json()
