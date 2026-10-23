# Melhorias identificadas

## Problemas críticos

### 1. Nome da pasta com hífen quebra o import Python
- **Arquivo:** `integracao-hellow/`
- **Problema:** Python não consegue importar módulos com hífen no nome. O `CMD` do `dockerfile` referencia `integracao-hellow.main:app`, o que causa erro em runtime.
- **Correção:** Renomear para `integracao_hellow/` e atualizar o `CMD` no Dockerfile.

### 2. Encoding corrompido no requirements.txt
- **Arquivo:** `requirements.txt`
- **Problema:** Arquivo salvo em UTF-16 com BOM. Pode quebrar o `pip install` durante a build da imagem.
- **Correção:** Recriar o arquivo em UTF-8.

## Problemas de convenção

### 3. Nome do Dockerfile fora do padrão
- **Arquivo:** `dockerfile`
- **Problema:** A convenção Docker exige o nome `Dockerfile` com D maiúsculo. Ferramentas como `docker build` e pipelines de CI podem não reconhecer o arquivo com letra minúscula.
- **Correção:** Renomear para `Dockerfile`.

## Melhorias de qualidade

### 4. README vazio
- **Arquivo:** `README.md`
- **Problema:** Contém apenas o título do repositório, sem nenhuma informação útil.
- **Correção:** Adicionar descrição do propósito do repositório, como ele está organizado e como navegar pelo conteúdo.

### 5. Typos na documentação
- **Arquivo:** `docs/01-geral.md`
- **Problema:** Dois erros de digitação no texto introdutório.
  - "paa contruir" → "para construir"
  - "desceve" → "descreve"
- **Correção:** Corrigir os dois trechos.

---

## Conteúdo faltando (escopo do cheatsheet)

O objetivo do repositório é ser um guia completo sobre criação e uso de imagens Docker. Os tópicos abaixo ainda não foram cobertos:

### Documentação
- [ ] Por que criar uma imagem Docker? (motivação, problemas que resolve)
- [ ] Como fazer o build de uma imagem (`docker build`)
- [ ] Como rodar um container localmente (`docker run`)
- [ ] Como publicar a imagem em um registry (Docker Hub, ECR, GCR)
- [ ] Como fazer o deploy da imagem (docker run em servidor, Docker Compose, Kubernetes básico)
- [ ] Múltiplos ambientes: variáveis de ambiente, arquivos `.env`, `ARG` vs `ENV`
- [ ] Docker Compose para orquestração local
- [ ] Multi-stage build para imagens mais leves
- [ ] Boas práticas de segurança (usuário não-root, imagens mínimas, secrets)

### Exemplos práticos
- [ ] Exemplo de `docker-compose.yml` com múltiplos serviços
- [ ] Exemplo de Dockerfile com multi-stage build
- [ ] Exemplo de Dockerfile para diferentes ambientes (dev vs prod)
- [ ] Exemplo de pipeline CI/CD fazendo build e push da imagem

---

## Evolução da aplicação de exemplo (`integracao-hellow`)

A aplicação atual é um endpoint simples sem dependências externas, o que a torna pouco representativa de um cenário real. A proposta é evoluí-la para que sirva como exemplo concreto ao longo de todo o cheatsheet.

### Objetivo

Ter uma aplicação que:
- Se conecta a um banco de dados PostgreSQL
- Tem configurações separadas por ambiente (dev, staging, prod)
- Separa configurações não-sensíveis (TOML) de secrets (variáveis de ambiente)
- Serve de base para demonstrar build, push, deploy e múltiplos ambientes

### Estrutura proposta

```
integracao-hellow/
├── app/
│   ├── main.py            # entrypoint FastAPI
│   ├── database.py        # conexão com o banco via config + secret
│   ├── settings.py        # lê o .toml do ambiente + env vars para secrets
│   └── routers/
│       └── items.py       # endpoint simples que lê/escreve no banco
├── config/
│   ├── dev.toml
│   ├── staging.toml
│   └── prod.toml
├── .env.example           # template dos secrets (nunca commitar o .env real)
├── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.staging.yml
└── docker-compose.prod.yml
```

### Separação de configuração e secrets

Cada arquivo `.toml` carrega as configurações não-sensíveis do ambiente:

```toml
# config/dev.toml
[app]
debug = true
log_level = "DEBUG"

[database]
host = "db"
port = 5432
name = "integracao_dev"
```

Os secrets (senha do banco, chaves de API) chegam exclusivamente via variável de ambiente — nunca versionados no repositório:

```
# .env.example
APP_ENV=dev
DB_PASSWORD=
```

O `settings.py` é responsável por carregar o `.toml` correto com base na variável `APP_ENV` e combinar com os secrets vindos do ambiente.

### O que cada Docker Compose representa

| Arquivo | Ambiente | Banco | Debug |
|---------|----------|-------|-------|
| `docker-compose.dev.yml` | Desenvolvimento local | `integracao_dev` | ativado |
| `docker-compose.staging.yml` | Homologação | `integracao_staging` | desativado |
| `docker-compose.prod.yml` | Produção | `integracao_prod` | desativado |

Cada compose sobe a aplicação + o banco PostgreSQL correspondente, injetando as variáveis de ambiente corretas sem alterar a imagem — a mesma imagem é deployada em todos os ambientes.
