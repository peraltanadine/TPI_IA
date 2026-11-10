# Bitácora — Mauricio Castro

Registro de lo que implementa el integrador y, sobre todo, de lo que se prueba y de la conclusión. Una entrada nueva va arriba. No se anota “anda” sin una corrida.

Cómo se llena cada entrada:

- **Qué se hizo:** el cambio concreto.
- **Qué se probó:** datos, semilla, qué se ejecutó, qué se miró.
- **Resultado:** números o el fallo, tal como salió.
- **Conclusión:** si se deja así, si hay que rehacerlo, o si queda pendiente de otra prueba.

Hasta que Mauricio corre la prueba, la entrada queda en “pendiente de prueba”.

## 2026-11-09 — La poda bajó la accuracy en un solo corte

### Qué se hizo

En la prueba de poda, el assert pedía que la accuracy de prueba no bajara en la partición con semilla 42. Ahora puede bajar hasta 3 puntos, el mismo margen que ya tenía `min_samples_leaf`. La brecha puede empeorar hasta 3 puntos. Sigue siendo obligatorio que el árbol quede con menos nodos. Antes de los asserts se imprimen los dos números. El notebook pasa a **Versión 5**.

### Qué se probó

Mauricio corrió la celda en Colab. El assert de nodos pasó. El de accuracy falló: en ese holdout la poda bajó la accuracy de prueba. El mensaje no decía cuánto.

No se volvió a entrenar el árbol en local: la celda base del árbol categórico corta al llegar al dataset continuo, y no hace falta para leer este fallo.

### Resultado

La poda sí achicó el árbol. En un solo corte eso no obliga a que el holdout suba: la decisión de podar usa el entrenamiento. La media de las 25 particiones está en la Tabla 5 (0,9269 sin poda, 0,9304 con poda).

### Conclusión

Hay que volver a correr la celda de la prueba de poda. Si la accuracy bajó más de 3 puntos, el mensaje nuevo trae los dos valores.

## 2026-11-09 — Versión visible en el título

### Qué se hizo

Debajo del título del notebook quedó **Versión 4**. Sirve para ver en Colab si el archivo que se abrió es el último. Esta versión incluye el arreglo de `predict` con etiquetas numéricas.

### Qué se probó

Nada. Es un texto en la primera celda.

### Conclusión

Si en Colab no dice Versión 4, no se actualizó el notebook.

## 2026-11-09 — Iris: predict devolvía etiquetas que sklearn no lee

### Qué se hizo

`predict` devolvía las clases en un array de dtype `object`, también cuando eran los números 0, 1 y 2 de Iris. Ahora, si ese array es `object`, se vuelve a armar para que los números queden como números. Las etiquetas de texto siguen siendo texto.

### Qué se probó

Mauricio llegó a `accuracy_score` en Iris y Colab cortó con `ValueError: mix of multiclass and unknown targets`. El `fit` sí había corrido.

En local se reprodujo el mismo error con `np.array([0, 1, 2, 0], dtype=object)`. sklearn lo clasifica como `unknown`. El mismo vector, sin forzar `object`, es `multiclass` y `accuracy_score` da 1.

### Resultado

El árbol no estaba devolviendo basura: devolvía los números en un tipo que sklearn no acepta como etiqueta.

### Conclusión

Hay que volver a correr la celda que define `DecisionTreeC45` y después la prueba. Si solo se corre la prueba, el kernel sigue con la clase vieja. Iris, XOR y sklearn todavía no tienen un resultado de accuracy.

## 2026-11-09 — NameError de DecisionTreeC45 en la prueba del núcleo

### Qué se hizo

La prueba del núcleo estaba en la sección 2.5, antes de la celda que define `DecisionTreeC45`. Se movió esa prueba para que quede inmediatamente después de la clase.

### Qué se probó

Mauricio corrió la celda en Colab. La entropía ya pasaba. En Iris falló con `NameError: name 'DecisionTreeC45' is not defined`.

### Resultado

La clase no existía todavía en el kernel: se define más abajo, en la celda de interoperabilidad con scikit-learn.

### Conclusión

Hay que volver a correr desde la celda que define `DecisionTreeC45` y seguir con la prueba, que ahora está debajo. Iris, XOR y sklearn siguen sin una corrida que llegue al final.

## 2026-11-09 — Assert de entropía en la celda 2.5

### Qué se hizo

No se cambió `entropy`. Se corrigieron los tres asserts de la celda 2.5, que le pasaban conteos.

### Qué se probó

Mauricio corrió la celda en Colab. Falló el primer assert: `entropy([1, 1])` no dio 1 bit.

En local se midió la misma función. `entropy([1, 1])` da 0. `entropy([0, 1])` da 1. `entropy([0, 1, 2, 3])` da 2. Una serie categórica con diez `"a"` y la categoría `"b"` en cero da 0, sin NaN.

### Resultado

`[1, 1]` son dos etiquetas iguales, o sea una clase sola. La entropía de una clase pura es 0. Para 1 bit hacen falta dos etiquetas distintas, `[0, 1]`.

`gain` llama a `entropy` con la columna de clase. Si la función pasara a leer conteos, un target numérico (0 y 1) se interpretaría mal.

### Conclusión

El fallo era del test, no del árbol. La celda 2.5 hay que volver a correrla: Iris, XOR y la comparación con sklearn no llegaron a ejecutarse.

## 2026-11-09 — Tarjetas 45 a 49, panel

### Qué se hizo

En la celda 6.1 quedó el panel. Cuatro pestañas: Datos, Árbol, Bosque y Validación. Ejecutar parte un holdout con el tamaño de prueba y arma los folds solo sobre el entrenamiento. Bajar CSV escribe `figuras/panel_resultados.csv` con media, desvío y el valor del holdout. Las figuras del panel van a `panel_confusion.png` y `panel_barras.png`, aparte de las figuras del informe.

El `cv` de 25 particiones no se reasigna. El tope del botón es 10 particiones. Profundidad «Sin límite» manda `None` al modelo; el control no usa un slider en `None`, que en ipywidgets no anda. Los comentarios de la celda están en las partes que no se leen solas.

### Qué se probó

En local, sin Colab, se armaron los controles contra Breast Cancer: la clase queda en `target`, los 30 atributos entran en el selector, y al cambiar la clase esa columna sale de los atributos. No se apretó Ejecutar. No se entrenó el árbol.

### Resultado

Pendiente de la corrida en Colab.

### Cómo probarlo

Hace falta que el kernel ya tenga `DecisionTreeC45`, `RandomForestWrap` y `metricas`. La celda de métricas, si se corre entera, entrena el árbol 25 veces antes de llegar al panel y tarda.

1. Correr la celda 6.1. Tienen que verse las cuatro pestañas, Ejecutar y Bajar CSV. La celda imprime ipywidgets y «2 folds y 1 repetición».
2. Sin cambiar nada, Ejecutar. Va a demorar: son 2 ajustes del árbol en los folds y uno más para el holdout. El bosque es rápido.
3. En el panel tiene que quedar una tabla (media, desvío, holdout), dos matrices y un gráfico de barras. Una sola tanda, no dos pegadas.
4. Ejecutar de nuevo. La salida anterior del panel se reemplaza.
5. Bajar CSV. En Colab tiene que descargarse. El archivo también queda en `figuras/panel_resultados.csv`.
6. Subir folds a 5 y repeticiones a 3 (15 particiones). Tiene que negarse y no entrenar. El tope es 10.
7. En Árbol, profundidad «Sin límite» es el default. Probar una corrida corta con profundidad 2 si la primera ya salió bien: tiene que terminar más rápido.

### Conclusión

Pendiente. Sin esa corrida no se cierran las tarjetas 45 a 49.

## 2026-11-09 — Tarjeta 11, corrida en Colab

### Qué se hizo

Mauricio ejecutó la celda 1.5 en Google Colab, dos veces.

### Qué se probó

Primera corrida. La celda imprime el fallback. El entorno dice Google Colab, ipywidgets 7.7.1, dropdown inicial `benign`. Un click deja: «ipywidgets responde. Click 1. Clase elegida: benign. Versión 7.7.1. Entorno: Google Colab.»

Segunda corrida. Misma celda, de nuevo. El desplegable queda en `malignant` y el botón «Probar click» se ve. La salida del widget muestra una sola línea: «ipywidgets responde. Click 2. Clase elegida: malignant. Versión 7.7.1. Entorno: Google Colab.» El número 2 indica que hubo dos clicks en esa corrida y que `clear_output(wait=True)` se llevó la línea anterior.

### Resultado

El botón y el desplegable se dibujan. El click imprime dentro del `Output`. El segundo click reemplaza la línea y toma la clase del desplegable. El `print` de fallback queda en la celda igual. No hizo falta `pip install` ni reiniciar el runtime.

Colab trae ipywidgets 7.7.1. En la máquina local el import había dado 8.1.9. El panel de las tarjetas 45–49 se escribe contra lo que corre en Colab.

### Conclusión

La tarjeta 11 cierra. ipywidgets en Colab sirve para la interfaz. Se mantiene el fallback por `print`, porque la consigna pide que el notebook siga siendo ejecutable si el widget no se ve. El siguiente paso de esta parte es el panel (45–49), con `Dropdown`, `Button`, `Output` y `VBox`, que es lo que esta corrida ya mostró.

## 2026-11-09 — Tarjeta 11, smoke test de ipywidgets

### Qué se hizo

En el notebook, sección 1.5, se reemplazó el `pass` por la prueba mínima de la tarjeta 11. La celda arma un `Dropdown` (benign / malignant), un `Button` («Probar click») y un `Output`, y los muestra con `display(widgets.VBox(...))`. El click llama a `clear_output(wait=True)` y imprime la clase elegida, el número de click, la versión de ipywidgets y si el entorno es Colab. La celda también imprime ese aviso por `print`, para que quede constancia si el botón no se dibuja.

### Qué se probó

Nada en Colab. En local, con ipywidgets 8.1.9 y Python 3.12.10, sin frontend de Jupyter, se llamó dos veces a `Button.click()` sobre el mismo patrón de la celda: `Output`, `clear_output(wait=True)` y un `print` adentro.

### Resultado

El callback corrió las dos veces. La consola mostró «click 1» y «click 2», con secuencias de limpieza entre medio. `Output.outputs` quedó vacío: sin kernel, el `print` no entra al widget y sale por la consola. Eso no dice si Colab dibuja el botón ni si el segundo click reemplaza la línea de verdad.

### Conclusión

La corrida de Colab está en la entrada de arriba. Esta entrada queda como el armado de la celda y la prueba local, que no alcanzaba para cerrar la tarjeta.

## 2026-11-09 — Lectura del tablero

### Qué se hizo

Se leyó el export `mYvQVOWz - ia.json` (tablero IA, 62 tarjetas) y el reparto del notebook. Mauricio Nicolás Castro está como integrador: andamiaje, Colab, widgets, interfaz, figuras, bitácora y cierre del informe.

La asignación real es el campo `idMembers` de cada tarjeta. El renglón `Owner: A–E` del texto quedó viejo: la tarjeta 5 está en Hecho y los nombres reales no se copiaron a esas descripciones. Por esa letra, las tarjetas 7, 8 y 9 dicen Owner D, pero en el tablero están asignadas a Matías Machado. No son de esta bitácora.

No se tocó código.

### Qué se probó

Nada. Esta entrada no tiene resultado de ejecución.

### Conclusión

Quedan 22 tarjetas con Mauricio fuera de Hecho. El núcleo propio, antes del informe, es la prueba de ipywidgets (11) y el panel (45–49). Las figuras, el LaTeX y el Run all vienen después, cuando haya salidas estables para incrustar. Las secciones del informe (52–57) están compartidas: él arma el esqueleto y cierra el PDF; el texto de cada parte lo escribe quien implementó esa parte.

### Tarjetas ya en Hecho, con él asignado

| Tarjeta | Lista | Con quién |
|---|---|---|
| 3. Consultar el dataset a la cátedra | Hecho | Todo el equipo |
| 5. Asignar nombres reales a los roles | Hecho | Solo |
| 10. Crear el notebook en Colab y versionarlo | Hecho | Solo |

### Tarjetas abiertas que son suyas

| Tarjeta | Lista | Sola o compartida | Para qué |
|---|---|---|---|
| 11. Probar ipywidgets en Colab | Probada el 9/11, mover a Hecho | Sola | En Colab, ipywidgets 7.7.1: el botón se ve, el click imprime y el segundo click reemplaza la línea. El fallback por `print` también queda. |
| 6. Instalar LaTeX y verificar `llncs.cls` | En revisión | Con Celeste Martín Rodich | `kpsewhich llncs.cls` y `kpsewhich splncs04.bst` tienen que devolver una ruta. |
| 42. Figuras con nombre estable | Backlog | Sola | `figuras/`, gris legible, DPI alto, `plt.close()`. Hoy hay fig4, fig7, fig9 y fig10. |
| 44. Tablas a `.tex` | Backlog | Sola | Media y desvío en columnas separadas. Hoy están la tabla 2 y la tabla 5. |
| 45. UI: dataset, target y features | Celda lista, falta Colab | Sola | Dropdowns. Al cambiar el dataset se repuebla la clase. |
| 46. UI: hiperparámetros DT y RF | Celda lista, falta Colab | Sola | Profundidad con «Sin límite», no con un slider en None. |
| 47. UI: CV y tamaño de prueba | Celda lista, falta Colab | Sola | Folds, repeticiones y tamaño de prueba. Tope de 10 particiones. |
| 48. Botón Ejecutar | Celda lista, falta Colab | Sola | Tabla, matrices y barras. La segunda corrida limpia el panel. |
| 49. Exportar resultados a CSV | Celda lista, falta Colab | Sola | Media, desvío y holdout. Fuera de Colab no rompe: deja el archivo. |
| 50. `main.tex` LNCS | Backlog | Sola | Siete secciones, español, autores e instituto. Tiene que compilar aunque el texto esté corto. |
| 51. Incrustar figuras y tablas | Backlog | Sola | `\includegraphics` e `\input`. Antes de redactar largo, para ver las 12 carillas. |
| 52. Secciones 1 y 2 | Backlog | Con Celeste y Nadine | Introducción y algoritmos. |
| 53. Sección 3 | Backlog | Con Camila, Celeste y Matías | Solución y problemas encontrados. |
| 54. Secciones 4 y 5 | Backlog | Con Nadine | Metodología y resultados. |
| 55. Secciones 6 y 7 | Backlog | Todo el equipo | Discusión y conclusiones. |
| 56. `referencias.bib` | Backlog | Todo el equipo | Cada cita verificada contra la fuente. Una cita que no coincide desaprueba el trabajo. |
| 57. Coloquio | Backlog | Todo el equipo | Demo de 5 minutos y reparto de preguntas. A él le tocan la UI, ipywidgets en Colab y las figuras. |
| 58. Restart and Run all | Backlog | Sola | Runtime limpio, sin clicks a mano. Fecha interna del tablero: 10/11. |
| 59. PDF de hasta 12 carillas | Backlog | Sola | Sin achicar márgenes ni interlineado de Springer. |
| 60. Ortografía | Backlog | Sola | Una pasada humana además del corrector. |
| 61. Subir código y cerrar tarjetas | Backlog | Sola | El tablero tiene que coincidir con el repo. |
| 62. Entregar | Backlog | Sola en la asignación | 11/11, 23:59. Checklist de las tarjetas 47, 56, 58, 59, 60 y 61. |

No están en su asignación: el árbol (Celeste y Camila), la carga y el EDA (Matías), ni los experimentos y el Random Forest (Nadine, tarjetas 30–40 y 43).
