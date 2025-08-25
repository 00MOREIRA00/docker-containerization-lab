# Introdução ao Dockerfile

O Dockerfile é um arquivo que contém um conjunto de instruções usadas pelo Docker paa contruir imagens.

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