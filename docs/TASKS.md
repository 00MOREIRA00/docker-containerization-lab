# Tasks do projeto

## Etapa 1 — API (integracao-hellow)

- [x] Adicionar FastAPI e uvicorn com `uv add`
- [x] Criar os endpoints de Canais (POST, GET, GET by id, PUT, DELETE)
- [x] Usar dados em memória por enquanto (sem banco)
- [x] Garantir que a API sobe com `uv run`

## Etapa 2 — Dockerfile inicial

- [x] Renomear `dockerfile` para `Dockerfile` (D maiúsculo)
- [x] Escrever o `Dockerfile` para a API com `uv`
- [x] Testar o build com `docker build`
- [x] Testar o run com `docker run`
- [x] Documentar a etapa em `docs/tutoriais/api/02-dockerfile.md`

## Etapa 3 — Banco de dados (PostgreSQL)

- [x] Adicionar SQLAlchemy e driver PostgreSQL com `uv add`
- [x] Criar os models e a conexão com o banco
- [x] Testar localmente com PostgreSQL rodando na máquina

## Etapa 4 — Docker Compose (ambiente local)

- [x] Criar `docker-compose.yml` com PostgreSQL
- [x] Configurar variáveis de ambiente via `.env`
- [x] Testar o `docker compose up` do zero
- [x] Documentar em `docs/tutoriais/api/03-docker-compose.md`

## Etapa 5 — Múltiplos ambientes

- [x] Criar `docker-compose.dev.yml`, `docker-compose.staging.yml`, `docker-compose.prod.yml`
- [x] Usar arquivos de config separados por ambiente (`.env.dev`, `.env.staging`, `.env.prod`)
- [x] Documentar as diferenças entre os ambientes
- [x] Documentar em `docs/tutoriais/api/04-multiplos-ambientes.md`

## Etapa 6 — Multi-stage build

- [x] Reescrever o `Dockerfile` com multi-stage (build stage + runtime stage)
- [x] Comparar tamanho da imagem antes e depois
- [x] Documentar em `docs/tutoriais/api/05-multistage.md`

