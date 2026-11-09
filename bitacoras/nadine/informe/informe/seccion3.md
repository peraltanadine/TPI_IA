# 3. Descripción de la solución implementada

## 3.1 Alcance de esta sección

Esta sección describe cómo se resolvió la comparación entre el árbol de decisión propio y el Random Forest, y qué problema de interfaz hubo que cerrar para medirlos con el mismo protocolo.

## 3.2 Uso de Scikit-learn en Random Forest

El algoritmo de árbol de decisión se implementa en el equipo. Para el bosque, la consigna habilita un modelo de biblioteca. La aclaración del enunciado dice, de forma textual:

> «El algoritmo DT deberá ser íntegramente desarrollado por el equipo, para el algoritmo RF se podrá utilizar un modelo de la libraría Scikit-learn.»

La cláusula que autoriza el ensamble es:

> «para el algoritmo RF se podrá utilizar un modelo de la libraría Scikit-learn»

Se conserva la grafía «libraría» porque así figura en `TP-IA-2026.pdf`.

En la solución, ese modelo es `sklearn.ensemble.RandomForestClassifier`, encapsulado en la clase `RandomForestWrap`. No se reimplementa el bosque: el wrapper solo fija la parametrización pedida y traduce las entradas al formato numérico que exige Scikit-learn.

## 3.3 Interfaz común con el árbol

`DecisionTreeC45` entrena y predice con `fit(X, y)`, `predict(X)`, `predict_proba(X)` y `score(X, y)`, donde `X` es un DataFrame de atributos e `y` el vector de clase. `RandomForestWrap` expone esos mismos cuatro métodos, con la misma firma de `score(X, y, sample_weight=None)`.

Los hiperparámetros del wrapper son `n_estimators`, `max_depth`, `max_features`, `min_samples_leaf`, `bootstrap` y `random_state`. Este último queda en la semilla global `SEED`, de modo que dos corridas del bosque produzcan el mismo resultado.

Scikit-learn no acepta columnas categóricas en crudo. El wrapper imputa las numéricas con la mediana y las categóricas o booleanas con la moda, y aplica one-hot a estas últimas. Ese paso queda dentro de `fit` y `predict`: el código que compara los modelos entrega a ambos las mismas columnas originales y no arma una matriz distinta para cada algoritmo.

## 3.4 Problema encontrado

La primera versión del wrapper entrenaba con `fit(df, nombre_de_la_clase)`, la firma del árbol mínimo `ArbolC45`. El árbol que entra a la evaluación es `DecisionTreeC45`, que separa atributos y clase. Con esas dos firmas, una función `evaluate` no podía recibir los dos modelos. Se cambió el wrapper a `fit(X, y)` para que el protocolo sea uno solo.

## 3.5 Protocolo de medición

Los dos modelos se miden con un único validador, definido una sola vez en el setup del notebook:

`cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED)`

`SEED` vale 42. Cinco folds repetidos cinco veces dan 25 particiones. `RepeatedStratifiedKFold` arma cada fold manteniendo la proporción de clases. Eso importa con clases desbalanceadas: un fold sin estratificar puede quedar sin alguna clase y la métrica de ese fold deja de ser comparable. Sobre Breast Cancer (357 benign / 212 malignant) se comprobó que los 25 folds de test contienen las dos clases.

`evaluar_cv` llama a `cross_validate` con ese objeto. No construye otro splitter. Usa `n_jobs=-1` y `return_train_score=True`. La diferencia train − test es la brecha de sobreajuste. Las métricas son accuracy, precision, recall y F1 (macro y weighted) y ROC-AUC. Cada una queda con 25 valores de entrenamiento y 25 de prueba por modelo.

En scikit-learn 1.6 el splitter no guarda `n_splits` como atributo. El número de particiones se lee con `cv.get_n_splits()`, que devuelve 25.

La corrida de control usa el dataset cargado. Hoy es el respaldo (no hay `data/dataset.csv`): 569 filas y 30 atributos continuos. El árbol es `DecisionTreeC45(random_state=SEED)`, sin tope de profundidad ni hoja mínima distinta de la de la clase. El bosque es `RandomForestWrap` con sus parámetros por defecto (100 árboles, `max_features="sqrt"`, `bootstrap=True`, `random_state=SEED`). Ninguno de los dos recibe nombres de clase ni filas escritas en la sección 4.

Dos ejecuciones seguidas, con el mismo `random_state`, devolvieron las mismas 25 filas en las ocho métricas, para el árbol y para el bosque.

Media ± desvío en test, y brecha media (train − test):

| Modelo | Métrica | Test | Brecha |
|---|---|---|---|
| DecisionTreeC45 | accuracy | 0,9283 ± 0,0239 | 0,0174 |
| DecisionTreeC45 | f1_macro | 0,9210 ± 0,0269 | 0,0192 |
| DecisionTreeC45 | f1_weighted | 0,9271 ± 0,0246 | 0,0177 |
| DecisionTreeC45 | precision_macro | 0,9368 ± 0,0243 | 0,0202 |
| DecisionTreeC45 | precision_weighted | 0,9312 ± 0,0235 | 0,0176 |
| DecisionTreeC45 | recall_macro | 0,9114 ± 0,0293 | 0,0177 |
| DecisionTreeC45 | recall_weighted | 0,9283 ± 0,0239 | 0,0174 |
| DecisionTreeC45 | roc_auc | 0,9162 ± 0,0255 | 0,0161 |
| RandomForestWrap | accuracy | 0,9564 ± 0,0232 | 0,0436 |
| RandomForestWrap | f1_macro | 0,9530 ± 0,0251 | 0,0470 |
| RandomForestWrap | f1_weighted | 0,9562 ± 0,0234 | 0,0438 |
| RandomForestWrap | precision_macro | 0,9573 ± 0,0232 | 0,0427 |
| RandomForestWrap | precision_weighted | 0,9581 ± 0,0220 | 0,0419 |
| RandomForestWrap | recall_macro | 0,9511 ± 0,0277 | 0,0489 |
| RandomForestWrap | recall_weighted | 0,9564 ± 0,0232 | 0,0436 |
| RandomForestWrap | roc_auc | 0,9893 ± 0,0092 | 0,0107 |

El bosque llega a accuracy 1 en entrenamiento y baja a 0,9564 en test: la brecha es el dato que pide `return_train_score=True`. Esta tabla se midió con el árbol en `max_depth=2`. El código de la sección 4 ya no impone ese tope: usa `DecisionTreeC45(random_state=SEED)` sobre el `df` cargado.

## 3.6 Matrices de confusión y ROC-AUC

El procedimiento no nombra clases. Las toma de `classes_` del modelo entrenado, en el mismo orden que las columnas de `predict_proba`. Así sirve para el dataset de la cátedra cuando reemplace al respaldo: alcanza con cambiar `RUTA_DATOS` y `TARGET_COL`.

Con dos clases, la segunda columna es la positiva. Es la convención de scikit-learn, no una clase elegida en el código. Si en el dataset oficial la positiva es otra, se pasa `clase_positiva` y esa clase pasa al final del orden, junto con su columna de `predict_proba`. La matriz se lee así:

| | Predicho negativo | Predicho positivo |
|---|---|---|
| Verdadero negativo | TN | FP |
| Verdadero positivo | FN | TP |

Con tres o más clases no hay una sola positiva. La Fig. 9 usa los nombres reales, y TN, FP, FN y TP se calculan por clase contra el resto. Esa tabla se guarda en `figuras/tabla_tn_fp_fn_tp.csv`.

ROC-AUC usa `predict_proba`. Con tres o más clases la llamada es `roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro")`. Con dos clases scikit-learn rechaza esa firma sobre una matriz de dos columnas, y el macro es el promedio de una curva por clase. La Fig. 10 dibuja una curva por cada clase del dataset.

El ejemplo de abajo es el respaldo, porque `data/dataset.csv` todavía no está. Holdout estratificado 80/20, semilla 42. En ese archivo las clases salen del propio `df`. El árbol no tiene tope de profundidad: `DecisionTreeC45(random_state=SEED)`. El bosque usa sus parámetros por defecto.

La positiva de esta corrida es la segunda clase del archivo, `malignant`.

| Modelo | TN | FP | FN | TP |
|---|---|---|---|---|
| DecisionTreeC45 | 68 | 4 | 4 | 38 |
| RandomForestWrap | 72 | 0 | 3 | 39 |

En este holdout el ROC-AUC macro es 0,9246 para el árbol y 0,9929 para el bosque. No se compara con 0,9162 y 0,9893 de la sección 3.5: aquello es la media de 25 particiones con el árbol en profundidad 2, y esto es un solo holdout sin ese tope.

La Fig. 9 normaliza cada fila, así que el número de arriba es el porcentaje de esa clase real. En el test hay 72 benign y 42 malignant.

| | Error en benign | Error en malignant |
|---|---|---|
| DecisionTreeC45 | 5,6% (4 de 72) | 9,5% (4 de 42) |
| RandomForestWrap | 0% (0 de 72) | 7,1% (3 de 42) |

El árbol se equivoca en las dos clases, con la misma cantidad de casos (4 y 4). Como malignant es la clase chica, ese 9,5% pesa más que el 5,6% de benign. El bosque no marca ningún benign como malignant: sus tres errores son malignant que deja pasar. El patrón no es el mismo. El árbol reparte el error; el bosque lo concentra en la clase positiva.

Archivos: `figuras/fig9_matrices_confusion.png` y `figuras/fig10_roc_por_clase.png`.

## 3.7 Métricas

`metricas(y_true, y_pred, y_proba, clases)` devuelve un diccionario listo para una fila de tabla. Siempre incluye accuracy y precision, recall y F1 con `average="macro"` y con `average="weighted"`. Si llega `y_proba`, agrega ROC-AUC. `zero_division=0` pone 0 cuando una clase no se predice, en lugar de un NaN o un warning. Los nombres de clase no están en la función: los toma de `y` o del argumento `clases`.

Macro y weighted no se usan para lo mismo. Macro da el mismo peso a cada clase. Weighted pesa cada clase por cuántas filas tiene, así que la mayoritaria manda. Con desbalance hay que mostrar las dos.

Para decir cuál modelo gana se usa `f1_macro`: no deja que la clase grande tape el error en la chica. Accuracy queda como lectura auxiliar. Weighted se publica en la misma tabla y no decide el ganador. En el código esa elección es la constante `METRICA_COMPARACION`.

## 3.8 Tabla 2

La Tabla 2 resume las 25 particiones del `cv` compartido, sobre el dataset cargado. Hoy es el respaldo. Cada celda es media ± desvío. Los tiempos están en segundos. El tamaño del árbol sale de recorrer sus nodos. El del bosque suma los nodos y las hojas de sus 100 árboles, y la altura es la del árbol más profundo de cada bosque.

| | DT | RF |
|---|---|---|
| accuracy | 0,9269 ± 0,0219 | 0,9564 ± 0,0232 |
| precision_macro | 0,9212 ± 0,0222 | 0,9573 ± 0,0232 |
| precision_weighted | 0,9285 ± 0,0218 | 0,9581 ± 0,0220 |
| recall_macro | 0,9246 ± 0,0256 | 0,9511 ± 0,0277 |
| recall_weighted | 0,9269 ± 0,0219 | 0,9564 ± 0,0232 |
| f1_macro | 0,9221 ± 0,0236 | 0,9530 ± 0,0251 |
| f1_weighted | 0,9270 ± 0,0220 | 0,9562 ± 0,0234 |
| roc_auc | 0,9246 ± 0,0256 | 0,9893 ± 0,0092 |
| tiempo_fit (s) | 26,0373 ± 4,7815 | 0,1912 ± 0,0430 |
| tiempo_predict (s) | 0,0254 ± 0,0108 | 0,0386 ± 0,0252 |
| nodos | 47,64 ± 5,96 | 3512,96 ± 169,96 |
| hojas | 24,32 ± 2,98 | 1806,48 ± 84,98 |
| altura | 13,20 ± 1,94 | 10,20 ± 0,96 |

En `f1_macro` el bosque queda por encima (0,9530 frente a 0,9221). El árbol es mucho más chico: unos 48 nodos contra unos 3500 del bosque. El ajuste no acompaña esa imagen: el árbol propio tarda unos 26 s por fold y el bosque de scikit-learn, 0,19 s. Predecir es barato en los dos. La Fig. 4 muestra las métricas de test con el desvío como barra de error.

Archivos: `figuras/tabla2_dt_vs_rf.tex` y `figuras/fig4_dt_vs_rf.png`.

## 3.9 Tabla 5

La Tabla 5 compara el mismo árbol con `pruning=False` y con `pruning=True` (`pruning_confidence=0.25`). Son las 25 particiones del `cv` compartido, sobre el dataset cargado. Cada celda es media ± desvío. La variante sin poda coincide con el DT de la Tabla 2: 47,64 nodos y accuracy de prueba 0,9269.

| | sin poda | con poda |
|---|---|---|
| nodos | 47,64 ± 5,96 | 30,68 ± 5,09 |
| hojas | 24,32 ± 2,98 | 15,84 ± 2,54 |
| altura | 13,20 ± 1,94 | 10,64 ± 2,23 |
| accuracy train | 1,0000 ± 0,0000 | 0,9902 ± 0,0058 |
| accuracy test | 0,9269 ± 0,0219 | 0,9304 ± 0,0204 |
| brecha | 0,0731 ± 0,0219 | 0,0598 ± 0,0215 |

La poda hace lo que se espera. El árbol queda más chico (unos 48 nodos contra unos 31). La accuracy de prueba sube un poco (0,9269 a 0,9304). La brecha entre train y test baja (0,0731 a 0,0598): sin poda el árbol memoriza el train (accuracy 1) y con poda deja de hacerlo. El archivo es `figuras/tabla5_poda.tex`.

## 3.10 Fig. 7

La brecha es la media de accuracy en train menos la media en test, en las 25 particiones del `cv` compartido. La Fig. 7 pone train y test lado a lado para el árbol sin poda, el árbol con poda y el bosque.

| | Train | Test | Brecha |
|---|---|---|---|
| DT sin poda | 1,0000 ± 0,0000 | 0,9269 ± 0,0219 | 0,0731 |
| DT con poda | 0,9902 ± 0,0058 | 0,9304 ± 0,0204 | 0,0598 |
| RF | 1,0000 ± 0,0000 | 0,9564 ± 0,0232 | 0,0436 |

Sin poda el árbol acierta todo el train y pierde 7,3 puntos en test. Con poda la brecha baja a 6,0 puntos y la accuracy de prueba no cae. El bosque queda en 4,4 puntos, por debajo de las dos variantes del árbol. En este dataset la poda achica el sobreajuste, pero no llega a la brecha de unos 3 puntos que se esperaba como referencia: la baja es de 7,3 a 6,0. La figura está en `figuras/fig7_brecha_train_test.png`.
