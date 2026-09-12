from decimal import Decimal

import pytest

from src.dominio.contratos import ProveedorExternoPort
from src.infraestructura.proveedores import (
    BilleteraAdapter,
    BilleteraProviderFake,
    PSEAdapter,
    PSEProviderFake,
    TarjetaAdapter,
    TarjetaProviderFake,
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


def test_adapter_traduce_la_operacion_del_proveedor_de_tarjeta():
    proveedor = TarjetaProviderFake()
    adapter = TarjetaAdapter(proveedor)

    assert adapter.procesar(Decimal("12.50")) is True
    assert proveedor.valores_cobrados == [Decimal("12.50")]


def test_adapters_envuelven_interfaces_incompatibles():
    pse = PSEProviderFake()
    billetera = BilleteraProviderFake()

    assert PSEAdapter(pse).procesar(Decimal("8.00")) is True
    assert BilleteraAdapter(billetera).procesar(Decimal("9.00")) is True
    assert pse.valores_procesados == [Decimal("8.00")]
    assert billetera.valores_autorizados == [Decimal("9.00")]
