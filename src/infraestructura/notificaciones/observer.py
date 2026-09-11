"""Implementaciones del patrón Observer para transacciones."""

import logging
from typing import Any

from src.dominio.contratos import ObservadorTransaccion


class SujetoTransaccion:
    """Mantiene observadores y publica cambios de estado de una transacción."""

    def __init__(self) -> None:
        self._observadores: list[ObservadorTransaccion] = []

    def suscribir(self, observador: ObservadorTransaccion) -> None:
        """Agrega un observador sin duplicar la suscripción."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: ObservadorTransaccion) -> None:
        """Retira un observador suscrito."""
        if observador in self._observadores:
            self._observadores.remove(observador)

    def cambiar_estado(self, transaccion: dict[str, Any], nuevo_estado: str) -> None:
        """Cambia el estado y notifica a todos los observadores suscritos."""
        transaccion["estado"] = nuevo_estado
        self.notificar(transaccion)

    def notificar(self, transaccion: dict[str, Any]) -> None:
        """Entrega la transacción actualizada a cada observador."""
        for observador in self._observadores:
            observador.actualizar(transaccion)


class NotificadorConsola(ObservadorTransaccion):
    """Notifica por consola el estado actualizado de una transacción."""

    def actualizar(self, transaccion: Any) -> None:
        print(
            f"Notificacion de transaccion {transaccion['id']}: "
            f"estado {transaccion['estado']}"
        )


class AuditoriaLogger(ObservadorTransaccion):
    """Registra en logging los cambios de estado de una transacción."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def actualizar(self, transaccion: Any) -> None:
        self.logger.info(
            "Transaccion %s cambio a estado %s",
            transaccion["id"],
            transaccion["estado"],
        )


__all__ = ["SujetoTransaccion", "NotificadorConsola", "AuditoriaLogger"]
