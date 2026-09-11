import pytest

from before.banking_before import Banco


@pytest.fixture
def banco():
    instancia = Banco()
    instancia.crear_cuenta("A-001", "Ana", 100.00)
    instancia.crear_cuenta("B-001", "Bruno", 20.00)
    return instancia


def test_deposito_con_tarjeta_descuenta_comision_y_completa_transaccion(
    banco, capsys
):
    resultado = banco.depositar("A-001", 100.00, "tarjeta")

    transaccion = banco.transacciones[0]
    assert resultado is True
    assert transaccion["estado"] == "COMPLETADA"
    assert transaccion["comision"] == 3.2
    assert banco.mostrar_saldo("A-001") == 196.8
    assert banco.cuentas["A-001"]["historial"] == [transaccion]

    salida = capsys.readouterr().out
    assert "Tarjeta fake procesando 100.00" in salida
    assert "Notificacion: nuevo saldo de A-001: 196.80" in salida


def test_caracteriza_precision_incorrecta_de_float():
    banco = Banco()
    banco.crear_cuenta("A-001", "Ana")

    banco.depositar("A-001", 0.1, "desconocido")
    banco.depositar("A-001", 0.2, "desconocido")

    saldo = banco.mostrar_saldo("A-001")
    assert saldo == 0.30000000000000004
    assert saldo != 0.3


def test_retiro_mayor_al_saldo_se_rechaza_y_no_se_agrega_al_historial(
    banco, capsys
):
    resultado = banco.retirar("A-001", 100.01)

    transaccion = banco.transacciones[0]
    assert resultado is False
    assert transaccion["estado"] == "RECHAZADA"
    assert banco.mostrar_saldo("A-001") == 100.00
    assert banco.cuentas["A-001"]["historial"] == []

    salida = capsys.readouterr().out
    assert "saldo insuficiente" in salida


@pytest.mark.parametrize(
    ("canal", "monto", "comision"),
    [
        ("tarjeta", 100.0, 3.2),
        ("pse", 100.0, 1.5),
        ("billetera", 100.0, 2.0),
        ("interno", 100.0, 0.0),
    ],
)
def test_calcula_comision_segun_canal(canal, monto, comision):
    banco = Banco()

    assert banco.calcular_comision(monto, canal) == comision


def test_transferencia_completa_descuenta_origen_y_acredita_destino(banco):
    resultado = banco.transferir("A-001", "B-001", 25.00)

    transaccion = banco.transacciones[0]
    assert resultado is True
    assert transaccion["tipo"] == "transferencia"
    assert transaccion["estado"] == "COMPLETADA"
    assert banco.mostrar_saldo("A-001") == 75.00
    assert banco.mostrar_saldo("B-001") == 45.00


def test_cuenta_inexistente_rechaza_la_transaccion(capsys):
    banco = Banco()

    resultado = banco.depositar("NO-EXISTE", 10.00, "pse")

    assert resultado is False
    assert banco.transacciones[0]["estado"] == "RECHAZADA"
    assert "cuenta inexistente" in capsys.readouterr().out
