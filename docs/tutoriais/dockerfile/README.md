# Tutoriais de Dockerfile

Esta trilha explica como construir, executar e otimizar a imagem da API.

## Ordem recomendada

1. [Fundamentos do Dockerfile](00-fundamentos.md)
2. [Dockerfile inicial](01-dockerfile.md)
3. [Multi-stage build](02-multistage.md)
4. [Conceitos de build](03-conceitos-build.md)

## Conceitos abordados

- Imagem base Python slim.
- Instalação reprodutível com `uv.lock`.
- Separação entre dependências de build e runtime.
- Execução da aplicação com usuário não-root.
- Comparação do tamanho das imagens.

Para a execução com diferentes configurações, consulte também a trilha de
[ambientes](../ambiente/README.md).
