# Tarjeta 43 · Holdout único

Fecha: 2026-11-06  
`docs/technical.md` §6.3 no está en el proyecto.

## Estado

Cerrada con la opción A. No se usa CV anidado.

En la sección 5 del notebook, antes del TODO de barridos, `partir_holdout` hace un corte estratificado 80/20 con `random_state=SEED`. `evaluar_holdout_una_vez` ajusta el árbol y el bosque en `X_tr` y predice `X_te` una vez. La segunda llamada, con el mismo dataset, no reentrena.

En el respaldo: 455 / 114. `f1_macro` 0,9246 (DT) y 0,9713 (RF). Archivo: `figuras/holdout_final.json`. El texto está en `informe/seccion4.md`.

Los barridos todavía no están escritos. La celda de TODO dice que tienen que usar `X_tr, y_tr`. Las tablas 2 y 5 y las figuras 7 y 9 se midieron antes, sobre todas las filas.
