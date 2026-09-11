"""Adapters fake para tarjeta, PSE y billetera digital."""

from decimal import Decimal

from src.dominio.contratos import ProveedorExternoPort


class TarjetaAdapter(ProveedorExternoPort):
    """Adapta una red de tarjetas simulada al puerto del dominio."""

    def __init__(self) -> None:
        self.montos_procesados: list[Decimal] = []

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return True


class PSEAdapter(ProveedorExternoPort):
    """Adapta un proveedor PSE simulado al puerto del dominio."""

    def __init__(self) -> None:
        self.montos_procesados: list[Decimal] = []

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return True


class BilleteraAdapter(ProveedorExternoPort):
    """Adapta una billetera digital simulada al puerto del dominio."""

    def __init__(self) -> None:
        self.montos_procesados: list[Decimal] = []

    def procesar(self, monto: Decimal) -> bool:
        self.montos_procesados.append(monto)
        return True


__all__ = ["TarjetaAdapter", "PSEAdapter", "BilleteraAdapter"]
