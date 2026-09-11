"""Interfaces del dominio para los patrones de la Fase 4."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class ComisionStrategy(ABC):
    """Contrato Strategy para encapsular el cálculo de una comisión.

    Cada estrategia concreta calcula la comisión de un canal u operación.
    El algoritmo puede intercambiarse en tiempo de ejecución sin modificar
    el flujo principal del banco.
    """

    @abstractmethod
    def calcular(self, monto: Decimal) -> Decimal:
        """Devuelve la comisión correspondiente al monto recibido."""
        raise NotImplementedError


class ProveedorExternoPort(ABC):
    """Contrato Adapter para unificar proveedores externos simulados.

    El núcleo bancario depende de este puerto y no de clases concretas de
    tarjeta, PSE o billetera. Las implementaciones futuras serán fakes y
    podrán sustituirse, incluido un fake que simule un fallo, sin cambiar
    la lógica del banco.
    """

    @abstractmethod
    def procesar(self, monto: Decimal) -> bool:
        """Procesa el monto con un proveedor fake y reporta si tuvo éxito."""
        raise NotImplementedError


class EstadoTransaccion(ABC):
    """Contrato State para encapsular estados y transiciones de transacción.

    Cada estado concreto conocerá las transiciones permitidas desde su
    posición. Así se evita mantener condicionales dispersos y se pueden
    rechazar explícitamente las transiciones inválidas.
    """

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Devuelve el nombre legible del estado actual."""
        raise NotImplementedError

    @abstractmethod
    def transicionar(self, evento: str) -> "EstadoTransaccion":
        """Aplica un evento y devuelve el siguiente estado permitido."""
        raise NotImplementedError


class ObservadorTransaccion(ABC):
    """Contrato Observer para reaccionar a cambios de una transacción.

    Los observadores concretos podrán notificar por consola o registrar
    auditoría sin mezclar esas responsabilidades con el procesamiento de
    la transacción.
    """

    @abstractmethod
    def actualizar(self, transaccion: Any) -> None:
        """Reacciona a una transacción cuyo estado ha cambiado."""
        raise NotImplementedError
