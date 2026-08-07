# ADR 008 — Expor a aplicação via Service LoadBalancer (Klipper ServiceLB)

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

A aplicação precisa ser acessível publicamente e distribuir o tráfego entre as
[2 réplicas](../architecture.md). O [K3s](001-kubernetes-deploy.md) roda em uma VM com um IP
público. É preciso decidir **como** expor o serviço para fora do cluster: qual objeto do
Kubernetes recebe o tráfego externo e o encaminha aos pods.

## Alternativas consideradas

- **Service `type: LoadBalancer` com Klipper ServiceLB** — o load balancer embutido do K3s;
  atribui a porta ao IP da VM sem infraestrutura extra; provisionamento imediato; opera na
  camada 4 (TCP).
- **Ingress (Traefik, que já vem no K3s)** — roteamento HTTP na camada 7; permite host/path
  routing, TLS e múltiplos serviços sob um mesmo IP; porém adiciona uma camada de
  configuração para um único serviço.
- **Service `type: NodePort`** — expõe uma porta alta (30000–32767) em cada nó; simples, mas
  a porta não-padrão é ruim para consumo público e exige o IP do nó.

## Decisão

Expor a aplicação com um **Service `type: LoadBalancer`**
([`k8s/app.yaml`](../k8s/app.yaml)), atendido pelo **Klipper ServiceLB** do K3s, publicando
a porta **80** do IP público da VM e encaminhando para a `targetPort` 8000 dos pods.
Critério: menor complexidade para expor **um único serviço** — não há, hoje, múltiplos
hosts/paths que justifiquem um Ingress.

## Consequências

**Positivas:**
- Zero infraestrutura adicional — o ServiceLB já vem com o K3s
- Balanceamento entre as réplicas na porta 80 do IP da VM
- Manifesto simples e portável para qualquer Kubernetes

**Negativas:**
- Sem terminação TLS/HTTPS nativa — TLS exigiria Ingress ou um proxy à frente
- Sem roteamento por host/path: um IP:porta atende a um serviço só
- Amarrado ao IP da VM, que muda se a VM for substituída ([ADR 001](001-kubernetes-deploy.md))
- Quando surgir um segundo serviço ou a necessidade de HTTPS, o passo natural é **migrar
  para Ingress** (Traefik) — os pods e Services permanecem inalterados
