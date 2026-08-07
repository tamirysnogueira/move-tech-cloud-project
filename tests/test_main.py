import json
import logging

from fastapi.testclient import TestClient

from app.main import app, JsonFormatter
from app.database import get_db

client = TestClient(app)


# --------------------------------------------------------------------- helpers
def _criar_pedido(customer="Ana"):
    res = client.post("/orders", json={"customer": customer})
    assert res.status_code == 201
    return res.json()["id"]


# ----------------------------------------------------------------------- health
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_health_degraded_quando_banco_indisponivel():
    # Sobrescreve a dependência do banco por uma sessão que falha no execute,
    # exercitando o ramo "degraded" do /health.
    class BancoQuebrado:
        def execute(self, *args, **kwargs):
            raise RuntimeError("banco fora do ar")

    def _get_db_quebrado():
        yield BancoQuebrado()

    app.dependency_overrides[get_db] = _get_db_quebrado
    try:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["database"] == "unavailable"
    finally:
        app.dependency_overrides.clear()


# ------------------------------------------------------------------------ stats
def test_stats():
    _criar_pedido("cliente-stats")
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert set(data["orders"]) == {"total", "open", "cancelled"}
    assert "total" in data["items"]
    assert data["orders"]["total"] >= 1


# ----------------------------------------------------------------------- orders
def test_create_and_list_orders():
    response = client.post("/orders", json={"customer": "Ana"})
    assert response.status_code == 201
    data = response.json()
    assert data["customer"] == "Ana"
    assert data["status"] == "open"
    assert data["items"] == []

    response = client.get("/orders")
    assert response.status_code == 200
    assert any(o["customer"] == "Ana" for o in response.json())


def test_get_order():
    pedido_id = _criar_pedido("Bruno")
    response = client.get(f"/orders/{pedido_id}")
    assert response.status_code == 200
    assert response.json()["id"] == pedido_id


def test_get_order_inexistente():
    response = client.get("/orders/nao-existe")
    assert response.status_code == 404


def test_cancel_order():
    pedido_id = _criar_pedido("Carla")
    response = client.delete(f"/orders/{pedido_id}")
    assert response.status_code == 204

    # Depois de cancelado, o status muda para "cancelled".
    assert client.get(f"/orders/{pedido_id}").json()["status"] == "cancelled"


def test_cancel_order_inexistente():
    response = client.delete("/orders/nao-existe")
    assert response.status_code == 404


# ------------------------------------------------------------------------ items
def test_add_and_list_items():
    pedido_id = _criar_pedido("Diego")

    res = client.post(
        f"/orders/{pedido_id}/items",
        json={"sku": "SKU-1", "description": "Teclado", "quantity": 2},
    )
    assert res.status_code == 201
    item = res.json()
    assert item["sku"] == "SKU-1"
    assert item["quantity"] == 2

    res = client.get(f"/orders/{pedido_id}/items")
    assert res.status_code == 200
    itens = res.json()
    assert len(itens) == 1
    assert itens[0]["description"] == "Teclado"

    # O pedido agora serializa o item embutido (order_to_dict com itens).
    pedido = client.get(f"/orders/{pedido_id}").json()
    assert pedido["items"][0]["sku"] == "SKU-1"


def test_add_item_pedido_inexistente():
    res = client.post(
        "/orders/nao-existe/items",
        json={"sku": "X", "description": "Y", "quantity": 1},
    )
    assert res.status_code == 404


def test_list_items_pedido_inexistente():
    res = client.get("/orders/nao-existe/items")
    assert res.status_code == 404


# -------------------------------------------------------------------------- docs
def test_docs_scalar():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "html" in response.headers["content-type"].lower()


# ---------------------------------------------------------------- log formatter
def test_json_formatter_gera_json_valido():
    record = logging.LogRecord(
        name="app.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="mensagem de teste",
        args=(),
        exc_info=None,
    )
    saida = JsonFormatter().format(record)
    dados = json.loads(saida)
    assert dados == {
        "level": "INFO",
        "message": "mensagem de teste",
        "logger": "app.test",
    }
