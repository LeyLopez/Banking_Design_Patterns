"""Adapters fake para tarjeta, PSE y billetera digital."""

from decimal import Decimal
from typing import Protocol

from src.dominio.contratos import ProveedorExternoPort


class ProveedorTarjetaFake(Protocol):
    def cobrar(self, valor: Decimal) -> bool:
        ...


class ProveedorPSEFake(Protocol):
    def iniciar_pago(self, valor: Decimal) -> bool:
        ...


class ProveedorBilleteraFake(Protocol):
    def autorizar_pago(self, valor: Decimal) -> bool:
        ...


class TarjetaProviderFake:
    def __init__(self) -> None:
        self.valores_cobrados: list[Decimal] = []

    def cobrar(self, valor: Decimal) -> bool:
        self.valores_cobrados.append(valor)
        return True


class PSEProviderFake:
    def __init__(self) -> None:
        self.valores_procesados: list[Decimal] = []

    def iniciar_pago(self, valor: Decimal) -> bool:
        self.valores_procesados.append(valor)
        return True


class BilleteraProviderFake:
    def __init__(self) -> None:
        self.valores_autorizados: list[Decimal] = []

    def autorizar_pago(self, valor: Decimal) -> bool:
        self.valores_autorizados.append(valor)
        return True


class TarjetaAdapter(ProveedorExternoPort):
    """Adapta una red de tarjetas simulada al puerto del dominio."""

    def __init__(self, proveedor: ProveedorTarjetaFake | None = None) -> None:
        self.montos_procesados: list[Decimal] = []
        self.proveedor = proveedor or TarjetaProviderFake()

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return self.proveedor.cobrar(monto)


class PSEAdapter(ProveedorExternoPort):
    """Adapta un proveedor PSE simulado al puerto del dominio."""

    def __init__(self, proveedor: ProveedorPSEFake | None = None) -> None:
        self.montos_procesados: list[Decimal] = []
        self.proveedor = proveedor or PSEProviderFake()

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return self.proveedor.iniciar_pago(monto)


class BilleteraAdapter(ProveedorExternoPort):
    """Adapta una billetera digital simulada al puerto del dominio."""

    def __init__(self, proveedor: ProveedorBilleteraFake | None = None) -> None:
        self.montos_procesados: list[Decimal] = []
        self.proveedor = proveedor or BilleteraProviderFake()

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return self.proveedor.autorizar_pago(monto)


__all__ = [
    "BilleteraAdapter",
    "BilleteraProviderFake",
    "PSEAdapter",
    "PSEProviderFake",
    "TarjetaAdapter",
    "TarjetaProviderFake",
]
