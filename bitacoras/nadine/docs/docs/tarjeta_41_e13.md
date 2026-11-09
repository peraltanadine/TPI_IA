# Tarjeta 41 · E13, matrices de confusión

Fecha: 2026-11-06  
`docs/informe-lncs.md` no está. La figura es la Fig. 9.

## Estado

Cerrada. `figura_confusion_roc` arma `plt.subplots(1, n)` y dibuja con `ConfusionMatrixDisplay.from_estimator`. Si hay dos clases, `normalize="true"`: cada fila suma 1 y se ve el porcentaje de error de esa clase. Los conteos TN/FP/FN/TP siguen en la celda y en `figuras/tabla_tn_fp_fn_tp.csv`.

Holdout 80/20 del respaldo, `random_state=SEED`. Positiva: la segunda clase del archivo, `malignant`. 72 benign y 42 malignant en el test.

| | Error en benign | Error en malignant |
|---|---|---|
| DecisionTreeC45 | 5,6% (4 de 72) | 9,5% (4 de 42) |
| RandomForestWrap | 0% (0 de 72) | 7,1% (3 de 42) |

El árbol reparte el error en las dos clases. El bosque no marca ningún benign como malignant: los tres errores son malignant que deja pasar. El texto está en `informe/seccion3.md`, sección 3.6, y en el markdown de la Fig. 9 del notebook. La imagen es `figuras/fig9_matrices_confusion.png`.
