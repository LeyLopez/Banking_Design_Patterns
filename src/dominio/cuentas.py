"""Entidades y repositorio en memoria del dominio bancario."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Cuenta:
    """Cuenta bancaria con saldo e historial de transacciones."""

    id: str
    titular: str
    saldo: Decimal
    limite_diario_transferencia: Decimal = Decimal("1000.00")
    transferido_hoy: Decimal = Decimal("0")
    historial: list[dict] = field(default_factory=list)


class CuentaRepository:
    """Repositorio en memoria para cuentas del alcance educativo."""

    def __init__(self) -> None:
        self._cuentas: dict[str, Cuenta] = {}

    def guardar(self, cuenta: Cuenta) -> None:
        self._cuentas[cuenta.id] = cuenta

    def obtener(self, cuenta_id: str) -> Cuenta:
        return self._cuentas[cuenta_id]
