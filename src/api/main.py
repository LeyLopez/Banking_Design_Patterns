"""API FastAPI mínima para delegar operaciones en BancoFacade."""

from collections.abc import Callable
from decimal import Decimal
from typing import Any

from fastapi import FastAPI, HTTPException

from src.aplicacion.banco_facade import BancoFacade
from src.api.schemas import (
    DepositoRequest,
    OperacionResponse,
    ReversoRequest,
    RetiroRequest,
    TransferenciaRequest,
)
from src.dominio.cuentas import Cuenta, CuentaRepository
from src.dominio.estados import TransicionInvalidaError


app = FastAPI(title="Sistema Bancario Simplificado")


def _crear_facade_demo() -> BancoFacade:
    """Crea cuentas sintéticas para probar la API desde Swagger."""
    repository = CuentaRepository()
    repository.guardar(Cuenta("A-001", "Ana Demo", Decimal("1000.00")))
    repository.guardar(Cuenta("B-001", "Bruno Demo", Decimal("500.00")))
    return BancoFacade(repository)


facade = _crear_facade_demo()


def _serializar(transaccion: dict[str, Any]) -> OperacionResponse:
    return OperacionResponse(
        id=transaccion["id"],
        tipo=transaccion["tipo"],
        cuenta_id=transaccion["cuenta_id"],
        destino_id=transaccion.get("destino_id"),
        monto=transaccion["monto"],
        canal=transaccion["canal"],
        comision=transaccion["comision"],
        estado=transaccion["estado"],
    )


def _ejecutar(operacion: Callable[[], dict[str, Any]]) -> OperacionResponse:
    try:
        return _serializar(operacion())
    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=f"Recurso no encontrado: {error.args[0]}",
        ) from error
    except TransicionInvalidaError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.post("/depositar", response_model=OperacionResponse)
def depositar(request: DepositoRequest) -> OperacionResponse:
    """Delega un depósito en BancoFacade."""
    return _ejecutar(
        lambda: facade.depositar(request.cuenta_id, request.monto, request.canal)
    )


@app.post("/retirar", response_model=OperacionResponse)
def retirar(request: RetiroRequest) -> OperacionResponse:
    """Delega un retiro en BancoFacade."""
    return _ejecutar(lambda: facade.retirar(request.cuenta_id, request.monto))


@app.post("/transferir", response_model=OperacionResponse)
def transferir(request: TransferenciaRequest) -> OperacionResponse:
    """Delega una transferencia en BancoFacade."""
    return _ejecutar(
        lambda: facade.transferir(
            request.origen_id, request.destino_id, request.monto
        )
    )


@app.post("/reversar", response_model=OperacionResponse)
def reversar(request: ReversoRequest) -> OperacionResponse:
    """Delega un reverso en BancoFacade."""
    return _ejecutar(lambda: facade.reversar(request.transaccion_id))
