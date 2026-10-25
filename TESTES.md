# Estratégia de testes da API

## Objetivo

Os testes verificam a lógica da API em duas camadas:

1. Services: validam as operações de negócio e persistência.
2. Handlers: validam a conversão de exceções em respostas HTTP.

## Estrutura

```text
integracao-hellow/tests/
├── test_services.py
└── test_handlers.py
```

## Testes dos services

Os services são testados com um banco SQLite criado em memória para cada caso.
Isso permite validar criação, consulta, atualização e exclusão sem alterar o
PostgreSQL de desenvolvimento.

Os cenários cobertos são:

- Criação e listagem de canais.
- Busca de canal inexistente.
- Atualização de canal.
- Atualização de canal inexistente.
- Exclusão de canal.
- Exclusão de canal inexistente.
- Levantamento de `NotFoundError`.

## Testes dos modelos

Os schemas Pydantic também são testados para garantir que:

- Nomes menores que o limite mínimo sejam rejeitados.
- Status fora do enum permitido sejam rejeitados.

## Testes dos handlers

Os handlers são executados diretamente e suas respostas são verificadas:

- Exceção customizada `HttpAppError`.
- Exceção HTTP do Starlette.
- Mensagem padrão quando a exceção HTTP não possui detalhe.
- Erro de validação `RequestValidationError`.
- Exceção inesperada.

Também é verificado que erros inesperados não expõem detalhes internos ao
consumidor da API.

## Como executar

No PowerShell, a partir da raiz do repositório:

### `unittest`

```powershell
Set-Location integracao-hellow
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

### `pytest`

```powershell
Set-Location integracao-hellow
..\.venv\Scripts\python.exe -m pytest tests -v
```

Os testes não precisam do PostgreSQL, do Docker ou de credenciais externas.

O projeto mantém as duas abordagens: `unittest` para os testes tradicionais e
`pytest` para fixtures, asserções e novos testes de forma mais concisa.

## Próximos testes

Como evolução, podemos adicionar testes de integração HTTP usando um cliente
de testes do FastAPI para validar o fluxo completo:

```text
requisição HTTP → rota → service → banco de teste → resposta HTTP
```
