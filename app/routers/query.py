from fastapi import APIRouter, HTTPException
from app.models.query_input import QueryInput, QueryResponse
from app.services.nl_service import translate_question_to_query
from app.services.query_service import execute_query
from app.services.dashboard_service import DashboardService
import httpx
import asyncio

router = APIRouter()
dashboard_service = DashboardService()

@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryInput):
    """Process natural language query and return results with dashboard"""
    try:
        # Step 1: Convert NL to SQL
        nl_result = await translate_question_to_query(request)
        if not nl_result.get("query"):
            raise HTTPException(status_code=400, detail="Failed to generate SQL query")
        
        sql_query = nl_result["query"]
        
        # Step 2: Execute SQL query
        query_result = await execute_query(sql_query)
        if not query_result.get("success"):
            raise HTTPException(status_code=400, detail=f"Query execution failed: {query_result.get('error')}")
        
        # Step 3: Generate dashboard suggestions
        dashboard_result = await dashboard_service.generate_suggestions(
            query_result.get("data", []),
            request.question
        )
        
        # Step 4: Generate follow-up suggestions
        suggestions = nl_result.get("suggested_follow_up_questions", [])
        
        return QueryResponse(
            success=True,
            question=request.question,
            sql=sql_query,
            data=query_result.get("data"),
            metadata=query_result.get("metadata"),
            dashboard=dashboard_result.get("suggestions", [])[0] if dashboard_result.get("suggestions") else None,
            suggestions=suggestions
        )
        
    except Exception as e:
        return QueryResponse(
            success=False,
            question=request.question,
            sql="",
            error=str(e)
        )
