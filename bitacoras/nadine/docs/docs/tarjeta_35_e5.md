# Tarjeta 35 · E5, DT con y sin poda

Fecha: 2026-11-06  
`docs/technical.md` §4 y `docs/cards/sprint-3.md` (card 28) no están en el proyecto.

## Estado

Cerrada. `construir_tabla5` ajusta `DecisionTreeC45(pruning=False)` y `DecisionTreeC45(pruning=True, pruning_confidence=0.25)` en las 25 particiones del `cv` compartido. Si la media de nodos con poda superara a la de sin poda, la función no escribe la tabla.

| | sin poda | con poda |
|---|---|---|
| nodos | 47,64 ± 5,96 | 30,68 ± 5,09 |
| hojas | 24,32 ± 2,98 | 15,84 ± 2,54 |
| altura | 13,20 ± 1,94 | 10,64 ± 2,23 |
| accuracy train | 1,0000 ± 0,0000 | 0,9902 ± 0,0058 |
| accuracy test | 0,9269 ± 0,0219 | 0,9304 ± 0,0204 |
| brecha | 0,0731 ± 0,0219 | 0,0598 ± 0,0215 |

El efecto es el esperado: el árbol podado es más chico, la accuracy de prueba sube un poco y la brecha baja. Sin poda coincide con el DT de la Tabla 2. El LaTeX está en `figuras/tabla5_poda.tex` y la discusión en `informe/seccion3.md`, sección 3.9.

La impresión de clima y viento que queda en la celda de sklearn es un ejemplo de la API, no la Tabla 5.

## Prueba de una partición

Mismo holdout 80/20, `random_state=42`, dataset de respaldo. No es la Tabla 5.

| | sin poda | con poda |
|---|---|---|
| nodos | 53 | 31 |
| hojas | 27 | 16 |
| altura | 15 | 11 |
| accuracy train | 1,0000 | 0,9890 |
| accuracy test | 0,9298 | 0,9211 |
| brecha | 0,0702 | 0,0680 |

Esa partición sola bajaba la accuracy de prueba (0,9298 a 0,9211). En las 25 particiones la media sube. Por eso la Tabla 5 no se arma con un solo corte.
