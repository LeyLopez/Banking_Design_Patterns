from decimal import Decimal

from src.aplicacion.banco_facade import BancoFacade
from src.dominio.cuentas import Cuenta, CuentaRepository
from src.infraestructura.notificaciones import SujetoTransaccion


def crear_facade():
    repository = CuentaRepository()
    repository.guardar(Cuenta("A-001", "Ana", Decimal("100.00")))
    repository.guardar(Cuenta("B-001", "Bruno", Decimal("20.00")))
    return BancoFacade(repository, sujeto=SujetoTransaccion()), repository


def test_flujo_completo_exitoso_deposito_transferencia_y_reverso():
    facade, repository = crear_facade()

    deposito = facade.depositar("A-001", Decimal("50.00"), "tarjeta")
    transferencia = facade.transferir("A-001", "B-001", Decimal("25.00"))
    reversado = facade.reversar(transferencia["id"])

    assert deposito["estado"] == "COMPLETADA"
    assert transferencia["estado"] == "REVERSADA"
    assert reversado["estado"] == "REVERSADA"
    assert repository.obtener("A-001").saldo == Decimal("148.25")
    assert repository.obtener("B-001").saldo == Decimal("20.00")


def test_rechazo_por_saldo_insuficiente_no_muta_la_cuenta():
    facade, repository = crear_facade()

    resultado = facade.retirar("A-001", Decimal("100.01"))

    assert resultado["estado"] == "RECHAZADA"
    assert repository.obtener("A-001").saldo == Decimal("100.00")
    assert repository.obtener("A-001").historial == [resultado]
