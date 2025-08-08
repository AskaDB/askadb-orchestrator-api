# askadb-orchestrator-api

Gateway entre a interface do usuário e os serviços de NLP (`askadb-nl-query`) e execução (`askadb-query-engine`).

## Endpoints
- POST `/query` → body `QueryRequest { question: string }` → chama `askadb-nl-query` e depois `askadb-query-engine`.

## Rodando localmente
```bash
make install
make run PORT=8000
```

## Docker
```bash
make docker-build
make docker-run
```