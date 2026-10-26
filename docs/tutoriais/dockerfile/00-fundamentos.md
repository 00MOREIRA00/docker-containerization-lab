# Introdução ao Dockerfile

O Dockerfile é um arquivo que contém um conjunto de instruções usadas pelo Docker para construir imagens.

Ele funciona como uma "receita", em que cada instrução descreve uma etapa necessária para configurar o ambiente da aplicação dentro de um container.

Com ele, conseguimos:

- Automatizar a criação de ambientes padronizados.

- Garantir que o código rode da mesma forma em diferentes máquinas.

- Reduzir erros de configuração manual.

- Facilitar deploys e integrações contínuas.

## Estrutura básica de um Dockerfile

Um Dockerfile é composto por instruções, como `FROM`, `COPY`, `RUN` e `CMD`, que são executadas em sequência.
Cada instrução cria uma nova camada na imagem.

Exemplo simples:

```Dockerfile
FROM python:3.11-slim        # Define a imagem base
WORKDIR /app                 # Define diretório de trabalho
COPY requirements.txt .      # Copia dependências
RUN pip install -r requirements.txt  # Instala dependências
COPY . .                     # Copia o código
CMD ["python", "app.py"]     # Comando que roda por padrão
```

## Principais instruções

- `FROM` → escolhe a imagem base.

- `WORKDIR` → define o diretório de trabalho.

- `COPY` → copia arquivos para o container.

- `RUN` → executa comandos durante o build.

- `CMD` → comando padrão quando o container inicia.

- `EXPOSE` → documenta a porta usada pela aplicação.

- `ENV` → define variáveis de ambiente.

## Boas práticas iniciais

- Usar versões específicas de imagens (`python:3.11-slim` em vez de `python:latest`).

- Usar `.dockerignore` para não copiar arquivos desnecessários, como `__pycache__/` e `.git/`.

- Reduzir o número de camadas quando fizer sentido.

- Avaliar multi-stage builds para imagens mais enxutas.

## Build

Build é o processo de criar uma imagem a partir do Dockerfile. Ao executar
`docker build`, o Docker processa cada instrução, camada por camada, até gerar
uma imagem pronta para execução.

## O que é uma Imagem 

Uma imagem é um snapshot imutável e versionável do ambiente da aplicação. Ela
funciona como um molde a partir do qual vários containers podem ser criados.


Dockerfile -> docker build -> Imagem -> docker run -> Container

A imagem fica salva localmente (ou num registry como Docker Hub). O container é a imagem rodando como processo.

## O que vai na imagem ?

Tudo que a aplicação precisa para existir:

- O sistema operacional base, como `python:3.11-slim`.
- As dependências instaladas, como FastAPI e Uvicorn.
- O código-fonte da aplicação.
- As instruções de inicialização, como `CMD`.

Variáveis de ambiente não vão na imagem — e isso é intencional.

A imagem deve ser a mesma para dev, staging e produção. O que muda entre os
ambientes são os valores de configuração, injetados em runtime:

docker run -e DATABASE_URL=postgres://... -e ENV=prod minha-imagem

Ou via Docker Compose com um arquivo `.env`.

Se você colocasse segredos na imagem, qualquer pessoa que baixasse a imagem teria acesso a eles — um problema sério de segurança.

Resumindo:

┌───────────────────────────┬─────────────────────────────────┐
│          O que é          │         Vai na imagem?          │
├───────────────────────────┼─────────────────────────────────┤
│ Código-fonte              │ ✅ sim                          │
├───────────────────────────┼─────────────────────────────────┤
│ Dependências              │ ✅ sim                          │
├───────────────────────────┼─────────────────────────────────┤
│ Variáveis de ambiente     │ ❌ não — injetadas no container │
├───────────────────────────┼─────────────────────────────────┤
│ Segredos (senhas, tokens) │ ❌ jamais                       │
├───────────────────────────┼─────────────────────────────────┤
│ Dados do banco            │ ❌ não — ficam em volumes       │
└───────────────────────────┴─────────────────────────────────┘
