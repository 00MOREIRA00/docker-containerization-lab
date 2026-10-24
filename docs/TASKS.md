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
- [ ] Documentar em `docs/tutoriais/api/03-docker-compose.md`

## Etapa 5 — Múltiplos ambientes

- [ ] Criar `docker-compose.dev.yml`, `docker-compose.staging.yml`, `docker-compose.prod.yml`
- [ ] Usar arquivos de config separados por ambiente (`.env.dev`, `.env.staging`, `.env.prod`)
- [ ] Documentar as diferenças entre os ambientes
- [ ] Documentar em `docs/tutoriais/api/04-multiplos-ambientes.md`

## Etapa 6 — Multi-stage build

- [ ] Reescrever o `Dockerfile` com multi-stage (build stage + runtime stage)
- [ ] Comparar tamanho da imagem antes e depois
- [ ] Documentar em `docs/tutoriais/api/05-multistage.md`

## Etapa 7 — Registry e Push

- [ ] Fazer o push da imagem para o Docker Hub (ou registry escolhido)
- [ ] Documentar o fluxo de tag + push
- [ ] Documentar em `docs/tutoriais/api/06-registry.md`

## Etapa 8 — Boas práticas e segurança

- [ ] Revisar o `Dockerfile` final contra as boas práticas
- [ ] Checar: usuário não-root, `.dockerignore`, camadas desnecessárias, segredos expostos
- [ ] Documentar em `docs/tutoriais/api/07-boas-praticas.md`

## Etapa 9 — Documentação geral

- [ ] Corrigir typos em `docs/01-geral.md` ("paa contruir", "desceve")
- [ ] Escrever o `README.md` do repositório com visão geral e como rodar
- [ ] Revisar todos os arquivos de `docs/` para consistência
