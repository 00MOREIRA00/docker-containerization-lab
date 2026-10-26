# dockerfile-cheatsheet

## Banco local com Docker Compose

O Compose executa somente o PostgreSQL. A API e o Alembic rodam localmente.
Na raiz, copie o exemplo, ajuste a senha no `.env` e inicie o banco:

```powershell
Copy-Item .env.example .env
docker compose up -d --wait
```

O banco fica acessivel em `localhost:5432`, com usuario `postgres` e banco
`pauta` por padrao. Altere `POSTGRES_PORT`, `POSTGRES_USER` e `POSTGRES_DB`
no `.env` se necessario. A porta e publicada apenas na interface local.
Os dados persistem no volume `pgdata`.

## API e Alembic locais

Dentro de `integracao-hellow`, use o mesmo `.env` da raiz com `uv --env-file`:

```powershell
cd integracao-hellow
uv run --env-file ../.env alembic upgrade head
uv run --env-file ../.env uvicorn main:app --reload --port 8001
```

A documentacao da API fica em http://localhost:8001/docs. A conexao usa as
variaveis `POSTGRES_*` do `.env`, com host `localhost`. Tambem e possivel definir
`DATABASE_URL` no ambiente; quando presente, ela tem prioridade sobre essas
variaveis. O Python nao carrega `.env` automaticamente; os comandos acima
fazem isso pelo uv.

O esquema e gerenciado pelo Alembic, sem scripts `initdb` nem `create_all()`.
A migration inicial cria `canais`. As rotas atuais ainda usam uma lista em
memoria e nao persistem os dados nessa tabela.

## Criar e aplicar migrations

Apos alterar os models, com o banco iniciado, execute dentro de
`integracao-hellow`:

```powershell
uv run --env-file ../.env alembic revision --autogenerate -m "descreve a alteracao"
```

Revise o arquivo gerado em `migrations/versions` antes de aplicar:

```powershell
uv run --env-file ../.env alembic upgrade head
uv run --env-file ../.env alembic current
uv run --env-file ../.env alembic check
```

Nao e necessario reconstruir imagens para alterar a API ou criar migrations.
A migration inicial espera que a tabela `canais` ainda nao exista; um banco
populado fora do Alembic precisa ser reconciliado antes da primeira execucao.

Na raiz, `docker compose down` encerra o banco e preserva os dados.
`docker compose down -v` tambem remove o volume e seus dados. Alterar usuario,
senha ou nome do banco no `.env` nao reconfigura um volume ja inicializado.

## Ambientes Docker

O repositorio possui um Compose separado para cada ambiente:

```text
docker-compose.dev.yml
docker-compose.staging.yml
docker-compose.prod.yml
```

Essa separacao serve para demonstrar como configuracoes, portas, redes e
volumes podem ser isolados entre desenvolvimento, staging e producao.

O ambiente `dev` e destinado ao desenvolvimento local, com reload da API e
portas acessiveis no host. Os ambientes `staging` e `prod` sao simulacoes
locais para aprendizado e validacao da separacao entre ambientes; nao devem
ser tratados como uma infraestrutura corporativa de homologacao ou producao.

Cada ambiente usa seu proprio arquivo de variaveis. Os arquivos reais nao sao
versionados; crie-os a partir dos exemplos:

```powershell
Copy-Item .env.dev.example .env.dev
Copy-Item .env.staging.example .env.staging
Copy-Item .env.prod.example .env.prod
```

Depois, ajuste as senhas nos arquivos reais e inicie o ambiente desejado:

```powershell
docker compose -f docker-compose.dev.yml up --build -d
docker compose -f docker-compose.staging.yml up --build -d
docker compose -f docker-compose.prod.yml up --build -d
```

Os arquivos `.env.dev`, `.env.staging` e `.env.prod` sao ignorados pelo Git.

Em uma empresa, staging e producao normalmente utilizariam uma plataforma de
deploy, banco gerenciado, secrets manager, observabilidade e alta
disponibilidade.

## Documentação

Consulte o [índice da documentação](docs/README.md). Os tutoriais estão
organizados em três trilhas:

- [API](docs/tutoriais/api/README.md)
- [Ambiente](docs/tutoriais/ambiente/README.md)
- [Dockerfile](docs/tutoriais/dockerfile/README.md)
