# Diagnóstico del código antes

Este diagnóstico analiza `before/banking_before.py` tal como fue generado. Las referencias de línea corresponden a las 175 líneas reales del archivo.

| Archivo | Línea exacta | Problema | Smell o SOLID afectado | Consecuencia |
|---|---:|---|---|---|
| `before/banking_before.py` | 34, 38 | `saldo_inicial` se convierte y almacena como `float`. | Bug de precisión financiera; primitive obsession | Las operaciones monetarias pueden acumular errores de representación binaria y producir saldos inesperados. |
| `before/banking_before.py` | 44–55 | `depositar` construye manualmente un diccionario de transacción, administra el consecutivo, registra la transacción y delega el procesamiento. | SRP; datos sin encapsulamiento | La operación depende de la estructura interna del diccionario y cualquier cambio en el flujo obliga a modificar `Banco`. |
| `before/banking_before.py` | 49 | El monto del depósito se convierte a `float`. | Bug de precisión financiera; primitive obsession | Un monto como `0.1` puede participar en cálculos cuyo resultado no coincide exactamente con el valor decimal esperado. |
| `before/banking_before.py` | 57–68 | `retirar` mezcla la creación y registro de la transacción con el envío al procesamiento central. | SRP; alto acoplamiento | Cambiar la forma de registrar o procesar un retiro afecta directamente la clase `Banco`. |
| `before/banking_before.py` | 62 | El monto del retiro se convierte a `float`. | Bug de precisión financiera; primitive obsession | La comparación contra el saldo y el cálculo del total pueden sufrir errores de redondeo. |
| `before/banking_before.py` | 70–82 | `transferir` crea y registra una transacción mediante un diccionario y delega todo el flujo a `Banco`. | SRP; alto acoplamiento | La clase concentra la construcción, validación, autorización y ejecución de transferencias. |
| `before/banking_before.py` | 76 | El monto de la transferencia se convierte a `float`. | Bug de precisión financiera; primitive obsession | Las transferencias acumuladas pueden dejar saldos con precisión inadecuada. |
| `before/banking_before.py` | 84–92 | La comisión se selecciona con `if/elif` según el canal (`tarjeta`, `pse`, `billetera`). | Violación de OCP | Agregar o cambiar un canal exige modificar el método existente y volver a probar todas las ramas. |
| `before/banking_before.py` | 85–92 | Las reglas de comisión están codificadas directamente dentro de `Banco`. | SRP; violación de OCP | `Banco` tiene una razón adicional para cambiar cada vez que cambia una tarifa o regla de comisión. |
| `before/banking_before.py` | 94–104 | `procesar_transaccion` calcula comisión, total y datos de la transacción además de coordinar validaciones y cambios de estado. | Violación de SRP | El método es difícil de probar por responsabilidad aislada y cualquier modificación puede afectar varias etapas del flujo. |
| `before/banking_before.py` | 106–112 | `Banco` instancia directamente `TarjetaProvider`, `PSEProvider` y `BilleteraProvider`. | Violación de DIP | No se puede sustituir un proveedor por otro fake o simular un fallo mediante inyección sin modificar `Banco`. |
| `before/banking_before.py` | 107–112 | La selección del proveedor también usa una cadena `if/elif` por canal. | Violación de OCP; acoplamiento a concretos | Cada nuevo proveedor requiere editar la lógica central y aumenta el número de ramas de `Banco`. |
| `before/banking_before.py` | 114–133 | El mismo método decide cómo validar depósitos, retiros y transferencias mediante condicionales por tipo de operación. | SRP; complejidad condicional | La lógica de operaciones distintas queda concentrada en un método largo y crece al añadir nuevos tipos. |
| `before/banking_before.py` | 45–51, 58–64, 71–79 | Los datos de la transacción y su estado se representan con diccionarios y strings sueltos. | Falta de encapsulamiento; primitive obsession | No existe un objeto que proteja invariantes ni un contrato que limite los valores posibles. |
| `before/banking_before.py` | 135–140 | Las transiciones se realizan comparando estados string con `==` y asignando el siguiente string. | Falta de encapsulamiento de estados; primitive obsession | Las transiciones válidas no están centralizadas ni protegidas; cualquier código podría asignar un estado arbitrario. |
| `before/banking_before.py` | 150–151 | El estado final también se cambia mediante comparación y asignación de strings. | Falta de encapsulamiento de estados | El flujo de estados está disperso y no modela explícitamente transiciones inválidas ni sus errores de dominio. |
| `before/banking_before.py` | 41 | `crear_cuenta` imprime una notificación como parte de la creación de la cuenta. | Acoplamiento entre negocio y presentación | Reutilizar la creación desde una API o interfaz distinta arrastra salida de consola innecesaria. |
| `before/banking_before.py` | 97–99, 116–118, 121–123, 127–129, 131–133 | Las rutas de rechazo imprimen directamente el resultado desde el procesamiento de negocio. | Acoplamiento entre lógica de negocio y presentación | La lógica no puede cambiar fácilmente de consola a API, log u otro observador. |
| `before/banking_before.py` | 153–157 | `procesar_transaccion` imprime la finalización y la notificación de saldo directamente. | Violación de SRP; acoplamiento negocio/presentación | La operación no está separada de su mecanismo de notificación y resulta difícil reutilizarla sin `print`. |
| `before/banking_before.py` | 35–40, 45–52, 58–65, 71–79 | Cuentas y transacciones se modelan como diccionarios con claves string. | Primitive obsession; falta de encapsulamiento | Los errores de clave o de estructura solo aparecen en tiempo de ejecución y las invariantes no pertenecen a una entidad. |
| `before/banking_before.py` | 95–158 | Un único método concentra búsqueda de cuenta, comisión, proveedores, validación, estados, movimiento de dinero, historial y notificaciones. | Violación de SRP; alta complejidad; acoplamiento general | El método tiene múltiples razones para cambiar y es el principal punto de riesgo al refactorizar. |

## Resumen de problemas frente a la Fase 3

- `float` para dinero: líneas 38, 49, 62 y 76.
- `procesar_transaccion` con responsabilidades mezcladas: líneas 94–158.
- `if/elif` por canal para comisiones: líneas 84–92.
- Estados como strings comparados con `==`: líneas 135–151, además de su creación en 45–52, 58–65 y 71–79.
- Notificaciones con `print` dentro de la lógica: líneas 97–99, 116–123, 127–133 y 153–157.
- Instanciación directa de proveedores concretos: líneas 106–112.
