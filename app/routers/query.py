from fastapi import APIRouter
from app.models.query_input import QueryRequest
from app.services import nl_service, query_service

router = APIRouter()

@router.post("/query")
async def process_query(request: QueryRequest):
    # 1. Traduz a pergunta em linguagem natural para uma query SQL
    sql_query = await nl_service.translate_question_to_query(request)

    # 2. Executa a query no engine
    result = await query_service.execute_query(sql_query)

    return result
