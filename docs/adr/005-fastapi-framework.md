# ADR 005 — Usar FastAPI (Python) como framework da API

**Status:** Aceito
**Data:** 2026-08-07

## Contexto

O núcleo do projeto é uma **API REST** de pedidos e itens. Era preciso escolher a
linguagem e o framework web que dariam produtividade no desenvolvimento, boa integração com
o restante da stack (SQLAlchemy, Pytest, Docker) e documentação de API sem esforço extra.

## Alternativas consideradas

- **FastAPI (Python)** — tipagem com Pydantic e validação automática; OpenAPI/Swagger
  gerado do código; curva de aprendizado baixa; ecossistema Python maduro (SQLAlchemy,
  Pytest).
- **Node.js (Express/Nest)** — ótimo para I/O assíncrono; exige mais configuração para
  validação e documentação automática (no caso do Express).
- **Go** — excelente desempenho e binários enxutos; mais verboso para CRUD e com curva de
  aprendizado maior para a equipe.
- **Java (Spring Boot)** — muito robusto e padrão de mercado corporativo; imagem e tempo de
  boot maiores, mais cerimônia para um serviço pequeno.

## Decisão

Usar **FastAPI** sobre **Uvicorn**, com **Pydantic** para validação, **SQLAlchemy** como
ORM e **Pytest** para testes. A documentação interativa é servida em `/docs` (Scalar sobre
o schema OpenAPI). Critério: baixa curva de aprendizado e alta produtividade para um serviço
de escopo enxuto, com validação e documentação "de graça".

## Consequências

**Positivas:**
- Validação e serialização automáticas via Pydantic (menos código de borda)
- Documentação OpenAPI/Swagger gerada a partir do próprio código
- Ecossistema Python facilita testes (Pytest) e persistência (SQLAlchemy)
- Aplicação leve e stateless, adequada ao escalonamento horizontal do K3s

**Negativas:**
- Desempenho bruto inferior a Go em cenários de altíssima concorrência
- Depende de servidor ASGI (Uvicorn) e boa gestão de concorrência para escalar
- A ausência de camada de serviço separada (regras hoje em `app/main.py`) tende a acoplar
  apresentação e negócio conforme o domínio cresce
