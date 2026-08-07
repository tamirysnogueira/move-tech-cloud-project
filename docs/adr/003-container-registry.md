# ADR 003 — Usar o Container Registry da Magalu Cloud

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

O deploy no K3s (ver [ADR 001](001-kubernetes-deploy.md)) consome a aplicação como uma
**imagem Docker**. O cluster precisa buscar (`docker pull`) essa imagem de algum lugar, e o
pipeline de CI/CD precisa publicá-la (`docker push`) a cada release. É preciso decidir
**onde** armazenar e versionar essas imagens de forma acessível ao cluster e ao pipeline.

## Alternativas consideradas

- **Container Registry da Magalu Cloud** — registry privado dentro da própria MGC; tráfego
  interno até a VM; credenciais integradas ao provedor; cobrado por armazenamento.
- **Docker Hub (público/privado)** — amplamente conhecido; plano gratuito com limite de
  `pull rate`; imagem trafega pela internet pública; risco de exposição no tier público.
- **GitHub Container Registry (ghcr.io)** — bem integrado ao GitHub Actions; porém a imagem
  sai da MGC e volta pela internet até a VM, e adiciona um provedor a mais na cadeia.

## Decisão

Usar o **Container Registry da Magalu Cloud**
(`container-registry.br-se1.magalu.cloud/<registry>/cloud-project`). O pipeline autentica
com os secrets `MGC_REGISTRY_USER` / `MGC_REGISTRY_PASSWORD`, publica a tag `:latest` e o
K3s a consome no `image:` do Deployment. Critério: manter a imagem no mesmo provedor do
cluster (registry e runtime na mesma nuvem), sem limite de `pull rate` e sem expor a imagem
publicamente.

## Consequências

**Positivas:**
- Registry privado por padrão — a imagem não fica exposta publicamente
- Proximidade com a VM/cluster na mesma nuvem (pull mais rápido e barato)
- Sem limites de `pull rate` como os do Docker Hub gratuito
- Credenciais integradas ao ecossistema MGC, já usadas no pipeline

**Negativas:**
- Custo de armazenamento por imagem (baixo para imagens < 500 MB)
- Acoplamento ao provedor MGC para o fluxo de imagens
- Uso da tag mutável `:latest` dificulta rollback e rastreabilidade — o próximo passo é
  adotar tags imutáveis por commit (ex.: `:sha-<git_sha>`)
