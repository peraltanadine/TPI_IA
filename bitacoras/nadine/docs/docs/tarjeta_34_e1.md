# Tarjeta 34 · E1, tabla comparativa DT vs RF

Fecha: 2026-11-06  
`docs/technical.md` §7 y `docs/informe-lncs.md` no están en el proyecto.

## ¿Se puede hacer?

Sí. El protocolo de la tarjeta 33 ya entrena los dos modelos sobre el mismo `cv` y el mismo `df`. Falta armar la Tabla 2 y la Fig. 4 con esos 25 valores, y sumar tiempo y tamaño, que hoy se calculan y se descartan.

## Estado

Cerrada. `construir_tabla2` corre el `cv` compartido una vez por modelo, con `return_estimator=True`.

| Pedido | Resultado |
|---|---|
| Media ± desvío | 25 folds, métricas de test |
| Tiempos | `fit_time` y `score_time` (el de `score`, que llama a `predict`) |
| Tamaño | DT: nodos, hojas y altura del árbol propio. RF: suma de nodos y hojas de los 100 árboles; altura = la del más profundo |
| `to_latex()` | `figuras/tabla2_dt_vs_rf.tex` |
| Fig. 4 | `figuras/fig4_dt_vs_rf.png`, barras con el desvío |

En el respaldo, `f1_macro` es 0,9221 ± 0,0236 (DT) y 0,9530 ± 0,0251 (RF). El árbol tiene ~48 nodos y el bosque ~3513, pero el ajuste del árbol propio tarda ~26 s por fold y el del bosque ~0,19 s. La conclusión “DT rápido, RF lento” no se sostiene en este código: el contraste que sí aparece es el de tamaño. Los números están en `informe/seccion3.md`, sección 3.8.

## Qué hacer

1. Pedir los estimadores ajustados de cada fold con `return_estimator=True` en el mismo `cross_validate`. Son 25 árboles y 25 bosques. De cada uno se leen tiempo y tamaño, y después se resumen como media ± desvío. Un solo ajuste no alcanza: la tarjeta pide desvío.
2. Tiempos: `fit_time` y `score_time` de ese resultado. `score_time` es el costo de predecir el fold de test.
3. Tamaño del árbol, caminando `estimador.arbol_.raiz`:
   - nodos: `contar_nodos_arbol`;
   - hojas: nodos con `es_hoja`;
   - altura: profundidad máxima desde la raíz.
4. Tamaño del bosque, en `pipeline_.named_steps["rf"].estimators_`: sumar `tree_.node_count` y `tree_.n_leaves` de los 100 árboles, y tomar el máximo de `tree_.max_depth` como altura del bosque.
5. La Tabla 2 tiene una fila por métrica de test, más filas de `tiempo_fit`, `tiempo_predict`, `nodos`, `hojas` y `altura`. Columnas: media y desvío de DT, media y desvío de RF. La comparación que decide es `f1_macro` (`METRICA_COMPARACION`). El resto se muestra.
6. `tabla2.to_latex(...)` a `figuras/tabla2_dt_vs_rf.tex`.
7. Fig. 4: barras agrupadas DT vs RF, eje de las métricas de test, barra de error = desvío. Archivo fijo `figuras/fig4_dt_vs_rf.png`.

No se crea otro `RepeatedStratifiedKFold`. Se usa el `cv` compartido.
