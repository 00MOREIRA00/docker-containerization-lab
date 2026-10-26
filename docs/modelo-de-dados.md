# Modelo de dados

## Visão geral

O banco possui uma entidade principal: `Canal`. Cada registro representa um
fluxo de integração entre um sistema de origem e um sistema de destino em um
ambiente específico.

```text
Canal
├── id
├── nome
├── sistema_origem
├── sistema_destino
├── status
├── ambiente
└── criado_em
```

No estado atual não existem relacionamentos com outras tabelas.

## Tabela `canais`

| Coluna | Tipo | Obrigatória | Regra ou finalidade |
|---|---|---:|---|
| `id` | UUID | Sim | Chave primária, gerada pela aplicação |
| `nome` | VARCHAR(100) | Sim | Nome do canal; a API exige entre 3 e 100 caracteres |
| `sistema_origem` | VARCHAR | Sim | Sistema que envia os dados |
| `sistema_destino` | VARCHAR | Sim | Sistema que recebe os dados |
| `status` | VARCHAR(20) | Sim | `ativo` ou `inativo` na validação da API |
| `ambiente` | VARCHAR(20) | Sim | `dev`, `staging` ou `prod` na validação da API |
| `criado_em` | TIMESTAMP WITH TIME ZONE | Sim | Data e hora de criação em UTC |

## Representação SQLAlchemy

O modelo persistente está em `integracao-hellow/models/canais_db.py`. Os
schemas de entrada e saída da API estão em `integracao-hellow/models/canais.py`.
Essa separação evita misturar o contrato HTTP com o mapeamento da tabela.

## Validação e restrições

As regras de enumeração de `status` e `ambiente`, assim como o tamanho mínimo
do nome, são aplicadas pelos schemas Pydantic antes da persistência.

A migration atual garante as colunas obrigatórias, os tipos, o tamanho máximo
do nome e a chave primária. Ela ainda não cria constraints SQL para impedir
valores inválidos de `status` ou `ambiente`; essa é uma possível evolução para
reforçar as regras também no banco.

## Migration inicial

A tabela é criada pela migration `0001_create_canais.py`:

```powershell
cd integracao-hellow
uv run --env-file ../.env alembic upgrade head
```

Para verificar a revisão aplicada:

```powershell
uv run --env-file ../.env alembic current
```

## Fluxo de persistência

```text
Requisição HTTP
      ↓
Schema Pydantic
      ↓
Rota
      ↓
Service de canais
      ↓
SQLAlchemy Session
      ↓
PostgreSQL / tabela canais
```

As sessões são abertas pela dependência `get_db`, recebem rollback quando uma
exceção ocorre e são fechadas ao final da requisição.

## Evoluções possíveis

- Criar constraints SQL para `status` e `ambiente`.
- Adicionar índices para filtros e ordenação quando o volume justificar.
- Adicionar `atualizado_em` e auditoria de alterações.
- Modelar sistemas, equipes responsáveis e credenciais em tabelas próprias.
- Definir uma regra de unicidade para impedir canais duplicados.
