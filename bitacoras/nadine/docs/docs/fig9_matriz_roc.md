# Card 32 · Matriz de confusión y ROC-AUC

Fecha: 2026-11-06

## ¿Se puede hacer?

Sí. El bloqueo viejo era que el árbol no tenía `predict_proba`. Eso ya está: `DecisionTreeC45.predict_proba` y `RandomForestWrap.predict_proba` devuelven una matriz `(n_filas, n_clases)` en el orden de `classes_`.

## Qué había

- `metricas()` y `evaluar_cv` ya calculan un ROC-AUC numérico si reciben probabilidades. No dibujan la matriz ni la curva.
- La EDA usa `sns.heatmap` para la correlación, no para la confusión.
- No existían la Fig. 9 ni la Fig. 10.

## Cómo quedó

Celda nueva, después del protocolo de CV, para no repetir las 25 particiones.

1. Holdout estratificado 80/20, `random_state=SEED`, el mismo para los dos modelos.
2. `orden_clases = list(árbol.classes_)`. Si el bosque trae otro orden, `proba_en_orden` reordena sus columnas.
3. Ningún nombre de clase está escrito en la función. Con 2 clases, la positiva es `classes_[1]` y las celdas de la Fig. 9 son TN, FP, FN y TP. Con 3 o más, la matriz usa los nombres del dataset y `tabla_tn_fp_fn_tp` calcula TN, FP, FN y TP de cada clase contra el resto. El resultado va a `figuras/tabla_tn_fp_fn_tp.csv`.
4. ROC-AUC:
   - 3 o más clases: `roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro", labels=orden)`.
   - 2 clases: sklearn responde `ValueError` si `y_proba` tiene dos columnas. Se promedia el AUC one-vs-rest de cada clase. En binario ese promedio es el AUC de la clase positiva.
5. Fig. 10: una curva por clase, en los dos modelos.

Un assert con tres clases comprueba que la función coincide con la firma de la tarjeta.

## Corrida de ejemplo

La sección 4 ya no trae filas ni nombres de clase escritos a mano. Esta corrida usa el `df` cargado (el respaldo, porque no hay `data/dataset.csv`) y `DecisionTreeC45(random_state=SEED)`, sin tope de profundidad. La segunda clase de ese archivo resulta malignant.

| Modelo | TN | FP | FN | TP |
|---|---|---|---|---|
| DecisionTreeC45 | 68 | 4 | 4 | 38 |
| RandomForestWrap | 72 | 0 | 3 | 39 |

ROC-AUC macro del holdout: árbol 0,9246, bosque 0,9929.

Archivos: `figuras/fig9_matrices_confusion.png`, `figuras/fig10_roc_por_clase.png`. El texto para el informe está en `informe/seccion3.md`, sección 3.6.

El ROC-AUC de la validación repetida (sección 3.5) es otra cuenta: media de 25 folds, no este holdout.
