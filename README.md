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
- 🚀 Com **deploy automático** disparado pelo GitHub Actions

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
| Registro de imagens | Magalu Cloud Container Registry |
| CI/CD | GitHub Actions |
| Observabilidade | Logs estruturados em JSON · métricas no formato Prometheus |

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

📚 Documentação interativa (Swagger UI) disponível em `/docs`.

---

## 🗂️ Estrutura do repositório

```
move-tech-cloud-project/
├── app/                      # Código da aplicação (FastAPI + SQLAlchemy)
├── tests/                    # Testes automatizados (Pytest)
├── k8s/
│   └── app.yaml              # Manifests do Deployment e Service (Kubernetes)
├── .github/
│   └── workflows/
│       └── deploy.yml        # Pipeline de CI/CD (GitHub Actions)
├── Dockerfile                # Receita da imagem Docker
├── docker-compose.yml        # Execução local
├── pyproject.toml            # Dependências e configuração do projeto
└── README.md
```

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

## ☁️ Deploy na Magalu Cloud

O deploy é totalmente automatizado pelo pipeline do GitHub Actions, que executa duas etapas em sequência:

1. **`test`** — instala as dependências e roda os testes automatizados (Pytest).
2. **`build-and-deploy`** (apenas se os testes passarem):
   - Faz login no Container Registry da Magalu Cloud
   - Constrói a imagem Docker e publica no registry
   - Configura o acesso ao cluster via `kubeconfig`
   - Aplica os manifests no Kubernetes e aguarda o rollout concluir

### Secrets necessários

Configurados em **Settings → Secrets and variables → Actions**:

| Secret | Descrição |
| --- | --- |
| `MGC_REGISTRY_USER` | Usuário do Container Registry |
| `MGC_REGISTRY_PASSWORD` | Senha do Container Registry |
| `MGC_REGISTRY_NAME` | Nome do registry na Magalu Cloud |
| `MGC_KUBECONFIG` | Conteúdo do arquivo `kubeconfig` do cluster |

### Verificação

Após o deploy, o serviço fica acessível pelo IP público do cluster:

```bash
kubectl get svc cloud-application   # coluna EXTERNAL-IP
```

- Health check: `http://<IP-DA-VM>/health` → `{"status": "ok"}`
- Documentação: `http://<IP-DA-VM>/docs`

---

## 🗺️ Roadmap por competência

O projeto é construído incrementalmente ao longo do curso:

- [x] **Competência 1 & 2** — Desenvolvimento da API REST (FastAPI + SQLAlchemy) e testes
- [ ] **Competência 3 — DevOps e Deploy** *(em andamento)*
  - [x] Conteinerização com Docker
  - [ ] Publicação da imagem no Container Registry da Magalu Cloud
  - [ ] Manifest Kubernetes (`k8s/app.yaml`)
  - [ ] Deploy no cluster K3s da Magalu Cloud
  - [ ] Pipeline de CI/CD no GitHub Actions
- [ ] **Competência 4 — Banco de dados gerenciado**
  - [ ] Conexão com PostgreSQL gerenciado (persistência de dados)

> As caixas serão marcadas conforme cada etapa é concluída.

---

## 🎓 Sobre o curso

Projeto desenvolvido no **Move Tech**, formação em Cloud Computing para iniciantes, resultado da parceria **Magalu × Prósper Digital Skills**.

> Inspirado no tutorial [Construindo APIs robustas utilizando Python](https://github.com/luizalabs/tutorial-python-brasil) do LuizaLabs.

---

## 👩‍💻 Autora

**Tamirys Nogueira**  
[GitHub @tamirysnogueira](https://github.com/tamirysnogueira)