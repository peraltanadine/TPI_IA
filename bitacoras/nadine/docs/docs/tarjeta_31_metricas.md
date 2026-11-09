# Tarjeta 31 · Métricas

Fecha: 2026-11-06  
`docs/technical.md` §6.2 no está en el proyecto.

## Estado

Cerrada. La función está en la celda de métricas de la sección 4: `metricas(y_true, y_pred, y_proba=None, clases=None)`. La comparación principal es `METRICA_COMPARACION = "f1_macro"`.

Devuelve un `dict` de floats, sin NaN:

| Clave | Cuándo |
|---|---|
| `accuracy` | siempre |
| `precision_macro`, `precision_weighted` | siempre |
| `recall_macro`, `recall_weighted` | siempre |
| `f1_macro`, `f1_weighted` | siempre |
| `roc_auc` | binario, si hay `y_proba` |
| `roc_auc_macro`, `roc_auc_weighted` | tres o más clases, si hay `y_proba` |

`zero_division=0` en precision, recall y F1. Si una clase no aparece en `y_pred`, esa clase aporta 0 y sklearn no avisa. Si el ROC-AUC no se puede calcular (por ejemplo una sola clase en `y_true`), la función avisa y no mete NaN.

Sirve para binario y para multiclase: el ramo de ROC mira cuántas columnas tiene `y_proba`. No hay nombres de clase escritos adentro. Los vectores de prueba fijos (`"a"`/`"b"` y las clases 0, 1, 2) se sacaron de la sección 4 para que la corrida use solo `df`. Esos casos ya habían pasado: el multiclase con una clase nunca predicha no dejó NaN ni warning de división.

## Decisión

La comparación principal entre DT y RF es `f1_macro`. Macro y weighted se siguen calculando las dos. Weighted y accuracy no eligen al ganador.

En la celda de la sección 4 la constante es `METRICA_COMPARACION = "f1_macro"`. El mismo texto está en `informe/seccion3.md`, sección 3.7.
