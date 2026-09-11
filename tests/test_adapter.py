from decimal import Decimal

import pytest

from src.dominio.contratos import ProveedorExternoPort
from src.infraestructura.proveedores import (
    BilleteraAdapter,
    PSEAdapter,
    TarjetaAdapter,
)


@pytest.mark.parametrize(
    "adapter",
    [TarjetaAdapter(), PSEAdapter(), BilleteraAdapter()],
)
def test_adapters_fake_procesan_sin_llamadas_externas(adapter):
    monto = Decimal("25.50")

    resultado = adapter.procesar(monto)

    assert resultado is True
    assert adapter.montos_procesados == [monto]
    assert isinstance(adapter, ProveedorExternoPort)


class FakeProveedorFalla(ProveedorExternoPort):
    """Fake de prueba que simula un proveedor externo no disponible."""

    def procesar(self, monto: Decimal) -> bool:
        return False


def test_fake_puede_simular_fallo_del_proveedor():
    proveedor = FakeProveedorFalla()

    resultado = proveedor.procesar(Decimal("10.00"))

    assert resultado is False
    assert isinstance(proveedor, ProveedorExternoPort)
