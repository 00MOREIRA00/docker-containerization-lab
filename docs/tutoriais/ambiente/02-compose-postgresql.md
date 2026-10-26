# Docker Compose: PostgreSQL local

O arquivo `docker-compose.yml`, na raiz do projeto, executa somente o banco
PostgreSQL. A API e o Alembic são executados localmente, fora dos containers.

## Configuração do serviço

```yaml
name: dockerfile-trainer

services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?defina POSTGRES_PASSWORD no arquivo .env}
      POSTGRES_DB: ${POSTGRES_DB:-pauta}
    ports:
      - "127.0.0.1:${POSTGRES_PORT:-5432}:5432"
    volumes:
      - pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U \"$${POSTGRES_USER}\" -d \"$${POSTGRES_DB}\""]
      interval: 5s
      timeout: 5s
      retries: 10
      start_period: 10s
    networks:
      - pauta-net

volumes:
  pgdata:

networks:
  pauta-net:
    driver: bridge
```

`name` define o nome do projeto Compose, usado para agrupar os recursos.
O serviço `postgres` utiliza a imagem oficial `postgres:18`.

A declaração de `volumes` fica na raiz do YAML, no mesmo nível de `services`
e `networks`. Dentro do serviço, `volumes` indica onde montar o volume.
A rede `pauta-net`, com driver `bridge`, conecta o container a uma rede Docker
do projeto. A API local acessa o banco pela porta publicada no host.

## Variáveis de ambiente

O Compose lê o `.env` da raiz para preencher os valores do YAML. O arquivo
`.env.example` serve como modelo, sem conter a senha real:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=troque-esta-senha
POSTGRES_DB=pauta
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

| Variável | Uso |
| --- | --- |
| `POSTGRES_USER` | Usuário criado na primeira inicialização. Padrão: `postgres`. |
| `POSTGRES_PASSWORD` | Senha obrigatória para inicializar o banco. |
| `POSTGRES_DB` | Banco criado na primeira inicialização. Padrão: `pauta`. |
| `POSTGRES_PORT` | Porta publicada na máquina. Padrão: `5432`. |
| `POSTGRES_HOST` | Host usado pela aplicação local: `localhost`. Não é enviado ao container pelo Compose. |

A sintaxe `${VAR:-valor}` usa o valor padrão quando a variável está ausente ou
vazia. `${VAR:?mensagem}` impede a execução e mostra a mensagem quando falta
um valor obrigatório.

O `.env` local foi criado com uma senha aleatória e está ignorado pelo Git.
Para preparar outro ambiente, copie o exemplo e defina uma nova senha:

```powershell
Copy-Item .env.example .env
```

Não sobrescreva seu `.env` existente se ele já contém as credenciais utilizadas.
Alterar usuário, senha ou nome do banco no arquivo não reconfigura um volume
que já foi inicializado.

## Publicação da porta e localhost

```yaml
- "127.0.0.1:${POSTGRES_PORT:-5432}:5432"
```

O mapeamento segue o formato `IP_LOCAL:PORTA_LOCAL:PORTA_DO_CONTAINER`.

- `127.0.0.1` é o endereço de loopback: aponta para a própria máquina em qualquer
  computador. Não é seu IP público nem identifica sua máquina na rede.
- `${POSTGRES_PORT:-5432}` define a porta na sua máquina.
- O último `5432` é a porta em que o PostgreSQL escuta dentro do container.

Essa configuração limita a publicação à interface local. A API e o DBeaver,
executados na sua máquina, usam `localhost` e a porta configurada no `.env`.
O endereço `127.0.0.1` pode ser versionado no Compose sem revelar seu IP.

## Persistência dos dados

O volume nomeado `pgdata` preserva os dados quando o container é removido ou
recriado. Na imagem PostgreSQL 18, ele é montado em `/var/lib/postgresql`,
e o diretório de dados padrão fica em `/var/lib/postgresql/18/docker`.

O bind mount de `./initdb` foi removido. A criação e a evolução das tabelas
ficam sob responsabilidade das migrations do Alembic. Também foi removido
o preload de `pg_stat_statements`, pois essa extensão não é utilizada no projeto.

## Healthcheck e inicialização

O healthcheck executa `pg_isready` dentro do container para verificar se o
PostgreSQL está aceitando conexões. Ele usa intervalo e timeout de 5 segundos,
10 tentativas e um período inicial de tolerância de 10 segundos.

No comando, `$$` impede que o Compose substitua a variável antecipadamente.
Assim, o shell dentro do container lê `POSTGRES_USER` e `POSTGRES_DB`.
Esse teste verifica a disponibilidade do servidor; não verifica migrations
nem substitui uma conexão autenticada pela aplicação.

Na raiz do projeto, execute:

```powershell
docker compose up -d --wait
```

`-d` mantém o container em segundo plano. `--wait` aguarda o serviço ficar
saudável antes de retornar. É opcional: com `docker compose up -d`, o comando
retorna antes de necessariamente o banco estar pronto para aceitar conexões.

Para consultar o estado e os logs:

```powershell
docker compose ps
docker compose logs postgres
```

## Conexão pelo DBeaver

Crie uma conexão PostgreSQL usando os valores do `.env`:

| Campo | Valor padrão |
| --- | --- |
| Host | `localhost` |
| Porta | `5432` |
| Database | `pauta` |
| Usuário | `postgres` |
| Senha | Valor de `POSTGRES_PASSWORD` no `.env` local |

A conexão pelo DBeaver foi realizada com sucesso, confirmando o acesso ao banco
com as credenciais configuradas.

## API e migrations fora do Docker

Com o banco iniciado, execute dentro de `integracao-hellow`:

```powershell
uv run --env-file ../.env alembic upgrade head
uv run --env-file ../.env uvicorn main:app --reload --port 8001
```

O primeiro comando aplica as migrations; o segundo inicia a API, cuja
documentação fica em http://localhost:8001/docs. O parâmetro `--env-file`
carrega as variáveis na execução local; o Python não lê o `.env` automaticamente.

A conexão em `provider/database.py` usa as variáveis `POSTGRES_*`. Se
`DATABASE_URL` estiver definida no ambiente, ela tem prioridade. Para este
banco local, use o driver `postgresql+psycopg` e o host `localhost`.

Após alterar os models, gere e revise uma nova migration antes de aplicá-la:

```powershell
uv run --env-file ../.env alembic revision --autogenerate -m "descreve a alteracao"
uv run --env-file ../.env alembic upgrade head
uv run --env-file ../.env alembic current
```

A migration inicial cria `canais`, e o Alembic registra a revisão na tabela
`alembic_version`. As rotas utilizam services e persistem os canais no
PostgreSQL; a conexão disponível, por si só, não substitui a aplicação das
migrations.

## Encerrar o ambiente

Na raiz do projeto:

```powershell
docker compose down
```

Esse comando remove o container e a rede, preservando os dados no volume.
Use `docker compose down -v` somente quando quiser apagar também o volume
e todos os dados do banco.
