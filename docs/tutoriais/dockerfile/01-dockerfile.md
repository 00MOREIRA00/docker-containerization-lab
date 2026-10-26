# Dockerfile inicial com uv

Vamos criar o Dockerfile para a criação da imagem da aplicação. 

## Primeira Versão

```dockerfile
FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

1. Primeiramente selecionamos uma imagem base para criação da nossa imagem. Dessa forma temos uma imagem python 3.11 slim como base.

```
FROM python:3.11-slim
```

2. Copia o executável uv de outra imagem para esta. O uv é a ferramenta que vai gerenciar as dependências e executar a aplicação. 

```
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
```

3. Define /app como o diretório de trabalho dentro do container. Os próximos comandos trabalham a partir dele. 

```
WORKDIR /app
```

4. Copia os arquivos que descrevem as dependências.

```
COPY pyproject.toml uv.lock ./
```

- pyproject.toml: configurações do projeto e dependências declaradas.

- uv.lock: versões exatas das dependências resolvidas.

5. Instala as dependências durante a construção da imagem.

```
RUN uv sync --frozen --no-dev
```

- uv sync: prepara o ambiente virtual, normalmente em /app/.venv, e instala as dependências.

- --frozen: usa o lockfile existente sem atualizá-lo.

- --no-dev: exclui as dependências do grupo de desenvolvimento.

6. Copia o projeto

```
COPY . .
```

7. Define o comando executado ao iniciar o container.

```dockerfile
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

- `uv run`: executa o comando no ambiente do projeto.
- `uvicorn main:app`: inicia o servidor usando o objeto `app` do arquivo `main.py`.
- `--host 0.0.0.0`: faz o servidor aceitar conexões pelas interfaces de rede do container.
- `--port 8001`: define a porta em que a aplicação escuta dentro do container.

## Construir a imagem

Com o Docker em execução, entre na pasta da aplicação a partir da raiz do repositório:

```powershell
cd integracao-hellow
docker build -t integracao-hellow:0.1 .
```

O `-t` define o nome da imagem (`integracao-hellow`) e sua tag (`0.1`). O ponto final usa a pasta atual como contexto do build, incluindo o `Dockerfile`, o `pyproject.toml`, o `uv.lock` e o código da API.

## Executar o container

```powershell
docker run --rm -p 8000:8001 integracao-hellow:0.1
```

O terminal permanece mostrando os logs. Aguarde a mensagem de inicialização do Uvicorn antes de chamar a API.

O `-p` segue o formato `PORTA_DO_COMPUTADOR:PORTA_DO_CONTAINER`:

- `8000`: porta do computador, usada no Postman e no navegador.
- `8001`: porta dentro do container, onde o Uvicorn está escutando.

```text
Postman → localhost:8000 → Docker → container:8001 → aplicação
```

O `--rm` remove automaticamente o container quando ele para. A imagem continua disponível. Para encerrar essa execução, pressione `Ctrl+C` no terminal.

## Testar a API no Postman

### Listar canais

Crie uma requisição com o método `GET` e a URL:

```text
http://localhost:8000/canais/v1/
```

Clique em **Send**. Sem canais cadastrados, a resposta esperada é **200 OK** com o corpo `[]`.

### Criar um canal

Use o método `POST` na mesma URL. Em **Body → raw → JSON**, informe:

```json
{
  "nome": "Canal de pedidos",
  "sistema_origem": "loja",
  "sistema_destino": "erp",
  "status": "ativo",
  "ambiente": "dev"
}
```

Clique em **Send**. A resposta esperada é **201 Created**, com os dados enviados e os campos `id` e `criado_em`. Repita o `GET` para consultar o canal criado.

Os canais são persistidos no PostgreSQL. Para preparar o banco, aplique as
migrations com Alembic conforme a documentação de [banco de dados](../api/03%20-%20bd.md).

A documentação interativa também está disponível em [http://localhost:8000/docs](http://localhost:8000/docs).

## Se aparecer connection refused

Confira se o container está rodando e se a porta foi publicada corretamente:

```powershell
docker ps
```

A coluna `PORTS` deve mostrar o mapeamento `8000->8001/tcp`. Consulte os logs usando o nome ou ID exibido pelo comando:

```powershell
docker logs NOME_OU_ID_DO_CONTAINER
```

Substitua `NOME_OU_ID_DO_CONTAINER` pelo valor correspondente. Os logs devem indicar que o Uvicorn iniciou na porta `8001`.

O mapeamento `-p 8000:8000` encaminha as requisições para uma porta em que esta aplicação não escuta. Nesse caso, pare o container e crie outro com `-p 8000:8001`.
