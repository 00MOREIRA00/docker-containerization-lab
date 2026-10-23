# Introdução ao Dockerfile

O Dockerfile é um arquivo que contém um conjunto de instruções usadas pelo Docker para contruir imagens.

Ele funciona como uma "receita" onde cada uma delas desceve uma etapa necessária para configurar o ambiente da aplicação dentro de um container. 

Com ele, conseguimos:

* Automatizar a criação de ambientes padronizados

* Garantir que o código rode da mesma forma em diferentes máquinas

* Reduzir erros de configuração manual

* Facilitar deploys e integrações contínuas

## Estrutura básica de um Dockerfile

Um Dockerfile é composto por instruções (keywords como FROM, COPY, RUN, CMD), que são executadas em sequência.
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

* `FROM` → escolhe a imagem base

* `WORKDIR` → define o diretório de trabalho

* `COPY` → copia arquivos para o container

* `RUN` → executa comandos durante a build

* `CMD` → comando padrão quando o container inicia

* `EXPOSE` → documenta a porta usada pela aplicação

* `ENV` → define variáveis de ambiente

## Boas práticas iniciais

Sempre usar versões específicas de imagens (python:3.11-slim em vez de python:latest)

Usar .dockerignore para não copiar arquivos desnecessários (ex: __pycache__/, .git/)

Reduzir número de camadas unindo comandos (RUN apt-get update && apt-get install ...)

Avaliar multi-stage builds para imagens mais enxutas

## Build 

Buildar é o processo de criar uma imagem a partir do Dockerfile. Rodamos o docker build e Docker executa cada instrução do arquivo, camada por camada, até gerar um pacote fechado e pronto para rodar em qualquer lugar

## O que é uma Imagem 

É um snapshot do ambiente da aplicação - imutável, versionado, portável. Pensa como um "molde": a partir dele você cria quantos containers quiser, todos identicos.


Dockerfile -> docker build -> Imagem -> docker run -> Container

A imagem fica salva localmente (ou num registry como Docker Hub). O container é a imagem rodando como processo.

## O que vai na imagem ?

Tudo que a aplicação pecisar para existir: 
Tudo que a aplicação precisa para existir:

- O sistema operacional base (ex: python:3.11-slim)
- As dependências instaladas (fastapi, uvicorn, etc.)
- O código-fonte da aplicação
- Configurações de como iniciar (CMD)

Variáveis de ambiente não vão na imagem — e isso é intencional.

A imagem é a mesma para dev, staging e prod. O que muda entre ambientes são os valores de configuração: URL do banco, chaves de API, nível de log. Esses valores são injetados em runtime, na hora de criar o container:

docker run -e DATABASE_URL=postgres://... -e ENV=prod minha-imagem

Ou via docker-compose.yml com um arquivo .env.

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