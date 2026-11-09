# Test de poda (card de la compañera, previa a E5)

Fecha: 2026-11-06  
`docs/technical.md` y `docs/cards/sprint-3.md` no están en el proyecto. E5 la cita como la card 28: el test que hay que tener antes de publicar la Tabla 5. La card 29 es el bug si la poda agranda el árbol o empeora la prueba.

## Estado

Abierta. No hay un test. No hay archivo de tests, ni `assert` sobre la poda. Lo único que corre solo es un `print` de la celda de sklearn, con 8 filas fijas de clima y viento: de 7 nodos a 3. Ahí la accuracy no cambia (train 0,667, test 0,500) y la brecha tampoco (0,167). No afirma nada, así que un bug no lo haría fallar.

El estimador no tiene `n_nodes()`, `n_leaves()` ni `max_depth_()`. El tamaño se mide por fuera, recorriendo `arbol_.raiz`.

## Qué ya se vio en la Tabla 5

Esas 25 particiones no reemplazan el test, pero los tres criterios de cierre ya salen en esa dirección, sobre el dataset cargado:

| Criterio | Sin poda | Con poda |
|---|---|---|
| Tamaño (nodos) | 47,64 | 30,68, menor |
| Accuracy de prueba | 0,9269 | 0,9304, no baja |
| Brecha train/test | 0,0731 | 0,0598, baja |

## Qué falta para cerrarla

1. Un test sobre el dataset cargado, no sobre clima/viento, que falle si alguna de estas tres cosas no se cumple: el árbol con poda tiene menos nodos, la accuracy de prueba no baja, la brecha baja.
2. `min_samples_leaf` grande: el árbol queda chico y la accuracy de prueba queda igual o mejor. No está medido.
3. Las predicciones: podar no cambia la mayoría. No está medido.
4. Medir el tamaño con la misma función en las dos variantes. Pueden ser métodos del estimador o el recorrido que ya usa la Tabla 5. Las dos variantes tienen que usar la misma cuenta.
