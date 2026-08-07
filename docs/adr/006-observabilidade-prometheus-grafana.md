# ADR 006 — Observabilidade com Prometheus, Grafana e logs estruturados

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

Os requisitos não-funcionais da solução (disponibilidade de 99,5%, P95 < 500 ms, 300 req/s
— ver [architecture.md](../architecture.md)) só podem ser afirmados se forem **medidos**.
Sem métricas e logs, uma degradação só é percebida pelo usuário final. A aplicação
precisava expor sinais de saúde e desempenho de forma padronizada e consumível pelo
ecossistema Kubernetes.

## Alternativas consideradas

- **Prometheus + Grafana (padrão Kubernetes)** — Prometheus faz *scrape* de um endpoint
  `/metrics`, Grafana exibe dashboards; integração nativa via `ServiceMonitor`
  (kube-prometheus-stack); open source e sem lock-in.
- **Apenas logs (sem métricas)** — simples, mas não responde "qual o P95?" nem alimenta
  alertas por SLO; insuficiente para os requisitos não-funcionais.
- **APM SaaS (Datadog, New Relic)** — muito completo (traces, métricas, logs num só lugar);
  custo recorrente e dependência de fornecedor externo, desproporcional ao escopo.

## Decisão

Instrumentar a API com **`prometheus-fastapi-instrumentator`**, expondo `/metrics` no
formato Prometheus, e coletar via **`ServiceMonitor`** (`servicemonitor.yaml`, scrape a cada
30s) para o **Prometheus** in-cluster, com dashboards no **Grafana**. Os logs da aplicação
são **estruturados em JSON** (`JsonFormatter` em `app/main.py`). Critério: medir os
requisitos não-funcionais com ferramentas open source nativas do Kubernetes, sem custo de
SaaS.

## Consequências

**Positivas:**
- Latência (P95 via `histogram_quantile`), throughput e taxa de erros mensuráveis
- Integração nativa com Kubernetes via `ServiceMonitor` (scrape automático de novas
  réplicas)
- Logs em JSON prontos para indexação e busca por campo
- Base pronta para alertas por SLO e para o Horizontal Pod Autoscaler (métricas de carga)

**Negativas:**
- Prometheus e Grafana consomem recursos na mesma VM (2 vCPU / 2 GB) — competem com a API
- Sem *tracing* distribuído ainda (só métricas e logs); correlação entre requisições é
  limitada
- Armazenamento de métricas é local/efêmero: a série histórica se perde se a VM for
  recriada (ver [ADR 001](001-kubernetes-deploy.md))
