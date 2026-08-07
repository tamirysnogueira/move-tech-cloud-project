# ADR 009 — Manter um monolito em camadas em vez de microsserviços

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

A aplicação implementa um domínio enxuto (pedidos e itens) mantido por uma equipe pequena.
É preciso decidir o **estilo arquitetural**: concentrar tudo em um único serviço ou já
dividir em serviços independentes desde o início. A escolha afeta complexidade de deploy,
custo, velocidade de desenvolvimento e capacidade de evolução.

## Alternativas consideradas

- **Monolito em camadas** (apresentação → serviço → dados) — um único deployável;
  simplicidade de build, deploy e observabilidade; transações locais; escala na horizontal
  por réplicas. Pode acoplar domínios conforme cresce.
- **Microsserviços desde o início** — serviços com deploy e escala independentes; porém
  adiciona rede entre serviços, consistência distribuída, mais pipelines e mais custo
  operacional — desproporcional a um domínio pequeno e a uma [VM single-node](001-kubernetes-deploy.md).

## Decisão

Manter um **monolito em camadas**, empacotado como **container único** e replicado em
[2 instâncias](../architecture.md) atrás do balanceador. A extração de um segundo serviço
fica **adiada** até que um subdomínio (ex.: **notificações**) tenha cadência de deploy ou
escala próprias que justifiquem a separação. Critério: **simplicidade primeiro** — pagar o
custo da distribuição só quando houver retorno claro.

## Consequências

**Positivas:**
- Build, deploy e observabilidade simples (um artefato, um pipeline, um `/metrics`)
- Menor custo: um deployável na mesma VM, sem malha de serviços
- Refatoração interna barata enquanto tudo compartilha o mesmo processo
- Adequado ao tamanho atual do domínio e da equipe

**Negativas:**
- Todo o código escala e é implantado junto — não há escala/deploy por subdomínio
- Risco de acoplamento entre camadas com o tempo (as regras hoje vivem em `app/main.py`,
  ver [ADR 005](005-fastapi-framework.md)) — mitiga-se mantendo fronteiras internas limpas
- Uma falha grave afeta todo o serviço (raio de explosão maior que em microsserviços)

## Estilo-alvo

Caso o domínio de notificações cresça, o próximo passo é **extrair um segundo serviço**,
evoluindo para uma arquitetura orientada a serviços — sem reescrever o núcleo de pedidos.
Manter a camada de serviço bem definida hoje reduz o custo dessa extração amanhã.
