# Dockerfile

O Multi-stage build é muito utilizado no mundo corporativo, focando em gerar imagens menores. mais seguras e com menos ferramentas desnecessárias. 

## Builder

O estágio de `builder` prepara a aplicação. Ele basicamente: 
* Intala dependencias 
* Usa o uv
* Cria o .venv
* Compila o bytecode
* Pode conter ferramentas de build e arquivos temporarios

Esse estágio existe apenas durante a construção da imagem

## Runtime 

O estágio runtime é a iamgem que realmente executa a API: 

Ele recebe somente:

* .env
* Código necessário da apicação
* Arquivos de configuração necessários 
* Usuário não root

