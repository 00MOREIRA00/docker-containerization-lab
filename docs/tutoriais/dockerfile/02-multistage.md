# Multi-stage build

Nesta etapa, o Dockerfile foi separado em dois estágios: `builder` e
`runtime`. O objetivo é usar ferramentas de instalação e compilação somente
durante o build, mantendo a imagem final focada em executar a API.

## Estágio `builder`

O estágio `builder` usa Python, o `uv` e os arquivos de dependências para:

- Criar o ambiente virtual da aplicação.
- Instalar as dependências de produção.
- Compilar bytecode Python.
- Preparar os arquivos que serão copiados para a imagem final.

Esse estágio não é usado para executar a API em produção.

```dockerfile
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
```

## Estágio `runtime`

O estágio `runtime` começa novamente a partir de uma imagem limpa do Python.
Ele recebe apenas:

- O ambiente virtual pronto.
- Os arquivos necessários para executar a API.
- O código dos módulos da aplicação.

O `uv`, caches e arquivos temporários do build não são copiados para essa
imagem. A aplicação também roda com o usuário não-root `appuser`.

```dockerfile
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/main.py /app/

USER appuser
```

O comando final continua sendo:

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Comparação de tamanho

As imagens foram construídas com o mesmo contexto e as mesmas dependências:

| Imagem | Tamanho |
|---|---:|
| Single-stage | 212.810.938 bytes (aprox. 203,0 MiB) |
| Multi-stage | 188.094.030 bytes (aprox. 179,4 MiB) |
| Diferença | 24.716.908 bytes (aprox. 23,6 MiB) |

A imagem multi-stage ficou aproximadamente 11,6% menor neste projeto.

O ganho pode variar conforme as dependências e os arquivos incluídos na
aplicação. O benefício principal não é apenas o tamanho: o estágio final
também deixa de conter ferramentas de build que não são necessárias em
execução.

## Validação

Para construir a imagem:

```powershell
Set-Location integracao-hellow
docker build -f Dockerfile -t dockerfile-trainer-api:multistage .
```

Para consultar o tamanho:

```powershell
docker image inspect dockerfile-trainer-api:multistage --format '{{.Size}}'
```

Em um pipeline corporativo, o estágio de build normalmente é executado pelo
CI/CD. A imagem final é publicada em um registry e somente o estágio
`runtime` é executado no ambiente de destino.
