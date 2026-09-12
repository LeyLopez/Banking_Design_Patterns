import pytest

from src.dominio.contratos import (
    ComisionStrategy,
    EstadoTransaccion,
    ObservadorTransaccion,
    ProveedorExternoPort,
)


@pytest.mark.parametrize(
    "contrato",
    [
        ComisionStrategy,
        ProveedorExternoPort,
        EstadoTransaccion,
        ObservadorTransaccion,
    ],
)
def test_los_contratos_no_se_pueden_instanciar_directamente(contrato):
    with pytest.raises(TypeError):
        contrato()
