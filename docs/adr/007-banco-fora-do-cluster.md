# ADR 007 — Manter o banco de dados fora do cluster

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

O cluster [K3s roda em uma única VM](001-kubernetes-deploy.md), cujo armazenamento é
**efêmero**: se a VM for recriada, os volumes locais desaparecem. A aplicação, porém,
precisa de **persistência durável** de pedidos e itens, disponível para as
[2 réplicas](../architecture.md) simultaneamente. É preciso decidir **onde**, em relação à
fronteira do cluster, o estado deve viver.

Este ADR trata da **topologia** (dentro × fora do cluster); a escolha por um serviço
gerenciado está no [ADR 002](002-dbaas-postgresql.md).

## Alternativas consideradas

- **Banco fora do cluster** (DBaaS ou instância dedicada) — o estado tem ciclo de vida
  independente do runtime; recriar a VM/cluster não afeta os dados; conexão via rede.
- **Banco dentro do cluster** (pod com PVC) — tudo em um lugar, latência menor; porém o
  estado fica acoplado ao ciclo de vida de um cluster single-node e efêmero, e o dado morre
  se a VM for recriada.

## Decisão

Manter o banco **fora do cluster**, como serviço acessado pela rede (`DATABASE_URL` injetada
via `db-secret`). O runtime (pods stateless) e o estado (banco durável) têm ciclos de vida
**independentes**. Critério: **separar estado de computação** — o cluster desta arquitetura
é descartável, e estado não pode viver em componente descartável.

## Consequências

**Positivas:**
- O dado sobrevive à recriação da VM, do cluster ou dos pods
- Pods permanecem verdadeiramente **stateless**, o que habilita o scaling horizontal
- Réplicas compartilham o mesmo banco sem conflito de volume
- Alinha-se ao princípio *backing services* do Twelve-Factor App

**Negativas:**
- Latência de rede entre API e banco (maior que um banco local ao pod)
- O banco vira uma dependência externa: exige rede/credenciais corretas e tratamento de
  falha de conexão (o `/health` já reporta `database: unavailable`)
- A performance passa a depender do pool de conexões e da capacidade do banco, não do pod
