# Diagramas UML con PlantUML

Los diagramas PlantUML reflejan las clases y el flujo reales de `src/`.

## Fuentes PlantUML

- `clases_dominio.puml`: clases del dominio y los cinco patrones.
- `clases_capas.puml`: dependencias entre API, aplicacion, dominio e infraestructura.
- `secuencia_deposito_exitoso.puml`: flujo exitoso de deposito.
- `secuencia_retiro_rechazado.puml`: flujo de retiro rechazado por saldo insuficiente.

Con PlantUML instalado y disponible en el `PATH`, renderizar todos los diagramas:

```powershell
plantuml diagrams/*.puml
```

Para generar SVG en lugar de PNG:

```powershell
plantuml -tsvg diagrams/*.puml
```

Tambien se puede usar Java con el JAR de PlantUML:

```powershell
java -jar plantuml.jar diagrams/*.puml
```

Los archivos `.dot` se conservan como la version Graphviz anterior.

## Diagramas Graphviz heredados

Renderizar el diagrama de clases:

```powershell
dot -Tpng diagrams/clases_dominio.dot -o diagrams/clases_dominio.png
```

Renderizar la secuencia de depósito exitoso:

```powershell
dot -Tpng diagrams/secuencia_deposito_exitoso.dot -o diagrams/secuencia_deposito_exitoso.png
```

También se puede generar SVG sustituyendo `-Tpng` por `-Tsvg` y cambiando la extensión de salida.
