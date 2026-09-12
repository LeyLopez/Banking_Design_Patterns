# Arquitectura

## Propósito

Explicar la separación real del proyecto en cuatro capas: dominio, aplicación, infraestructura y entrada API. La arquitectura mantiene el núcleo bancario independiente de FastAPI y de proveedores externos.

## Capas

```text
src/
├── dominio/
│   ├── contratos.py
│   ├── cuentas.py
│   └── estados/
├── aplicacion/
│   ├── banco_facade.py
│   └── comision_strategy.py
├── infraestructura/
│   ├── proveedores/
│   └── notificaciones/
└── api/
    ├── main.py
    └── schemas.py
```

### Dominio

Contiene `Cuenta`, `CuentaRepository`, los contratos abstractos y la máquina de estados. `EstadoCreada`, `EstadoAutorizada`, `EstadoProcesada`, `EstadoCompletada`, `EstadoRechazada` y `EstadoReversada` conocen sus transiciones permitidas.

### Aplicación

`BancoFacade` es el punto de entrada de los casos de uso `depositar`, `retirar`, `transferir` y `reversar`. Coordina repositorio, estrategias, adapters, estados y observadores. `comision_strategy.py` contiene `ComisionTarjeta`, `ComisionPSE` y `ComisionBilletera`.

### Infraestructura

`proveedores/adapters.py` contiene `TarjetaAdapter`, `PSEAdapter` y `BilleteraAdapter`, todos fake. `notificaciones/observer.py` contiene `SujetoTransaccion`, `NotificadorConsola` y `AuditoriaLogger`.

### Entrada

`api/main.py` expone los cuatro endpoints POST y delega en `BancoFacade`. `api/schemas.py` valida los DTO con Pydantic y `Decimal`.

## Inyección de dependencias

`BancoFacade` recibe opcionalmente `CuentaRepository`, registros de `ComisionStrategy`, registros de `ProveedorExternoPort` y `SujetoTransaccion` en su constructor. En las pruebas, por ejemplo, se inyecta un repositorio en memoria y un fake de proveedor sin cambiar la Facade.

## Dependencias

Depende de `domain-knowledge.md` y `patterns-decision-record.md`.

## Límites

La persistencia es en memoria. No hay base de datos, autenticación, despliegue ni llamadas HTTP reales.
