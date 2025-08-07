# orchestrator-api

Gateway entre a interface do usuário e os serviços de NLP (`nl-query`) e execução (`query-engine`).


## Endpoints
- POST `/query` → body `QueryRequest { question: string }` → chama `nl-query` e depois `query-engine`.

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