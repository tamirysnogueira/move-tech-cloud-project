# ADR 004 — Automatizar o deploy com GitHub Actions

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

O caminho da aplicação até a nuvem envolve várias etapas repetitivas e sujeitas a erro:
rodar os testes, construir a imagem Docker, publicar no
[Container Registry](003-container-registry.md), aplicar os manifests no
[K3s](001-kubernetes-deploy.md) e aguardar o rollout. Fazer isso manualmente é lento,
inconsistente e não deixa rastro de quem fez o quê. É preciso um mecanismo de CI/CD.

## Alternativas consideradas

- **GitHub Actions** — nativo ao repositório (o código já está no GitHub); secrets
  integrados; sem servidor de CI para manter; YAML versionado junto com o projeto.
- **Deploy manual** (via terminal do desenvolvedor) — zero configuração inicial; porém sem
  consistência, sem rastreabilidade e dependente da máquina de quem executa.
- **Jenkins / GitLab CI (self-hosted)** — muito flexível; exige provisionar e manter um
  servidor de CI, o que não se justifica no escopo do projeto.

## Decisão

Usar **GitHub Actions** com o workflow `.github/workflows/deploy.yaml`, em dois jobs
encadeados: `test` (instala dependências com Poetry e roda o Pytest) e `build-and-deploy`
(login no registry, build/push da imagem, `kubectl apply` dos manifests e
`kubectl rollout status`). O `build-and-deploy` só executa se o `test` passar
(`needs: test`). Critério: consistência e rastreabilidade sem operar infraestrutura de CI.

## Consequências

**Positivas:**
- Pipeline versionado junto com o código (IaC do próprio processo de deploy)
- Deploy só acontece com os testes verdes (`needs: test` como gate de qualidade)
- Rastreabilidade: cada deploy fica registrado no histórico do Actions
- Sem servidor de CI para manter; secrets gerenciados pelo próprio GitHub

**Negativas:**
- Acoplamento ao GitHub como plataforma de CI/CD
- O gatilho atual é `workflow_dispatch` (manual) — não há deploy contínuo em `push`
  para a branch principal ainda
- O deploy depende de secrets (`MGC_*`, `MGC_KUBECONFIG`, `DATABASE_URL`) corretamente
  configurados; um secret ausente quebra o pipeline
