# 🛒 Move Tech Cloud Project — Micro E-commerce API

> API REST de micro e-commerce para gestão de pedidos e itens, empacotada com Docker, orquestrada com Kubernetes (K3s) e publicada na **Magalu Cloud** com deploy contínuo via **GitHub Actions**.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white">
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes%20(K3s)-326CE5?logo=kubernetes&logoColor=white">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white">
  <img alt="Magalu Cloud" src="https://img.shields.io/badge/Cloud-Magalu%20Cloud-0086FF">
  <img alt="Status" src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow">
</p>

> ℹ️ **Projeto em evolução.** Este repositório é desenvolvido ao longo das competências do curso **Move Tech** (Magalu × Prósper Digital Skills). Novas funcionalidades, infraestrutura e documentação são adicionadas a cada etapa — veja o [Roadmap](#-roadmap-por-competência).

---

## 📖 Sobre o projeto

Aplicação de referência de uma **API de micro e-commerce** que gerencia pedidos e seus itens. O foco do projeto não é apenas a API em si, mas a jornada completa de **levar uma aplicação local até a nuvem**, aplicando práticas reais de DevOps: conteinerização, registro de imagens, orquestração com Kubernetes e automação de deploy com CI/CD.

Ao final da trilha, a aplicação está:

- 📦 Empacotada em uma imagem **Docker**
- 🗄️ Publicada no **Container Registry da Magalu Cloud**
- ☸️ Rodando no **Kubernetes (K3s)** da Magalu Cloud com alta disponibilidade (2 réplicas)
- 🐘 Persistindo dados em **PostgreSQL gerenciado (DBaaS)**
- 🚀 Com **deploy automático** disparado pelo GitHub Actions
- 📊 **Observável** com métricas Prometheus + Grafana e logs estruturados em JSON
- 📈 **Escalável automaticamente** com Horizontal Pod Autoscaler (HPA)
- 🧪 Validada por **testes de carga (k6)** contra SLOs de latência e erro
- 📐 **Documentada** com diagrama de arquitetura e ADRs (Competência 6)

---

## 🧰 Stack de tecnologias

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3.11 |
| Framework web | FastAPI |
| ORM | SQLAlchemy |
| Gerenciador de dependências | Poetry |
| Testes | Pytest |
| Conteinerização | Docker / Docker Compose |
| Orquestração | Kubernetes (K3s) |
| Banco de dados | PostgreSQL gerenciado (DBaaS) · SQLite (local) |
| Registro de imagens | Magalu Cloud Container Registry |
| CI/CD | GitHub Actions |
| Observabilidade | Logs estruturados em JSON · métricas Prometheus · dashboards Grafana |
| Escalabilidade | Horizontal Pod Autoscaler (HPA) |
| Teste de carga | k6 |
| Documentação de arquitetura | Diagrama C4/Mermaid · ADRs |

---

## 🚀 Endpoints da API

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/health` | Verifica se a API está no ar |
| `GET` | `/stats` | Estatísticas gerais da aplicação |
| `GET` | `/metrics` | Métricas no formato Prometheus |
| `POST` | `/orders` | Cria um novo pedido |
| `GET` | `/orders` | Lista todos os pedidos |
| `GET` | `/orders/{id}` | Retorna um pedido com seus itens |
| `DELETE` | `/orders/{id}` | Cancela um pedido |
| `POST` | `/orders/{id}/items` | Adiciona um item ao pedido |
| `GET` | `/orders/{id}/items` | Lista os itens de um pedido |

📚 Documentação interativa (Scalar, sobre o schema OpenAPI) disponível em `/docs`.

---

## 🗂️ Estrutura do repositório

```
move-tech-cloud-project/
├── app/                      # Código da aplicação (FastAPI + SQLAlchemy)
├── tests/                    # Testes automatizados (Pytest)
├── docs/
│   ├── architecture.md       # Diagrama C2, componentes, NFRs, trade-offs, melhorias
│   └── adr/                  # Architecture Decision Records (001–009)
├── k8s/
│   ├── app.yaml              # Deployment (2 réplicas + resources) e Service
│   ├── hpa.yaml              # Horizontal Pod Autoscaler (min 2, max 6, CPU 70%)
│   └── servicemonitor.yaml   # Scrape do /metrics pelo Prometheus (observabilidade)
├── load/
│   └── k6/
│       └── load-test.js      # Teste de carga (k6) — SLO P95 < 500 ms e erro < 1%
├── .github/
│   └── workflows/
│       ├── deploy.yaml       # Pipeline de CI/CD (GitHub Actions)
│       └── load-test.yaml    # Teste de carga sob demanda (k6)
├── run-load-test.sh          # Roda o teste de carga localmente (k6 nativo ou Docker)
├── Dockerfile                # Receita da imagem Docker
├── docker-compose.yml        # Execução local
├── pyproject.toml            # Dependências e configuração do projeto
└── README.md
```

> 📐 **Arquitetura:** o desenho da solução, os requisitos não-funcionais, os trade-offs e as
> decisões técnicas (ADRs) estão documentados em [`docs/architecture.md`](docs/architecture.md)
> e [`docs/adr/`](docs/adr/README.md).

---

## 💻 Como rodar localmente

**Pré-requisito:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) ou [Docker Engine](https://docs.docker.com/engine/install/) (Linux).

```bash
# Clone o repositório
git clone https://github.com/tamirysnogueira/move-tech-cloud-project.git
cd move-tech-cloud-project

# Suba a aplicação
docker compose up --build
```

Acesse:

- API: <http://localhost:8000>
- Documentação interativa: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/health>

> 💡 Sem a variável `DATABASE_URL` configurada, a aplicação usa **SQLite** como banco local. A persistência em PostgreSQL gerenciado é adicionada na Competência 4.

---

## ✅ Testes e cobertura

A suíte roda com **cobertura habilitada por padrão** (configurada no `pyproject.toml`): o percentual aparece na tela ao final e o comando **falha automaticamente se a cobertura ficar abaixo de 90%** (`--cov-fail-under=90`).

```bash
poetry run pytest
```

Saída ao final da execução:

```text
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/database.py      13      0   100%
app/main.py          88      0   100%
app/models.py        20      0   100%
-----------------------------------------------
TOTAL               121      0   100%
Required test coverage of 90% reached. Total coverage: 100.00%
```

No CI, o mesmo comando roda no job `test` do pipeline e o resumo da cobertura é publicado no **Step Summary** do GitHub Actions. Como o `build-and-deploy` depende do `test` (`needs: test`), **nenhum deploy acontece com a cobertura abaixo do mínimo**.

---

## ☁️ Deploy na Magalu Cloud

O deploy é totalmente automatizado pelo pipeline do GitHub Actions, que executa duas etapas em sequência:

1. **`test`** — instala as dependências e roda os testes automatizados (Pytest).
2. **`build-and-deploy`** (apenas se os testes passarem):
   - Faz login no Container Registry da Magalu Cloud
   - Constrói a imagem Docker e publica no registry
   - Configura o acesso ao cluster via `kubeconfig`
   - Cria/atualiza o `db-secret` com a `DATABASE_URL` do PostgreSQL gerenciado
   - Aplica os manifests (`k8s/app.yaml` + `k8s/hpa.yaml`) e aguarda o rollout concluir

### Secrets necessários

Configurados em **Settings → Secrets and variables → Actions**:

| Secret | Descrição |
| --- | --- |
| `MGC_REGISTRY_USER` | Usuário do Container Registry |
| `MGC_REGISTRY_PASSWORD` | Senha do Container Registry |
| `MGC_REGISTRY_NAME` | Nome do registry na Magalu Cloud |
| `MGC_KUBECONFIG` | Conteúdo do arquivo `kubeconfig` do cluster |
| `DATABASE_URL` | String de conexão do PostgreSQL gerenciado (DBaaS) |

### Verificação

Após o deploy, o serviço fica acessível pelo IP público do cluster:

```bash
kubectl get svc cloud-project   # coluna EXTERNAL-IP
kubectl get hpa cloud-project   # réplicas atuais x alvo de CPU
```

- Health check: `http://<IP-DA-VM>/health` → `{"status": "ok", "database": "ok"}`
- Documentação: `http://<IP-DA-VM>/docs`
- Métricas: `http://<IP-DA-VM>/metrics`

---

## 📊 Observabilidade

A aplicação expõe sinais de saúde e desempenho de forma padronizada para o ecossistema Kubernetes:

- **Métricas** no formato Prometheus em `/metrics`, instrumentadas com `prometheus-fastapi-instrumentator`.
- **Coleta** via `ServiceMonitor` ([`k8s/servicemonitor.yaml`](k8s/servicemonitor.yaml)), que faz *scrape* a cada 30s para o **Prometheus** in-cluster.
- **Dashboards** no **Grafana** (latência P95, throughput, taxa de erros).
- **Logs estruturados em JSON** (`JsonFormatter`), prontos para indexação e busca por campo.

Consulte o [ADR 006](docs/adr/006-observabilidade-prometheus-grafana.md) para o racional da escolha.

---

## 📈 Escalabilidade e autoscaling

A aplicação é **stateless**, então escala na horizontal atrás do balanceador. O escalonamento é automático via **Horizontal Pod Autoscaler** ([`k8s/hpa.yaml`](k8s/hpa.yaml)):

| Parâmetro | Valor |
| --- | --- |
| Réplicas mínimas | 2 |
| Réplicas máximas | 6 |
| Métrica-alvo | CPU 70% da `request` |

O HPA usa as `resources.requests`/`limits` declaradas no Deployment (100m–500m CPU · 128–256Mi) como base de cálculo e depende do `metrics-server` (incluso no K3s).

---

## 🧪 Teste de carga

Um teste de carga com **k6** valida os requisitos não-funcionais (P95 < 500 ms e taxa de erro < 1%):

**No GitHub Actions** — workflow **Teste de carga (k6)** (`workflow_dispatch`). Os parâmetros de tuning são **inputs do formulário** (visíveis e ajustáveis a cada execução), e a **URL alvo é descoberta automaticamente** no cluster — o job lê o `EXTERNAL-IP` do Service com o `kubeconfig` (único segredo envolvido), sem IP hardcoded:

```bash
kubectl get svc cloud-project -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

| Input | Descrição | Default |
| --- | --- | --- |
| `vus` | Usuários virtuais simultâneos | `20` |
| `duration` | Tempo no patamar de carga | `2m` |
| `ramp` | Tempo de rampa até os VUs | `30s` |
| `p95_alvo_ms` | SLO de latência P95 em ms (o job falha se estourar) | `500` |
| `base_url` | *Opcional* — sobrescreve a URL; vazio = descobre no cluster | *(vazio)* |

> 🔐 **Separação de responsabilidades:** só o que é credencial vive em Secret (`MGC_KUBECONFIG`, `DATABASE_URL`, credenciais do registry). A URL é derivada da plataforma e os parâmetros de carga são inputs — não são segredos, então ficam visíveis nos logs.

O job publica um resumo no *Step Summary*, guarda os artefatos (`resumo.md`, `resultado.json`) por 30 dias e **falha se algum threshold do k6 estourar**.

**Localmente** — com [`run-load-test.sh`](run-load-test.sh) (detecta k6 nativo ou cai para Docker):

```bash
./run-load-test.sh http://<IP-DA-VM> 20 2m 500
```

O script [`load/k6/load-test.js`](load/k6/load-test.js) exercita os endpoints de pedidos e reporta latência por rota e throughput. Detalhes em [`docs/architecture.md`](docs/architecture.md#recursos-e-escalonamento-automático-hpa).

---

## 🗺️ Roadmap por competência

O projeto é construído incrementalmente ao longo do curso:

- [x] **Competência 1 & 2** — Desenvolvimento da API REST (FastAPI + SQLAlchemy) e testes
- [x] **Competência 3 — DevOps e Deploy**
  - [x] Conteinerização com Docker
  - [x] Publicação da imagem no Container Registry da Magalu Cloud
  - [x] Manifest Kubernetes (`k8s/app.yaml`)
  - [x] Deploy no cluster K3s da Magalu Cloud
  - [x] Pipeline de CI/CD no GitHub Actions
- [x] **Competência 4 — Banco de dados gerenciado**
  - [x] Conexão com PostgreSQL gerenciado (persistência de dados)
- [x] **Competência 5 — Observabilidade**
  - [x] Métricas Prometheus (`/metrics`) + `ServiceMonitor`
  - [x] Dashboards no Grafana e logs estruturados em JSON
- [x] **Competência 6 — Arquitetura de soluções em nuvem**
  - [x] Diagrama de arquitetura e requisitos não-funcionais ([`docs/architecture.md`](docs/architecture.md))
  - [x] Decisões técnicas documentadas ([ADRs 001–009](docs/adr/README.md))
  - [x] Trade-offs e pontos de melhoria
  - [x] Extras: HPA, `resources` e teste de carga com k6

---

## 📦 Entregas da Competência 6

A Competência 6 é, por definição, **exclusivamente de documentação e análise** — não pedia código novo. Abaixo, o que era **requisito** e o que foi entregue **além do escopo**.

### ✔️ Obrigatório (requisitos da competência)

- [x] Diagrama C2 (Mermaid) e tabela de componentes em [`docs/architecture.md`](docs/architecture.md)
- [x] Requisitos não-funcionais **com número** e estilo arquitetural **nomeado**
- [x] Tabela de trade-offs preenchida
- [x] ADR 001 — K3s para deploy ([`docs/adr/001-kubernetes-deploy.md`](docs/adr/001-kubernetes-deploy.md))
- [x] ADR 002 — DBaaS PostgreSQL ([`docs/adr/002-dbaas-postgresql.md`](docs/adr/002-dbaas-postgresql.md))
- [x] Cada ADR com **Contexto · Alternativas · Decisão · Consequências**
- [x] Pontos de melhoria identificados

### ⭐ Entregas adicionais (além do escopo)

Feitas por iniciativa própria, para aproximar o projeto de um cenário real de produção:

| Extra | O que foi feito |
| --- | --- |
| **+7 ADRs** | Além dos 2 exigidos, documentei as decisões de Container Registry, CI/CD, FastAPI, observabilidade, banco fora do cluster, LoadBalancer vs Ingress e monolito vs microsserviços ([ADRs 003–009](docs/adr/README.md)) com índice |
| **Autoscaling (HPA)** | `resources.requests`/`limits` no Deployment + [`k8s/hpa.yaml`](k8s/hpa.yaml) (2–6 réplicas, CPU 70%), aplicado pelo pipeline |
| **Teste de carga (k6)** | Script [`load/k6/load-test.js`](load/k6/load-test.js), workflow dedicado e [`run-load-test.sh`](run-load-test.sh) para execução local, validando os SLOs (P95 < 500 ms, erro < 1%) |
| **Cobertura de testes** | Elevada de **74% → 100%**, com **gate de 90%** que falha o build (`--cov-fail-under=90`) e publicação no Step Summary do CI |
| **CI/CD "contexto real"** | URL do teste de carga **descoberta via `kubectl`** (sem IP hardcoded) e separação consciente entre *secret* (credencial), *variable* (config) e *input* (tuning) |
| **Correções e organização** | Bugs corrigidos no `run-load-test.sh` (parâmetro de P95 e arquivo de resumo), `servicemonitor.yaml` movido para `k8s/` e README reescrito |

---

## 🎓 Sobre o curso

Projeto desenvolvido no **Move Tech**, formação em Cloud Computing para iniciantes, resultado da parceria **Magalu × Prósper Digital Skills**.

> Inspirado no tutorial [Construindo APIs robustas utilizando Python](https://github.com/luizalabs/tutorial-python-brasil) do LuizaLabs.

---

## 👩‍💻 Autora

**Tamirys Nogueira**  
[GitHub @tamirysnogueira](https://github.com/tamirysnogueira)