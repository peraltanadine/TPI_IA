# 4. Metodología

## 4.1 Esquema anti-fuga

Se elige la opción A: un holdout final. No se usa validación cruzada anidada.

El dataset cargado se parte una sola vez, de forma estratificada, en 80% de entrenamiento y 20% de holdout, con `random_state=SEED`. En el respaldo son 455 y 114 filas. Los barridos de hiperparámetros (E2–E4 y E6–E7) y el `cv` de 25 particiones, cuando se usen para elegir un hiperparámetro, reciben solo el entrenamiento. El holdout no entra en esos bucles.

Cada modelo se ajusta en el entrenamiento y se predice el holdout una vez. El resultado se guarda en `figuras/holdout_final.json`. Si se vuelve a correr la celda con el mismo dataset, no se reentrena: se lee ese archivo.

| | accuracy | f1_macro | roc_auc |
|---|---|---|---|
| DecisionTreeC45 | 0,9298 | 0,9246 | 0,9246 |
| RandomForestWrap | 0,9737 | 0,9713 | 0,9929 |

La métrica de comparación es `f1_macro`. En este corte el bosque queda arriba.

Las tablas 2 y 5 y las figuras 7 y 9 se calcularon antes de fijar este corte, sobre todas las filas. Describen el comportamiento de los modelos. No son la evaluación final.
