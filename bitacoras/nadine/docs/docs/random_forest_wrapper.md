# Wrapper de Random Forest

Fecha: 2026-11-06  
Notebook: `TPI_Inteligencia_Artificial.ipynb` (sección 4, celda del wrapper)  
Informe: `informe/seccion3.md`

## Qué pedía la tarea

Envolver `sklearn.ensemble.RandomForestClassifier` con la misma interfaz que el árbol propio, para que los dos pasen por el mismo código de evaluación.

Parámetros: `n_estimators`, `max_depth`, `max_features`, `min_samples_leaf`, `bootstrap`, `random_state=SEED`.

La consigna lo permite. Hay que citar textualmente, en la sección 3 del informe, la frase del PDF: el RF puede ser un modelo de Scikit-learn.

Se cierra cuando:

- corre sobre el dataset;
- tiene `fit`, `predict`, `predict_proba` y `score` como el DT;
- la cita está en el informe.

## Qué ya estaba hecho

En la celda de la sección 4 ya existía la clase `RandomForestWrap`.

- Delegaba el aprendizaje en `RandomForestClassifier`.
- Recibía los seis parámetros, con `random_state=SEED`.
- Tenía `fit`, `predict`, `predict_proba` y `score`.
- Imputaba numéricas con la mediana y categóricas con la moda más one-hot, para datasets mixtos.
- Traía un smoke test de juguete y otro con el dataset del notebook (holdout 80/20 estratificado).

Eso cubría el esqueleto, pero no los tres criterios tal como quedó el árbol después.

## Qué faltaba

1. **La firma no era la del DT que se evalúa.**  
   El wrapper usaba `fit(df, target)`, `predict(df)` y `score(df, y=None)`, copiando al `ArbolC45` mínimo. Ese árbol no tiene `predict_proba` ni `score`. El que sí tiene los cuatro métodos es `DecisionTreeC45`, y su firma es otra: `fit(X, y)`, `predict(X)`, `predict_proba(X)`, `score(X, y)`. Una función de evaluación no podía llamar a los dos igual.

2. **No había corrida verificada en este proyecto.**  
   La celda estaba escrita, con `execution_count` vacío. El dataset de respaldo es Breast Cancer (569 filas, 30 atributos numéricos) porque `data/dataset.csv` no está.

3. **La cita no estaba en el informe de este directorio.**  
   `docs/technical.md` §5 no está en el repo (tampoco en la copia `Desktop/TPI_IA`). El PDF sí: `Desktop/TPI_IA/TP-IA-2026.pdf`, sección «Random Forest» y la aclaración de la descripción del problema. En este workspace no había carpeta `informe/`.

`evaluate`, la tabla E1 y la poda E5 siguen como TODO de la misma sección. No forman parte del cierre de este wrapper.

## Qué se cambió y por qué

### Notebook, celda del wrapper

`RandomForestWrap` ahora hereda `ClassifierMixin` y `BaseEstimator`, igual que `DecisionTreeC45`.

- `fit(X, y)`: `X` es un DataFrame de atributos, `y` el vector clase. Misma comprobación de tipo y de largo que el árbol.
- `predict(X)` y `predict_proba(X)` alinean las columnas a las vistas en el entrenamiento.
- `score(X, y, sample_weight=None)` devuelve accuracy con la misma firma que `ClassifierMixin.score`.
- Los seis parámetros se guardan en `__init__` sin lógica extra, así `get_params` sirve para el mismo estilo de búsqueda que el árbol.
- El preprocesamiento sigue adentro del wrapper. Quien evalúa pasa las columnas crudas a los dos modelos; no arma un one-hot aparte solo para el bosque.
- El smoke test separa `X` e `y` y, si `DecisionTreeC45` ya está definido, comprueba que los cuatro métodos existan en las dos clases.
- El holdout del dataset real usa el mismo contrato.

La sección 4 del notebook apunta a la cita y a esta interfaz. El texto anterior decía que el RF de sklearn está permitido, pero no dejaba la frase del PDF ni la firma real.

### Informe

Se creó `informe/seccion3.md`. Es la sección 3 («Descripción de la solución implementada»). Incluye la aclaración completa del PDF, con la grafía original «libraría», y la cláusula «para el algoritmo RF se podrá utilizar un modelo de la libraría Scikit-learn». También explica el cambio de `fit(df, target)` a `fit(X, y)`.

## Verificación

Se ejecutaron la carga del notebook y la celda del wrapper con scikit-learn 1.6.1 (la misma versión que imprime el setup). No hay `data/dataset.csv`, así que corre el respaldo Breast Cancer, igual que la celda 1.2.

| Prueba | Resultado |
|---|---|
| Toy mixto: `temp` numérica, `clima` y `viento` categóricas | OK. Accuracy 1.00. `num_cols=['temp']`, `cat_cols=['clima','viento']` |
| `predict_proba` suma 1 por fila | OK |
| `get_params` incluye los seis parámetros y `random_state=42` | OK |
| Breast Cancer, 569×31, holdout 80/20 estratificado, 100 árboles | OK. Train 455 / test 114. 30 numéricas, 0 categóricas. Accuracy **0.9737**. `predict_proba` (114, 2). Clases: benign, malignant |
| Segunda corrida con la misma semilla | Misma accuracy |
| Función única `evaluar(modelo, X_train, y_train, X_test, y_test)` con `fit`, `predict`, `predict_proba` y `score` | OK sobre `RandomForestWrap` |

## Qué no se tocó

- No se implementó `evaluate`, ni E1, ni E5.
- No se modificó `DecisionTreeC45`.
- No se inventó `docs/technical.md`: no está en el proyecto.
