"""Estrategias de cálculo de comisión por canal."""

from decimal import Decimal

from src.dominio.contratos import ComisionStrategy


class ComisionTarjeta(ComisionStrategy):
    """Calcula la comisión del canal de tarjeta: 2.9% más 0.30."""

    def calcular(self, monto: Decimal) -> Decimal:
        return monto * Decimal("0.029") + Decimal("0.30")


class ComisionPSE(ComisionStrategy):
    """Calcula la comisión del canal PSE: 1.5%."""

    def calcular(self, monto: Decimal) -> Decimal:
        return monto * Decimal("0.015")


class ComisionBilletera(ComisionStrategy):
    """Calcula la comisión del canal de billetera: 2%."""

    def calcular(self, monto: Decimal) -> Decimal:
        return monto * Decimal("0.02")


__all__ = ["ComisionTarjeta", "ComisionPSE", "ComisionBilletera"]
