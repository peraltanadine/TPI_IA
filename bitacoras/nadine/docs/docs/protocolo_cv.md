# Card 33 · Repeated Stratified K-Fold

Fecha: 2026-11-06

## Estado al empezar

No había protocolo. El setup solo tenía `SEED`. La celda de métricas terminaba en un TODO: `evaluate`, la validación cruzada, E1 y E5 estaban sin hacer. `docs/technical.md` §6.1 no está en el proyecto.

## Qué faltaba

Una sola constante `cv`, usada por el árbol y por el bosque:

`cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED)`

Y un `cross_validate` con `n_jobs=-1` y `return_train_score=True` que deje 25 filas por métrica y se repita igual con la misma semilla.

## Qué se hizo

- `cv` se crea en la celda 1.1, una sola vez. `evaluar_cv` rechaza otro splitter o una semilla distinta.
- La tabla larga tiene una fila por partición y métrica (`repeat`, `fold`, `train`, `test`, `brecha`).
- Antes de medir, se controla que cada fold de test conserve todas las clases.
- El árbol y el bosque pasan por la misma función.

En scikit-learn 1.6, `RepeatedStratifiedKFold` no tiene atributo `n_splits`. El conteo sale de `get_n_splits()` (25) y `n_repeats` (5).

El árbol de la corrida usa `max_depth=2` y `min_samples_leaf=5`. Un ajuste suelto sobre Breast Cancer tarda 17,5 s con esa profundidad y 14,2 s sin tope (`min_samples_leaf=5` en ambos). El bosque usa 100 árboles.

## Verificación

Dataset de respaldo, 569 filas. Las dos clases aparecen en los 25 folds de test.

| Criterio | Resultado |
|---|---|
| `cross_validate` con DT y con RF | OK, 142,5 s las dos pasadas de cada uno |
| 25 filas por métrica | OK, 8 métricas × 2 modelos |
| Dos corridas con `random_state=SEED` | Tablas idénticas (`assert_frame_equal`) |

Los promedios están en `informe/seccion3.md`, sección 3.5.

E5 está en `construir_tabla5` y en `figuras/tabla5_poda.tex`. El resumen DT vs RF de esta corrida queda en `resumen_cv` dentro del notebook.
