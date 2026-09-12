"""Facade de operaciones bancarias del código después."""

from decimal import Decimal
from typing import Any

from src.aplicacion.comision_strategy import (
    ComisionBilletera,
    ComisionPSE,
    ComisionTarjeta,
)
from src.dominio.contratos import (
    ComisionStrategy,
    EstadoTransaccion,
    ProveedorExternoPort,
)
from src.dominio.cuentas import Cuenta, CuentaRepository
from src.dominio.estados import EstadoCreada
from src.infraestructura.notificaciones import SujetoTransaccion
from src.infraestructura.proveedores import (
    BilleteraAdapter,
    PSEAdapter,
    TarjetaAdapter,
)


class BancoFacade:
    """Punto de entrada simple para las operaciones bancarias."""

    def __init__(
        self,
        repository: CuentaRepository | None = None,
        estrategias: dict[str, ComisionStrategy] | None = None,
        proveedores: dict[str, ProveedorExternoPort] | None = None,
        sujeto: SujetoTransaccion | None = None,
    ) -> None:
        self._repository = repository or CuentaRepository()
        self._estrategias = estrategias or {
            "tarjeta": ComisionTarjeta(),
            "pse": ComisionPSE(),
            "billetera": ComisionBilletera(),
        }
        self._proveedores = proveedores or {
            "tarjeta": TarjetaAdapter(),
            "pse": PSEAdapter(),
            "billetera": BilleteraAdapter(),
        }
        self._sujeto = sujeto or SujetoTransaccion()
        self._transacciones: dict[str, dict[str, Any]] = {}
        self._siguiente_id = 1
        self._reversores = {
            "deposito": self._revertir_deposito,
            "retiro": self._revertir_retiro,
            "transferencia": self._revertir_transferencia,
        }

    def depositar(
        self, cuenta_id: str, monto: Decimal, canal: str = "tarjeta"
    ) -> dict[str, Any]:
        cuenta = self._repository.obtener(cuenta_id)
        estrategia = self._estrategias[canal]
        proveedor = self._proveedores[canal]
        transaccion = self._nueva_transaccion(
            "deposito", cuenta_id, monto, canal=canal
        )
        transaccion["comision"] = estrategia.calcular(transaccion["monto"])
        if not proveedor.procesar(transaccion["monto"]):
            return self._rechazar(transaccion, cuenta)

        cuenta.saldo += transaccion["monto"] - transaccion["comision"]
        self._completar(transaccion)
        cuenta.historial.append(transaccion)
        return transaccion

    def retirar(self, cuenta_id: str, monto: Decimal) -> dict[str, Any]:
        cuenta = self._repository.obtener(cuenta_id)
        transaccion = self._nueva_transaccion("retiro", cuenta_id, monto)
        total = transaccion["monto"]
        if cuenta.saldo < total:
            return self._rechazar(transaccion, cuenta)

        cuenta.saldo -= total
        self._completar(transaccion)
        cuenta.historial.append(transaccion)
        return transaccion

    def transferir(
        self, origen_id: str, destino_id: str, monto: Decimal
    ) -> dict[str, Any]:
        origen = self._repository.obtener(origen_id)
        destino = self._repository.obtener(destino_id)
        transaccion = self._nueva_transaccion(
            "transferencia", origen_id, monto, destino_id=destino_id
        )
        monto_transferencia = transaccion["monto"]
        limite_superado = (
            origen.transferido_hoy + monto_transferencia
            > origen.limite_diario_transferencia
        )
        if origen.saldo < monto_transferencia or limite_superado:
            return self._rechazar(transaccion, origen)

        origen.saldo -= monto_transferencia
        destino.saldo += monto_transferencia
        origen.transferido_hoy += monto_transferencia
        self._completar(transaccion)
        origen.historial.append(transaccion)
        return transaccion

    def reversar(self, transaccion_id: str) -> dict[str, Any]:
        transaccion = self._transacciones[transaccion_id]
        origen = self._repository.obtener(transaccion["cuenta_id"])
        destino_id = transaccion.get("destino_id")
        destino = self._repository.obtener(destino_id) if destino_id else None

        self._cambiar_estado(transaccion, "reversar")
        self._revertir_saldo(transaccion, origen, destino)
        return transaccion

    def _nueva_transaccion(
        self,
        tipo: str,
        cuenta_id: str,
        monto: Decimal,
        destino_id: str | None = None,
        canal: str = "interno",
    ) -> dict[str, Any]:
        transaccion = {
            "id": f"tx-{self._siguiente_id}",
            "tipo": tipo,
            "cuenta_id": cuenta_id,
            "destino_id": destino_id,
            "monto": Decimal(str(monto)),
            "canal": canal,
            "comision": Decimal("0"),
            "estado": "CREADA",
            "_estado": EstadoCreada(),
        }
        self._siguiente_id += 1
        self._transacciones[transaccion["id"]] = transaccion
        return transaccion

    def _cambiar_estado(self, transaccion: dict[str, Any], evento: str) -> None:
        estado: EstadoTransaccion = transaccion["_estado"]
        siguiente = estado.transicionar(evento)
        transaccion["_estado"] = siguiente
        self._sujeto.cambiar_estado(transaccion, siguiente.nombre)

    def _completar(self, transaccion: dict[str, Any]) -> None:
        self._cambiar_estado(transaccion, "autorizar")
        self._cambiar_estado(transaccion, "procesar")
        self._cambiar_estado(transaccion, "completar")

    def _rechazar(
        self, transaccion: dict[str, Any], cuenta: Cuenta
    ) -> dict[str, Any]:
        self._cambiar_estado(transaccion, "rechazar")
        cuenta.historial.append(transaccion)
        return transaccion

    def _revertir_saldo(
        self,
        transaccion: dict[str, Any],
        origen: Cuenta,
        destino: Cuenta | None,
    ) -> None:
        self._reversores[transaccion["tipo"]](transaccion, origen, destino)

    @staticmethod
    def _revertir_deposito(
        transaccion: dict[str, Any], origen: Cuenta, destino: Cuenta | None
    ) -> None:
        del destino
        origen.saldo -= transaccion["monto"] - transaccion["comision"]

    @staticmethod
    def _revertir_retiro(
        transaccion: dict[str, Any], origen: Cuenta, destino: Cuenta | None
    ) -> None:
        del destino
        origen.saldo += transaccion["monto"]

    @staticmethod
    def _revertir_transferencia(
        transaccion: dict[str, Any], origen: Cuenta, destino: Cuenta | None
    ) -> None:
        if destino is None:
            return
        origen.saldo += transaccion["monto"]
        destino.saldo -= transaccion["monto"]
        origen.transferido_hoy -= transaccion["monto"]


__all__ = ["BancoFacade"]
