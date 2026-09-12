from decimal import Decimal

from fastapi.testclient import TestClient

from src.api import main
from src.aplicacion.banco_facade import BancoFacade
from src.dominio.cuentas import Cuenta, CuentaRepository


def cliente_con_cuentas(monkeypatch):
    repository = CuentaRepository()
    repository.guardar(Cuenta("A-001", "Ana", Decimal("100.00")))
    repository.guardar(Cuenta("B-001", "Bruno", Decimal("20.00")))
    monkeypatch.setattr(main, "facade", BancoFacade(repository))
    return TestClient(main.app)


def test_post_depositar_delega_en_facade(monkeypatch):
    cliente = cliente_con_cuentas(monkeypatch)

    respuesta = cliente.post(
        "/depositar",
        json={"cuenta_id": "A-001", "monto": "10.00", "canal": "pse"},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["tipo"] == "deposito"
    assert respuesta.json()["estado"] == "COMPLETADA"


def test_post_transferir_y_retirar_delegan_en_facade(monkeypatch):
    cliente = cliente_con_cuentas(monkeypatch)

    transferencia = cliente.post(
        "/transferir",
        json={
            "origen_id": "A-001",
            "destino_id": "B-001",
            "monto": "25.00",
        },
    )
    retiro = cliente.post(
        "/retirar",
        json={"cuenta_id": "A-001", "monto": "10.00"},
    )

    assert transferencia.status_code == 200
    assert transferencia.json()["estado"] == "COMPLETADA"
    assert retiro.status_code == 200
    assert retiro.json()["estado"] == "COMPLETADA"


def test_post_reversar_delega_en_facade(monkeypatch):
    cliente = cliente_con_cuentas(monkeypatch)
    transferencia = cliente.post(
        "/transferir",
        json={
            "origen_id": "A-001",
            "destino_id": "B-001",
            "monto": "25.00",
        },
    )

    respuesta = cliente.post(
        "/reversar",
        json={"transaccion_id": transferencia.json()["id"]},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "REVERSADA"


def test_api_rechaza_monto_no_positivo(monkeypatch):
    cliente = cliente_con_cuentas(monkeypatch)

    respuesta = cliente.post(
        "/retirar",
        json={"cuenta_id": "A-001", "monto": "0"},
    )

    assert respuesta.status_code == 422


def test_facade_demo_deja_cuentas_disponibles_para_swagger(monkeypatch):
    monkeypatch.setattr(main, "facade", main._crear_facade_demo())
    cliente = TestClient(main.app)

    respuesta = cliente.post(
        "/retirar",
        json={"cuenta_id": "A-001", "monto": "10.00"},
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "COMPLETADA"
