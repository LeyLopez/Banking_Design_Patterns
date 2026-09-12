import pytest

from src.dominio.estados import (
    EstadoAutorizada,
    EstadoCompletada,
    EstadoCreada,
    EstadoProcesada,
    EstadoRechazada,
    EstadoReversada,
    TransicionInvalidaError,
)


def test_flujo_exitoso_hasta_completada():
    estado = EstadoCreada()

    estado = estado.transicionar("autorizar")
    assert isinstance(estado, EstadoAutorizada)
    estado = estado.transicionar("procesar")
    assert isinstance(estado, EstadoProcesada)
    estado = estado.transicionar("completar")

    assert isinstance(estado, EstadoCompletada)
    assert estado.nombre == "COMPLETADA"


def test_transaccion_completada_puede_reversarse_una_vez():
    estado = EstadoCompletada().transicionar("reversar")

    assert isinstance(estado, EstadoReversada)
    assert estado.nombre == "REVERSADA"


def test_reversar_dos_veces_lanza_error_de_dominio():
    estado = EstadoCompletada().transicionar("reversar")

    with pytest.raises(TransicionInvalidaError):
        estado.transicionar("reversar")


def test_rechazo_desde_creada_es_valido_y_es_terminal():
    estado = EstadoCreada().transicionar("rechazar")

    assert isinstance(estado, EstadoRechazada)
    with pytest.raises(TransicionInvalidaError):
        estado.transicionar("autorizar")


def test_transicion_no_permitida_desde_creada_lanza_error():
    with pytest.raises(TransicionInvalidaError):
        EstadoCreada().transicionar("completar")
