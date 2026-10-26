# Decisões técnicas

Este documento registra decisões que afetam a estrutura da aplicação. A ideia
é explicar não apenas o que foi implementado, mas também o motivo e os limites
de cada escolha.

## API com FastAPI

O serviço usa FastAPI por oferecer tipagem, validação com Pydantic e
documentação OpenAPI automática. A aplicação também se integra bem ao
ecossistema ASGI e ao Uvicorn.

## PostgreSQL como banco principal

O PostgreSQL foi escolhido para persistir o catálogo de canais. O banco roda
em container no desenvolvimento e possui um serviço separado dos containers da
API nos arquivos Compose.

O acesso é feito com SQLAlchemy e o driver `psycopg`. A URL de conexão pode ser
fornecida por `DATABASE_URL`; quando ela não existe, a aplicação monta a
conexão a partir das variáveis `POSTGRES_*`.

## Alembic para migrations

O schema não é criado com `Base.metadata.create_all()` durante a inicialização
da API. As alterações de estrutura são versionadas com Alembic e aplicadas
explicitamente:

```powershell
uv run --env-file ../.env alembic upgrade head
```

Isso torna a evolução do banco reproduzível entre desenvolvimento, staging e
produção.

## Services para regras de negócio

As rotas ficam responsáveis por HTTP, dependências e serialização. As
operações sobre canais ficam em `service/canais.py`, o que facilita testes
unitários e evita concentrar toda a regra dentro dos endpoints.

## Exceções e handlers separados

As exceções representam problemas da aplicação, enquanto os handlers
transformam essas exceções em respostas HTTP consistentes. O handler genérico
de erro inesperado não expõe detalhes internos ao consumidor e registra o
stack trace no log.

## Timeouts no acesso ao banco

Foram definidos timeouts de conexão, aquisição de conexão do pool, execução de
comandos SQL e espera por locks. O objetivo é evitar que uma requisição fique
presa indefinidamente por causa do banco.

Esses timeouts não substituem um timeout completo de requisição HTTP; eles
protegem especificamente as etapas de comunicação com o PostgreSQL.

## Configuração por ambiente

Os arquivos `.env.dev`, `.env.staging` e `.env.prod` mantêm configurações,
portas e bancos isolados. Os arquivos reais não são versionados; somente os
arquivos `.example` servem como referência.

Staging e produção são ambientes locais simulados neste repositório. Em um
ambiente corporativo, secrets manager, CI/CD, observabilidade, backups e alta
disponibilidade seriam responsabilidades da plataforma de deploy.

## Imagem multi-stage

O Dockerfile possui os estágios `builder` e `runtime`. Dependências e
ferramentas utilizadas apenas na construção não são mantidas na imagem final.
O runtime executa como usuário não-root e não recebe arquivos `.env` nem
credenciais.

## Escopo atual

Autenticação, autorização, paginação, filtros, rate limiting, métricas e
integrações externas ainda não fazem parte da implementação atual. Esses itens
estão registrados como próximos passos em [API.md](../API.md).
