from decimal import Decimal

import pytest

from src.aplicacion.banco_facade import BancoFacade
from src.dominio.cuentas import Cuenta, CuentaRepository
from src.dominio.estados import TransicionInvalidaError


def crear_facade_con_limite(limite: str = "100.00"):
    repository = CuentaRepository()
    repository.guardar(
        Cuenta(
            "A-001",
            "Ana",
            Decimal("500.00"),
            limite_diario_transferencia=Decimal(limite),
        )
    )
    repository.guardar(Cuenta("B-001", "Bruno", Decimal("0.00")))
    return BancoFacade(repository), repository


def test_transferencias_hasta_el_limite_diario_son_validas():
    facade, repository = crear_facade_con_limite()

    primera = facade.transferir("A-001", "B-001", Decimal("60.00"))
    segunda = facade.transferir("A-001", "B-001", Decimal("40.00"))

    assert primera["estado"] == "COMPLETADA"
    assert segunda["estado"] == "COMPLETADA"
    assert repository.obtener("A-001").transferido_hoy == Decimal("100.00")


def test_transferencia_que_supera_el_limite_diario_se_rechaza():
    facade, repository = crear_facade_con_limite()
    facade.transferir("A-001", "B-001", Decimal("60.00"))

    resultado = facade.transferir("A-001", "B-001", Decimal("40.01"))

    assert resultado["estado"] == "RECHAZADA"
    assert repository.obtener("A-001").transferido_hoy == Decimal("60.00")
    assert repository.obtener("A-001").saldo == Decimal("440.00")
    assert repository.obtener("B-001").saldo == Decimal("60.00")


def test_segundo_reverso_es_invalido_y_no_vuelve_a_mover_el_saldo():
    facade, repository = crear_facade_con_limite("500.00")
    transferencia = facade.transferir("A-001", "B-001", Decimal("25.00"))
    facade.reversar(transferencia["id"])
    saldo_origen = repository.obtener("A-001").saldo
    saldo_destino = repository.obtener("B-001").saldo

    with pytest.raises(TransicionInvalidaError):
        facade.reversar(transferencia["id"])

    assert repository.obtener("A-001").saldo == saldo_origen
    assert repository.obtener("B-001").saldo == saldo_destino
