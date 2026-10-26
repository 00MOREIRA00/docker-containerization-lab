# API de canais

## Popular o banco local

Com o PostgreSQL iniciado pelo Compose e as migrations aplicadas, execute
nesta pasta:

```powershell
uv run --env-file ../.env python -m scripts.seed_dev
```

O seed adiciona seis canais fictícios, com status ativo e inativo e ambientes
`dev`, `staging` e `prod`. O campo ambiente é apenas um dado do exemplo;
todos os registros são inseridos no mesmo banco configurado no `.env`.

Os IDs dos exemplos são fixos. Executar novamente não duplica os exemplos
nem sobrescreve registros existentes. Se um exemplo for excluído, uma nova
execução o recria. A inserção ocorre em uma única transação e não cria tabelas;
execute `uv run --env-file ../.env alembic upgrade head` antes, se necessário.

Confira os dados no DBeaver:

```sql
SELECT * FROM public.canais ORDER BY criado_em, id;
```
