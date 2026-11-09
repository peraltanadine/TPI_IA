# Tarjeta 36 · E2–E4, barridos del DT

Fecha: 2026-11-06  
`docs/technical.md` §7 y `docs/informe-lncs.md` no están en el proyecto. La celda de la sección 5 sigue en `# TODO — barridos E2–E11`.

## ¿Se puede hacer?

El barrido sí. `DecisionTreeC45` ya tiene `max_depth`, `min_samples_leaf` y `min_gain_ratio`, y el `cv` compartido ya está. No depende de E5, ni del test de poda, ni de E6 en adelante: esos responden otra pregunta.

La trampa que la sección 5 marca como card 43 sí importa para el cierre. Elegir el hiperparámetro con estas 25 particiones y publicar esa misma accuracy como resultado del modelo queda sesgado. La Fig. 6a y las tres tablas pueden salir de este `cv`. La accuracy del valor elegido, la que va al informe como resultado, tiene que salir de un holdout que el barrido no vio, o de un CV anidado. Sin esa separación, la curva está bien y el número del óptimo no.

Cada barrido mueve un solo parámetro. Los otros quedan en el default del estimador: `max_depth=None`, `min_samples_leaf=1`, `min_gain_ratio=0`, `pruning=False`, `random_state=SEED`. Se usa el `df` cargado. Hoy es el respaldo: 30 columnas numéricas y ninguna categórica.

## Qué falta

| Pedido | Ahora |
|---|---|
| E2, `max_depth` en 1, 2, 3, 5, 8 y None | No está corrido |
| E3, `min_samples_leaf` | El parámetro existe. La tarjeta no fija la grilla. Propuesta: 1, 2, 5, 10, 20, 50 |
| E4, `min_gain_ratio` | El parámetro existe y el árbol ya parte por gain ratio. La tarjeta no fija la grilla. Propuesta: 0, 0,01, 0,05, 0,1, 0,2 |
| Tres tablas, media ± desvío en las 25 particiones | No están |
| Fig. 6a, curva con barras de error | No está |
| Discutir el óptimo y por qué no es el de más accuracy | No está |

De cada valor se guardan accuracy de train, accuracy de test y brecha. La curva de la Fig. 6a es la accuracy de test contra `max_depth`, con el desvío de las 25 particiones. `None` se etiqueta "sin tope".

## Cómo se elige el óptimo

No se elige el punto con la accuracy de test más alta. Se elige el árbol más chico cuya media de test queda a menos de un desvío de esa máxima. Si la accuracy sigue subiendo de punta a punta, sin frenarse, el barrido no se publica: la tarjeta lo marca como señal de que algo está mal.

## E4 en este dataset

Gain ratio existe para no preferir un atributo solo porque tiene muchas categorías. En el respaldo todos los cortes son binarios, de una columna continua, así que esa penalización no tiene a quién aplicarse. Si al mover `min_gain_ratio` la accuracy casi no cambia, se dice así. Es un resultado válido. Con el dataset definitivo, si trae categóricas, el barrido se vuelve a correr.
