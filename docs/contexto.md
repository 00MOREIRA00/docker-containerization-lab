# O problema que o Docker resolve

## O cenário

Imagine que você desenvolveu um pequeno serviço de integração em Python — o **Integração Hello** — uma API simples que vai ser consumida por outros sistemas.

Ela funciona perfeitamente na sua máquina.

Você passa o código para um colega. Ele tenta rodar e quebra.

> *"Mas na minha máquina funciona..."*

---

## Por que quebrou?

Porque o ambiente dele é diferente do seu.

Podem ser coisas sutis:

- Ele tem Python 3.9, você tem Python 3.11
- A versão do `uvicorn` que ele instalou tem um comportamento diferente
- Uma variável de ambiente que você tem no seu sistema e esqueceu de documentar
- Um pacote do sistema operacional que está presente na sua máquina e não na dele

Esse problema se multiplica quando o serviço precisa ir para um servidor de homologação, depois para produção, depois para a máquina de um novo integrante do time.

Cada ambiente vira uma incógnita.

---

## O que o Docker faz

O Docker permite empacotar a aplicação junto com tudo que ela precisa para rodar: a versão exata do Python, as dependências, as configurações de ambiente.

Esse pacote é chamado de **imagem**.

A partir da imagem, você cria **containers** — processos isolados que rodam a aplicação sempre do mesmo jeito, independente de onde estejam.

```
Sua máquina      →  mesma imagem  →  funciona
Máquina do colega →  mesma imagem  →  funciona
Servidor de homolog →  mesma imagem  →  funciona
Produção         →  mesma imagem  →  funciona
```

---

## O que vamos fazer aqui

Ao longo desse repositório, vamos pegar o **Integração Hello** e resolver, passo a passo, cada problema que aparece quando você quer que um serviço rode de forma confiável em qualquer lugar:

| Etapa | O que resolve |
|-------|---------------|
| [Fundamentos do Dockerfile](./tutoriais/dockerfile/00-fundamentos.md) | Como descrever o ambiente da aplicação |
| Build e Run | Como empacotar e rodar localmente |
| Registry e Push | Como compartilhar a imagem com o time |
| Múltiplos ambientes | Como lidar com dev, homolog e produção |
| Docker Compose | Como orquestrar o serviço junto com suas dependências |
| Multi-stage build | Como deixar a imagem mais leve e segura |
| Boas práticas | O que evitar e o que sempre fazer |

O projeto de exemplo é simples de propósito — para que o foco fique nas ferramentas e nos conceitos, não na aplicação em si.
