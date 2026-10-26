# Múltiplos ambientes

Nesta etapa, a API passa a ter configurações separadas para desenvolvimento,
staging e produção. A separação evita misturar bancos, volumes, portas e
configurações de ambientes diferentes.

## Ambientes disponíveis

| Ambiente | Compose | API | PostgreSQL | Características |
|---|---|---:|---:|---|
| Dev | `docker-compose.dev.yml` | `8001` | `5432` | Reload, código montado e banco exposto localmente |
| Staging | `docker-compose.staging.yml` | `8002` | `5433` | Sem reload, banco separado e configuração próxima da produção |
| Prod | `docker-compose.prod.yml` | `8003` | Não exposto | Sem reload, volume e rede próprios |

Os ambientes usam volumes e redes diferentes:

```text
dev      -> pgdata_dev      / pauta-dev
staging  -> pgdata_staging  / pauta-staging
prod     -> pgdata_prod     / pauta-prod
```

Assim, apagar ou recriar o banco de desenvolvimento não altera os dados de
staging ou produção.

## Arquivos de configuração

Cada ambiente possui um arquivo de variáveis próprio:

```text
.env.dev
.env.staging
.env.prod
```

Os arquivos reais não são versionados, pois podem conter senhas. O repositório
possui apenas os modelos:

```text
.env.dev.example
.env.staging.example
.env.prod.example
```

Crie os arquivos locais com:

```powershell
Copy-Item .env.dev.example .env.dev
Copy-Item .env.staging.example .env.staging
Copy-Item .env.prod.example .env.prod
```

Depois, substitua os valores de `POSTGRES_PASSWORD` por senhas apropriadas.
Os arquivos `.env.*` estão no `.gitignore` e não devem ser adicionados ao Git.

## Iniciando cada ambiente

Desenvolvimento:

```powershell
docker compose -f docker-compose.dev.yml up --build -d
docker compose -f docker-compose.dev.yml run --rm api alembic upgrade head
```

A API fica disponível em `http://localhost:8001`.

Staging:

```powershell
docker compose -f docker-compose.staging.yml up --build -d
docker compose -f docker-compose.staging.yml run --rm api alembic upgrade head
```

A API fica disponível em `http://localhost:8002`.

Produção simulada:

```powershell
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml run --rm api alembic upgrade head
```

A API fica disponível em `http://localhost:8003`. O PostgreSQL permanece
acessível somente dentro da rede do Compose.

Para parar um ambiente, use o mesmo arquivo Compose:

```powershell
docker compose -f docker-compose.dev.yml down
```

Use `down -v` somente quando quiser remover também os dados do volume daquele
ambiente.

## O que muda entre os ambientes

### Desenvolvimento

O ambiente de desenvolvimento prioriza feedback rápido. A API usa `--reload`
e monta o código local no container. O PostgreSQL é publicado em
`localhost:5432` para facilitar inspeção com ferramentas como DBeaver.

### Staging

Staging simula uma execução mais próxima da produção. A API roda sem reload e
usa banco, volume, rede e portas próprios. É o ambiente adequado para validar
migrations e mudanças antes da produção simulada.

### Produção

O Compose de produção não monta o código local e não expõe o PostgreSQL ao
host. A API roda sem reload e os dados ficam no volume exclusivo do ambiente.

## Limites desta simulação

Staging e produção neste repositório são ambientes locais para aprendizado e
validação da separação de configurações. Eles não representam uma infraestrutura
corporativa completa.

Em uma empresa, staging e produção normalmente usariam banco gerenciado,
secrets manager, imagens versionadas em registry, CI/CD, load balancer,
monitoramento, backups e alta disponibilidade. Dependendo da escala, o
Compose seria substituído por Kubernetes, ECS, Nomad ou outra plataforma de
orquestração.
