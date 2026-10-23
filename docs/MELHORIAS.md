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
- **Correção:** Adicionar descrição do projeto, instruções de uso e como rodar com Docker.

### 5. Typos na documentação
- **Arquivo:** `docs/01-geral.md`
- **Problema:** Dois erros de digitação no texto introdutório.
  - "paa contruir" → "para construir"
  - "desceve" → "descreve"
- **Correção:** Corrigir os dois trechos.
