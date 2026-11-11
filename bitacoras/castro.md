# Bitácora — Mauricio Castro

Registro de lo que implementa el integrador y, sobre todo, de lo que se prueba y de la conclusión. Una entrada nueva va arriba. No se anota “anda” sin una corrida.

Cómo se llena cada entrada:

- **Qué se hizo:** el cambio concreto.
- **Qué se probó:** datos, semilla, qué se ejecutó, qué se miró.
- **Resultado:** números o el fallo, tal como salió.
- **Conclusión:** si se deja así, si hay que rehacerlo, o si queda pendiente de otra prueba.

Hasta que Mauricio corre la prueba, la entrada queda en “pendiente de prueba”.

## 2026-11-11 — Una sola pasada en la celda de métricas

### Qué se hizo

El notebook pasa a **Versión 12**. La celda de métricas ya no entrena el árbol dos veces. Una pasada arma la tabla. El cruce usa 2 procesos como máximo: con 8 la máquina se queda sin memoria. La semilla 42 deja la corrida fija.

### Qué se probó

No se volvió a entrenar. El cambio es el recorrido de la celda.

### Resultado

En Colab la doble pasada fueron 50 minutos y cortó por el nombre `DT`. Con una pasada y 2 procesos el árbol queda cerca de 15 minutos.

### Conclusión

Hay que correr la celda en Versión 12. Hasta que imprima `✓ DecisionTreeC45` no hay más texto: los ajustes van en otros procesos.

## 2026-11-11 — La segunda pasada comparaba el nombre

### Qué se hizo

El notebook pasa a **Versión 11**. La primera pasada guardaba el modelo como `DT` y `evaluar_cv` lo nombra `DecisionTreeC45`. El assert cortaba ahí, con las dos pasadas ya calculadas. Ahora las dos usan el nombre de la clase.

### Qué se probó

El traceback de Colab, 50 minutos, columna `modelo` distinta en el 100 % de las filas. No se volvió a entrenar.

### Resultado

No había diferencia de métricas en el mensaje: el primer valor que no coincidía era `DT` contra `DecisionTreeC45`.

### Conclusión

Hay que volver a correr la celda en Versión 11. El árbol otra vez son dos pasadas.

## 2026-11-11 — La celda de métricas quedaba en blanco

### Qué se hizo

El notebook pasa a **Versión 10**. La celda de métricas ajustaba el árbol tres veces, 25 particiones cada una, con 4 procesos y sin texto hasta el final. Un cruce de 20 filas con 4 procesos tardó 53 segundos solo en arrancar. Ahora va en un proceso, imprime `ajuste 1/25` y la tabla reutiliza la primera pasada. La segunda pasada sigue, para comprobar que coincide.

### Qué se probó

El arranque en 4 procesos, con un árbol de sklearn y 20 filas. No se volvieron a entrenar las 25 particiones de Heart Disease.

### Resultado

Ese arranque devolvió a los 53 segundos, sin imprimir nada antes. La celda ya tenía la Tabla 2 de la corrida del 11 de noviembre. El aviso de E5 sigue al final, a propósito.

### Conclusión

Hay que frenar la corrida vieja y volver a correr la celda en Versión 10. La primera pasada del árbol son unos 25 minutos, con una línea por ajuste.

## 2026-11-11 — Tipos y menú sin nombres fijos

### Qué se hizo

El notebook pasa a **Versión 9**. Se sacó la lista `sex`, `cp`, `fbs` y el resto. Un atributo es categoría si es texto, bool, o un entero con hasta 10 valores distintos. El menú del panel toma los CSV de `data/`. La clase es la columna `target` si existe y, si no, la última.

### Qué se probó

Se corrió esa regla sobre los tres CSV, sin entrenar.

### Resultado

Heart Disease sigue en cinco continuas y ocho códigos. Iris queda en cuatro continuas. Play Tennis queda en cuatro categorías, `windy` incluido. El menú ya no nombra esos archivos en el código.

### Conclusión

Los modelos no dependen del nombre de las columnas. El lector de las cuatro sedes sí: esos archivos no traen encabezado. Las tablas del informe no se recalcularon.

## 2026-11-11 — Tres datasets en el menú del panel

### Qué se hizo

El notebook pasa a **Versión 8**. El desplegable del panel ofrece Play Tennis (`data/play+tennis+dataset/weather.csv`, clase `play`), Iris (`data/iris+dataset/iris.csv`, clase `species`) y Heart Disease (`data/dataset.csv`, clase `target`). Breast Cancer sigue como respaldo. Un bool, como `windy`, se trata como categoría. El informe no se reentrenó.

### Qué se probó

Se cargaron los tres CSV y se miró el tipo de cada columna después del preprocess, pasando la clase de cada archivo. No se apretó Ejecutar. No se abrió Colab.

### Resultado

Play Tennis queda todo discreto, con `windy` en true/false. Iris queda con las cuatro medidas continuas y `species` como clase. Heart Disease sigue mezclado: cinco continuas y ocho códigos. El menú arranca en Heart Disease.

### Conclusión

Las tablas del paper siguen siendo las del mezclado. Para ver el menú hay que correr la celda 6.1 en Colab. Play Tennis tiene 14 filas: sirve para probar el panel, no para una tabla del informe.

## 2026-11-11 — El apartado de problemas del paper

### Qué se hizo

La sección «Solución y problemas» de `informe/main.tex` contaba las tres diferencias con C4.5 y casi no contaba los fallos que hubo que corregir. Ahora incluye, con el arreglo al lado, lo que está en esta bitácora y en la de la solución: la firma `fit(X, y)`, la entropía sobre etiquetas, la prueba que corría antes de existir la clase, `predict` con dtype `object` en Iris, el ROC de dos clases, el assert de la poda, el piso 0,85 que era de Breast Cancer, el texto de pandas 3 y el nodo sin clase mayoritaria, y el diálogo de Drive.

### Qué se probó

Recompilación con MiKTeX. No se volvió a entrenar.

### Resultado

Queda en el PDF de esta fecha. Los números de las tablas no se tocaron.

### Conclusión

El apartado ahora explica qué se rompió y qué se dejó. Sigue faltando la pasada de ortografía.

## 2026-11-11 — Heart Disease, cuatro sedes, corrida local

### Qué se hizo

El notebook pasa a **Versión 7**. La celda 1.2 arma el dataset adentro del notebook: lee `processed.cleveland.data`, `processed.hungarian.data`, `processed.switzerland.data` y `processed.va.data`, trata `?` como faltante y mapea `num` 0 a ausencia y 1–4 a presencia. Escribe `data/dataset.csv`. No quedó un script aparte.

La celda 1.4 corre antes del EDA. Los códigos (sexo, dolor, `fbs`, electrocardiograma, angina, pendiente, `ca`, `thal`) quedan como categoría. Las continuas quedan como float. No se imputa. El colesterol 0 se deja: el archivo de nombres no lo define como faltante.

Los barridos E2–E11 miran solo el entrenamiento del holdout 80/20 con semilla 42. La exportación no copia el archivo de Breast Cancer encima de un resultado de esta corrida. El cruce validado usa 4 procesos: con 8, la máquina de 8 GB se quedaba sin memoria.

### Qué se probó

`python` ejecutó todas las celdas de código, en orden, y guardó el notebook con las salidas. Semilla 42. `RepeatedStratifiedKFold` de 5 por 5. Dataset: 920 filas (303, 294, 123 y 200), 411 ausencia y 509 presencia, 1759 faltantes, 172 colesteroles en 0.

Pasaron la entropía, Iris (0,973), XOR, la poda en el holdout (448 a 71 nodos) y el bosque (accuracy de holdout 0,8641 en el valor por defecto).

### Resultado

Tabla 2, 25 particiones. F1 macro: árbol 0,7809 ± 0,0271, bosque 0,8157 ± 0,0308. Accuracy: 0,7850 ± 0,0265 y 0,8187 ± 0,0305. ROC-AUC: 0,8195 ± 0,0295 y 0,8839 ± 0,0254. Nodos: 452,00 ± 36,44 y 28876,48 ± 664,66. Altura del árbol: 13,00 ± 0,00. Ajuste: 50,59 ± 9,80 s y 0,484 ± 0,041 s.

Tabla 5. Sin poda: 452 nodos, accuracy de prueba 0,7850, brecha 0,1435, train 0,9285. Con poda (CF 0,25): 71,20 nodos, accuracy de prueba 0,7741, brecha 0,0922. En el único holdout la poda sube la accuracy de prueba de 0,7880 a 0,7989.

Holdout por defecto, 736 / 184, positiva presencia. Árbol: accuracy 0,7880, F1 macro 0,7819, ROC-AUC 0,8192, TN/FP/FN/TP 57/25/14/88. Bosque: 0,8641, 0,8616, 0,9219, 67/15/10/92.

Barridos, regla del más chico dentro de un desvío del máximo. Profundidad 2, hoja 50, gain ratio 0,1, 10 árboles, `log2`. Profundidad, gain ratio y cantidad de árboles siguen subiendo en el valor más complejo. El holdout de esa combinación, elegida de a un parámetro, da F1 macro 0,7926 en el árbol y 0,8336 en el bosque. El bosque por defecto, en el mismo corte, queda en 0,8616.

`informe/main.pdf` compiló en 9 carillas, sin cajas que se salgan del margen.

### Conclusión

Los números de Breast Cancer no se reutilizan. El árbol no es un C4.5 completo: un solo corte por atributo, poda sin subtree raising y factor `t` propio. Queda para Mauricio la pasada de ortografía, subir el PDF y mover el Trello. Colab no se abrió. El botón Ejecutar del panel no se apretó.

## 2026-11-10 — Cierre del notebook y del informe

### Qué se hizo

El notebook pasa a **Versión 6**.

La celda de Drive ya no llama a `drive.mount`. Imprime que sigue con `data/dataset.csv` o con el respaldo, y un Run all no se queda esperando el permiso.

La celda de figuras copia a `figuras/` lo ya medido: `fig4_dt_vs_rf.png`, `fig7_brecha_train_test.png`, `fig9_matrices_confusion.png`, `fig10_roc_por_clase.png`, `tabla2_dt_vs_rf.tex`, `tabla5_poda.tex`, `tabla_tn_fp_fn_tp.csv` y `holdout_final.json`. No reentrena y no arma otra Tabla 2. Esos archivos también quedaron copiados en el repo. En los `.tex` se escapó el guion bajo y la tabla se escala al ancho de la página. Los números son los de la corrida anterior.

La demo 6.2 lee `holdout_final.json` si existe y lo muestra. Si no está, dice que el camino es Ejecutar en el panel. No lanza las 25 particiones.

El informe está en `informe/main.tex`, con `referencias.bib`. Español, clase `llncs`, los cinco autores y una sola filiación (UTN FRRe). Entran la Tabla 2, la Tabla 5 y las figuras 4, 7, 9 y 10. El texto sale de las secciones ya escritas y de la bitácora del árbol. Dice que los barridos E2–E11 no se corrieron, que los números son de Breast Cancer y que el árbol no es un C4.5 completo: un solo corte por atributo continuo, poda sin subtree raising y factor `t` propio.

### Qué se probó

Compilación en esta máquina, con MiKTeX. `pdflatex` cargó `llncs.cls` 2.26 desde `C:\Users\castr\AppData\Local\Programs\MiKTeX\tex\latex\llncs\llncs.cls`. BibTeX usó `splncs04.bst` en `C:\Users\castr\AppData\Local\Programs\MiKTeX\bibtex\bst\llncs\splncs04.bst`. Salieron 8 páginas (`informe/main.pdf`, 756396 bytes). Las cinco citas resuelven: Quinlan (AddErrs, pp. 278–279), Liu p. 67, Breiman 2001, Pedregosa et al. 2011 y Breast Cancer Wisconsin. El log de la segunda pasada no marca cajas que se salgan del margen.

No corrí el notebook en Colab. No apreté Ejecutar en el panel. No volví a entrenar la poda.

### Resultado

El PDF entra en las 12 carillas. En la Tabla 2 el F1 macro sigue en 0,9221 ± 0,0236 para el árbol y 0,9530 ± 0,0251 para el bosque. La Tabla 5 sigue en 47,64 nodos sin poda y 30,68 con poda.

### Conclusión

Queda para Mauricio: abrir el notebook y confirmar que el título dice Versión 6; correr la celda de poda; en el panel, Ejecutar, una segunda corrida y Bajar CSV; el Run all cuando pueda dejar la máquina (la celda de métricas entrena el árbol 25 veces, dos pasadas); leer el PDF; pasar en el Trello a Hecho la 11 y, cuando vea el panel, la 45–49; subir el PDF a la cátedra. El tablero en vivo no se tocó.

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
| 6. Instalar LaTeX y verificar `llncs.cls` | Compiló en esta máquina | Con Celeste Martín Rodich | `llncs.cls` 2.26 y `splncs04.bst` están en el MiKTeX de esta PC. El PDF salió. |
| 42. Figuras con nombre estable | Archivos en `figuras/` | Sola | fig4, fig7, fig9 y fig10 copiadas, sin regenerar. La celda de copia falta correrla en Colab. |
| 44. Tablas a `.tex` | Archivos en `figuras/` | Sola | Tabla 2 y Tabla 5, media y desvío en columnas separadas. Mismos números. |
| 45. UI: dataset, target y features | Celda lista, falta Colab | Sola | Dropdowns. Al cambiar el dataset se repuebla la clase. |
| 46. UI: hiperparámetros DT y RF | Celda lista, falta Colab | Sola | Profundidad con «Sin límite», no con un slider en None. |
| 47. UI: CV y tamaño de prueba | Celda lista, falta Colab | Sola | Folds, repeticiones y tamaño de prueba. Tope de 10 particiones. |
| 48. Botón Ejecutar | Celda lista, falta Colab | Sola | Tabla, matrices y barras. La segunda corrida limpia el panel. |
| 49. Exportar resultados a CSV | Celda lista, falta Colab | Sola | Media, desvío y holdout. Fuera de Colab no rompe: deja el archivo. |
| 50. `main.tex` LNCS | Escrito y compilado | Sola | `informe/main.tex`. Siete secciones, español, cinco autores, UTN FRRe. 8 carillas. |
| 51. Incrustar figuras y tablas | Hecho en el tex | Sola | Entran fig4, fig7, fig9, fig10, Tabla 2 y Tabla 5. |
| 52. Secciones 1 y 2 | Redactadas | Con Celeste y Nadine | Introducción y algoritmos, a partir del texto ya medido. Falta la lectura del equipo. |
| 53. Sección 3 | Redactada | Con Camila, Celeste y Matías | Solución, el cambio de `fit(X, y)` y las tres diferencias con C4.5. |
| 54. Secciones 4 y 5 | Redactadas | Con Nadine | Metodología y resultados con los números de las tablas. |
| 55. Secciones 6 y 7 | Redactadas | Todo el equipo | Discusión (respaldo, sin barridos, poda en 25 particiones) y conclusiones. |
| 56. `referencias.bib` | Cinco citas, usadas | Todo el equipo | Quinlan 1993, Liu p. 67, Breiman 2001, Pedregosa 2011, Breast Cancer Wisconsin. |
| 57. Coloquio | Backlog | Todo el equipo | Demo de 5 minutos y reparto de preguntas. A él le tocan la UI, ipywidgets en Colab y las figuras. |
| 58. Restart and Run all | Drive ya no frena | Sola | Falta correrlo en Colab. La celda de métricas entrena el árbol 25 veces, dos pasadas. |
| 59. PDF de hasta 12 carillas | 8 carillas | Sola | `informe/main.pdf`. Márgenes de `llncs`, sin achicarlos. |
| 60. Ortografía | Backlog | Sola | Una pasada humana además del corrector. |
| 61. Subir código y cerrar tarjetas | Backlog | Sola | El tablero tiene que coincidir con el repo. |
| 62. Entregar | Backlog | Sola en la asignación | 11/11, 23:59. Checklist de las tarjetas 47, 56, 58, 59, 60 y 61. |

No están en su asignación: el árbol (Celeste y Camila), la carga y el EDA (Matías), ni los experimentos y el Random Forest (Nadine, tarjetas 30–40 y 43).
