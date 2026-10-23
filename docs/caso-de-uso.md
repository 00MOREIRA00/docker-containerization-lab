# Caso de uso — Integração Hello

## Contexto

Uma empresa opera múltiplos sistemas internos: ERP, CRM, plataforma de e-commerce e ferramentas de analytics. Com o crescimento, o número de integrações entre esses sistemas aumentou e passou a ser difícil responder perguntas simples:

- Quais sistemas estão se comunicando entre si?
- Essa integração está ativa em produção ou só em homologação?
- Quem é a origem e quem é o destino de cada fluxo de dados?

O **Integração Hello** nasce como o microserviço responsável por centralizar esse catálogo.

---

## O que o serviço faz

Gerencia **Canais** — os registros de comunicação entre dois sistemas.

Cada Canal representa uma integração entre um sistema de origem e um sistema de destino, com seu status e o ambiente onde está operando.

---

## Entidade: Canal

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `nome` | string | Nome descritivo do canal |
| `sistema_origem` | string | Sistema que envia os dados |
| `sistema_destino` | string | Sistema que recebe os dados |
| `status` | enum | `ativo` ou `inativo` |
| `ambiente` | enum | `dev`, `staging` ou `prod` |
| `criado_em` | datetime | Data de criação do registro |

### Exemplo de registro

```json
{
  "id": "a3f1c2d4-...",
  "nome": "Pedidos para ERP",
  "sistema_origem": "e-commerce",
  "sistema_destino": "erp",
  "status": "ativo",
  "ambiente": "prod",
  "criado_em": "2024-01-15T10:30:00Z"
}
```

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/canais` | Registrar um novo canal |
| `GET` | `/canais` | Listar todos os canais |
| `GET` | `/canais/{id}` | Detalhar um canal |
| `PUT` | `/canais/{id}` | Atualizar dados ou status |
| `DELETE` | `/canais/{id}` | Remover um canal |

---

## Por que isso justifica múltiplos ambientes

O catálogo de canais muda conforme o ambiente:

- Em **dev**, os canais apontam para sistemas mockados ou locais
- Em **staging**, os canais replicam o cenário de produção para testes
- Em **prod**, os canais são os fluxos reais entre sistemas da empresa

A aplicação é a mesma. A imagem Docker é a mesma. O que muda é o banco de dados e as configurações de cada ambiente — exatamente o que esse cheatsheet vai demonstrar.
