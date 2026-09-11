"""Estados concretos y transiciones de una transacción."""

from src.dominio.contratos import EstadoTransaccion


class TransicionInvalidaError(Exception):
    """Indica que un evento no está permitido en el estado actual."""


def _transicion_invalida(estado: str, evento: str) -> TransicionInvalidaError:
    return TransicionInvalidaError(
        f"No se puede aplicar '{evento}' desde el estado '{estado}'"
    )


class EstadoCreada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "CREADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        if evento == "autorizar":
            return EstadoAutorizada()
        if evento == "rechazar":
            return EstadoRechazada()
        raise _transicion_invalida(self.nombre, evento)


class EstadoAutorizada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "AUTORIZADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        if evento == "procesar":
            return EstadoProcesada()
        if evento == "rechazar":
            return EstadoRechazada()
        raise _transicion_invalida(self.nombre, evento)


class EstadoProcesada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "PROCESADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        if evento == "completar":
            return EstadoCompletada()
        if evento == "reversar":
            return EstadoReversada()
        raise _transicion_invalida(self.nombre, evento)


class EstadoCompletada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "COMPLETADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        if evento == "reversar":
            return EstadoReversada()
        raise _transicion_invalida(self.nombre, evento)


class EstadoRechazada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "RECHAZADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        raise _transicion_invalida(self.nombre, evento)


class EstadoReversada(EstadoTransaccion):
    @property
    def nombre(self) -> str:
        return "REVERSADA"

    def transicionar(self, evento: str) -> EstadoTransaccion:
        raise _transicion_invalida(self.nombre, evento)


__all__ = [
    "EstadoCreada",
    "EstadoAutorizada",
    "EstadoProcesada",
    "EstadoCompletada",
    "EstadoRechazada",
    "EstadoReversada",
    "TransicionInvalidaError",
]
