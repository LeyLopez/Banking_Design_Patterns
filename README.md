# Resumen del proyecto

## Proposito

Este proyecto implementa una API educativa de un sistema bancario simplificado. Permite depositar, retirar, transferir y reversar operaciones usando cinco patrones GoF: Strategy, Adapter, State, Observer y Facade.

## Alcance

- Cuentas en memoria con saldos `Decimal`.
- Comisiones intercambiables por canal.
- Proveedores externos exclusivamente fake.
- Limite diario de transferencias.
- Estados de transaccion y reverso unico.
- Notificaciones de consola y auditoria.
- API FastAPI con endpoints para las operaciones principales.

## Casos de uso

| Caso | Resultado |
|---|---|
| Depositar | Acredita el monto neto de comision despues de procesar el canal fake. |
| Retirar | Descuenta el monto si existe saldo suficiente. |
| Transferir | Mueve dinero entre cuentas y valida el limite diario. |
| Reversar | Deshace una operacion completada una sola vez. |

## Proposito academico

El codigo `before/` contiene problemas a los cuales se les realiza un diagnostica. El codigo `src/` muestra la refactorizacion y sus pruebas. La API y la documentacion sirven como apoyo para una sustentacion de 10 a 15 minutos.

## Fuera de alcance

No es un sistema financiero de produccion. No incluye persistencia real, autenticacion, multi-moneda, concurrencia distribuida ni integraciones externas reales.

## Dependencias

La ejecucion requiere las dependencias de `requirements.txt`. Los proveedores y datos de pago son sinteticos; no se almacenan numeros completos de tarjeta, CVV, tokens ni credenciales.
