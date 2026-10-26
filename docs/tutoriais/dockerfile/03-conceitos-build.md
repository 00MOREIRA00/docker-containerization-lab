# Conceitos de build

O multi-stage build é muito utilizado no mundo corporativo para gerar imagens
menores, mais seguras e com menos ferramentas desnecessárias.

## Builder

O estágio `builder` prepara a aplicação. Ele normalmente:

- instala dependências;
- usa o `uv`;
- cria o `.venv`;
- compila o bytecode;
- pode conter ferramentas de build e arquivos temporários.

Esse estágio existe apenas durante a construção da imagem

## Runtime 

O estágio `runtime` é a imagem que realmente executa a API.

Ele recebe somente:

- ambiente virtual com as dependências de produção;
- código necessário da aplicação;
- arquivos de configuração necessários;
- usuário não-root.

Arquivos `.env` e credenciais não devem ser copiados para a imagem. Eles devem
ser fornecidos em tempo de execução, pelo Compose, pelo ambiente de deploy ou
por um secret manager.

