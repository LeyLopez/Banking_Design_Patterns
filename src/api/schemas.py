"""Esquemas Pydantic de la API bancaria."""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


Canal = Literal["tarjeta", "pse", "billetera"]


class DepositoRequest(BaseModel):
    cuenta_id: str
    monto: Decimal = Field(gt=0)
    canal: Canal = "tarjeta"


class RetiroRequest(BaseModel):
    cuenta_id: str
    monto: Decimal = Field(gt=0)


class TransferenciaRequest(BaseModel):
    origen_id: str
    destino_id: str
    monto: Decimal = Field(gt=0)


class ReversoRequest(BaseModel):
    transaccion_id: str


class OperacionResponse(BaseModel):
    id: str
    tipo: str
    cuenta_id: str
    destino_id: str | None = None
    monto: Decimal
    canal: str
    comision: Decimal
    estado: str
