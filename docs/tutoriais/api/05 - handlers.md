# Handlers 

Os handlers são funções que interceptam eventos especificos da aplicação e definem como trata-los.

No fastapi, um exception handler serve para capturar exeções e transforma o erro em uma resposta HTTP padronizada.

Sem handler exemplo: 

```
raise HotFoundError("Canal não encontrado")
```

O Fastapi retorna automaticamente algo como:

```
O FastAPI retorna automaticamente algo como:

{
  "detail": "Canal não encontrado"
}
```

Como um handler global, podemos padronizar:

```
{
  "erro": {
    "codigo": 404,
    "mensagem": "Canal não encontrado"
  }
}
```

## Por que usar ? 

Eles são uteis para:

* Centralizar o tratamento de erros 
* Padronizar respostas da API
* Registrar logs
* Evitar repetir try/except em todas as rotas 
* Tratar erros inesperados, validações e problemas de banco 