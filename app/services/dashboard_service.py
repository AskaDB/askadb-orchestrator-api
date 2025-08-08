import httpx
import json
from typing import List, Dict, Any

class DashboardService:
    def __init__(self):
        self.dashboard_url = "http://localhost:8003/suggest"
    
    async def generate_suggestions(self, data: List[Dict[str, Any]], question: str) -> Dict[str, Any]:
        """Generate dashboard suggestions using the dashboard core service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.dashboard_url,
                    json={
                        "data": data,
                        "question": question
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    # Fallback to basic suggestions
                    return self._generate_fallback_suggestions(data, question)
                    
        except Exception as e:
            print(f"Dashboard service error: {e}")
            return self._generate_fallback_suggestions(data, question)
    
    def _generate_fallback_suggestions(self, data: List[Dict[str, Any]], question: str) -> Dict[str, Any]:
        """Generate basic fallback suggestions when dashboard service is unavailable"""
        if not data:
            return {"suggestions": []}
        
        # Simple rule-based suggestions
        question_lower = question.lower()
        columns = list(data[0].keys()) if data else []
        
        # Find numeric and categorical columns
        numeric_cols = []
        categorical_cols = []
        
        for col in columns:
            if col.lower() in ['sales_amount', 'quantity', 'amount', 'value', 'total']:
                numeric_cols.append(col)
            elif col.lower() in ['region', 'product', 'month', 'category']:
                categorical_cols.append(col)
        
        suggestions = []
        
        # Bar chart suggestion
        if categorical_cols and numeric_cols:
            suggestions.append({
                "type": "bar_chart",
                "title": "Gráfico de Barras",
                "description": "Ideal para comparar valores entre categorias",
                "confidence": 0.8,
                "config": {
                    "type": "bar",
                    "data": {
                        "labels": [row.get(categorical_cols[0], '') for row in data[:10]],
                        "datasets": [{
                            "label": numeric_cols[0],
                            "data": [row.get(numeric_cols[0], 0) for row in data[:10]],
                            "backgroundColor": "#3b82f6"
                        }]
                    }
                },
                "reasoning": "Dados categóricos e numéricos detectados"
            })
        
        # Line chart for time series
        if 'month' in question_lower or any('month' in col.lower() for col in columns):
            suggestions.append({
                "type": "line_chart",
                "title": "Gráfico de Linha",
                "description": "Perfeito para mostrar tendências ao longo do tempo",
                "confidence": 0.9,
                "config": {
                    "type": "line",
                    "data": {
                        "labels": [row.get('month', '') for row in data[:10]],
                        "datasets": [{
                            "label": "Vendas",
                            "data": [row.get('sales_amount', 0) for row in data[:10]],
                            "borderColor": "#3b82f6"
                        }]
                    }
                },
                "reasoning": "Dados temporais detectados"
            })
        
        # Table as fallback
        suggestions.append({
            "type": "table",
            "title": "Tabela de Dados",
            "description": "Apresenta todos os dados de forma organizada",
            "confidence": 0.5,
            "config": {
                "type": "table",
                "data": {
                    "columns": columns,
                    "rows": data[:10]
                }
            },
            "reasoning": "Visualização padrão para qualquer tipo de dados"
        })
        
        return {"suggestions": suggestions}
