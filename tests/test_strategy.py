from decimal import Decimal

import pytest

from src.aplicacion.comision_strategy import (
    ComisionBilletera,
    ComisionPSE,
    ComisionTarjeta,
)
from src.dominio.contratos import ComisionStrategy


@pytest.mark.parametrize(
    ("estrategia", "esperada"),
    [
        (ComisionTarjeta(), Decimal("3.20")),
        (ComisionPSE(), Decimal("1.50")),
        (ComisionBilletera(), Decimal("2.00")),
    ],
)
def test_calcula_comision_para_monto_de_cien(estrategia, esperada):
    assert estrategia.calcular(Decimal("100.00")) == esperada


@pytest.mark.parametrize(
    "estrategia",
    [ComisionTarjeta(), ComisionPSE(), ComisionBilletera()],
)
def test_las_estrategias_cumplen_el_contrato(estrategia):
    assert isinstance(estrategia, ComisionStrategy)


def test_tarjeta_conserva_precision_decimal():
    estrategia = ComisionTarjeta()

    resultado = estrategia.calcular(Decimal("0.10"))

    assert resultado == Decimal("0.3029")
    assert isinstance(resultado, Decimal)
