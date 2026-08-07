#!/usr/bin/env bash
#
# Roda o mesmo teste de carga do workflow "Teste de carga (k6)", localmente.
# Detecta k6 nativo ou cai para Docker automaticamente.
#
#   ./run-load-test.sh http://<EXTERNAL-IP>
#   ./run-load-test.sh http://<EXTERNAL-IP> 40 3m 500
#
# Argumentos (todos opcionais menos o primeiro):
#   1  BASE_URL   URL da API
#   2  VUS        usuários virtuais        (padrão 20)
#   3  DURATION   duração do patamar       (padrão 5m)
#   4  P95_MS     alvo de P95 em ms        (padrão 500)

set -euo pipefail

BASE_URL="${1:-}"
VUS="${2:-20}"
DURATION="${3:-5m}"
P95_MS="${4:-500}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_FILE="$SCRIPT_DIR/load/k6/load-test.js"

# ---------------------------------------------------------------- validações
if [[ -z "$BASE_URL" ]]; then
  echo "uso: $0 <base_url> [vus] [duration] [p95_ms]" >&2
  echo "ex.:  $0 http://200.1.2.3 20 5m 500" >&2
  exit 1
fi

if [[ ! -f "$TEST_FILE" ]]; then
  echo "erro: não encontrei $TEST_FILE" >&2
  echo "rode este script a partir da raiz do repositório." >&2
  exit 1
fi

BASE_URL="${BASE_URL%/}"   # remove barra final

echo "→ verificando se a API responde em $BASE_URL/health"
if ! curl -fsS --max-time 10 "$BASE_URL/health" > /dev/null; then
  echo "erro: a API não respondeu. Confira o EXTERNAL-IP:" >&2
  echo "  kubectl get svc" >&2
  exit 1
fi
echo "  ok"

echo
echo "════════════════════════════════════════════"
echo "  alvo:     $BASE_URL"
echo "  VUs:      $VUS"
echo "  patamar:  $DURATION  (+30s rampa de cada lado)"
echo "  SLO P95:  ${P95_MS} ms"
echo "════════════════════════════════════════════"
echo

# ------------------------------------------------------------------ execução
if command -v k6 > /dev/null 2>&1; then
  echo "→ usando k6 nativo ($(k6 version 2>&1 | head -1))"
  echo
  BASE_URL="$BASE_URL" VUS="$VUS" DURATION="$DURATION" P95_MS="$P95_MS" \
    k6 run "$TEST_FILE"

elif command -v docker > /dev/null 2>&1; then
  echo "→ k6 não instalado, usando Docker (grafana/k6)"
  echo
  # --network host é necessário no Linux se o alvo for localhost.
  # Para um IP público (o caso do lab) a rede padrão já basta.
  NET_FLAG=""
  if [[ "$BASE_URL" == *"localhost"* || "$BASE_URL" == *"127.0.0.1"* ]]; then
    NET_FLAG="--network host"
    echo "  (alvo local detectado: usando --network host)"
  fi

  docker run --rm -i $NET_FLAG \
    -v "$SCRIPT_DIR:/work" -w /work \
    -e BASE_URL="$BASE_URL" \
    -e VUS="$VUS" \
    -e DURATION="$DURATION" \
    -e P95_MS="$P95_MS" \
    grafana/k6:latest run /work/load/k6/load-test.js

else
  echo "erro: nem k6 nem docker encontrados." >&2
  echo >&2
  echo "instale um dos dois:" >&2
  echo "  macOS:   brew install k6" >&2
  echo "  Linux:   https://grafana.com/docs/k6/latest/set-up/install-k6/" >&2
  echo "  Docker:  https://docs.docker.com/get-docker/" >&2
  echo >&2
  echo "ou use o fallback sem dependências:" >&2
  echo "  python3 load/simple-load-test.py $BASE_URL --vus $VUS" >&2
  exit 1
fi

# -------------------------------------------------------------------- saída
echo
if [[ -f summary.md ]]; then
  echo "════════════════════════════════════════════"
  cat summary.md
  echo "════════════════════════════════════════════"
  echo
  echo "→ resumo salvo em ./summary.md"
  echo "  copie estes números para a seção de escalabilidade do docs/architecture.md"
fi
