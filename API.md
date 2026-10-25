# API

## Estado atual

A API já possui:

- CRUD de canais.
- Versionamento inicial em `/canais/v1`.
- Migrations com Alembic.
- Persistência em PostgreSQL.
- Camada de services para concentrar a lógica.
- Exceções HTTP customizadas.
- Handlers para erros HTTP, validação e falhas inesperadas.
- Timeouts de conexão, pool, consultas SQL e locks.

## Próximas evoluções

### 1. Testes automatizados

- Testar cada endpoint.
- Testar os services isoladamente.
- Testar exceções e handlers.
- Testar erros de validação e banco.

### 2. Tratamento específico de erros de banco

Atualmente, erros como `IntegrityError` e `OperationalError` podem cair no
handler genérico `500`. O ideal é mapeá-los para respostas mais específicas:

```text
IntegrityError    -> 409 Conflict
OperationalError  -> 503 Service Unavailable
TimeoutError      -> 504 Gateway Timeout
```

### 3. Paginação e filtros

A listagem atualmente retorna todos os canais. Podemos adicionar:

```http
GET /canais/v1/?page=1&limit=20
GET /canais/v1/?status=ativo
GET /canais/v1/?ambiente=prod
```

### 4. Regras de negócio

Possíveis regras:

- Impedir origem e destino iguais.
- Impedir canais duplicados.
- Validar transições de status.
- Verificar se os sistemas existem antes de criar o canal.

### 5. Autenticação e autorização

Atualmente, não há controle de acesso definido. Poderão ser adicionados:

- Login ou integração com um provedor de identidade.
- JWT ou API key.
- Controle de permissões.
- Proteção das operações de criação, alteração e exclusão.

### 6. Health checks

Adicionar endpoints como:

```http
GET /health
GET /ready
```

O endpoint `/ready` pode verificar se o PostgreSQL está acessível.

### 7. Observabilidade

- Logs estruturados.
- Request ID.
- Tempo de execução das requisições.
- Logs de erros de banco.
- Métricas, quando necessário.

### 8. Documentação da API

Melhorar a documentação OpenAPI com:

- Descrição dos endpoints.
- Exemplos de requisições e respostas.
- Documentação dos erros.
- Tags e códigos HTTP possíveis.

### 9. Segurança e limites

- Configuração de CORS.
- Rate limiting.
- Limite de tamanho de payload.
- Validação das entradas.
- Não exposição de detalhes internos nos erros.

## Ordem sugerida

```text
1. Testes
2. Tratamento específico de erros de banco
3. Paginação e filtros
4. Regras de negócio
5. Health checks
6. Autenticação
7. Observabilidade e hardening
```
