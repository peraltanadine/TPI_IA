# Bitácora — Mauricio Castro

Registro de lo que implementa el integrador y, sobre todo, de lo que se prueba y de la conclusión. Una entrada nueva va arriba. No se anota “anda” sin una corrida.

Cómo se llena cada entrada:

- **Qué se hizo:** el cambio concreto.
- **Qué se probó:** datos, semilla, qué se ejecutó, qué se miró.
- **Resultado:** números o el fallo, tal como salió.
- **Conclusión:** si se deja así, si hay que rehacerlo, o si queda pendiente de otra prueba.

Hasta que Mauricio corre la prueba, la entrada queda en “pendiente de prueba”.

## 2026-11-09 — Tarjeta 11, smoke test de ipywidgets

### Qué se hizo

En el notebook, sección 1.5, se reemplazó el `pass` por la prueba mínima de la tarjeta 11. La celda arma un `Dropdown` (benign / malignant), un `Button` («Probar click») y un `Output`, y los muestra con `display(widgets.VBox(...))`. El click llama a `clear_output(wait=True)` y imprime la clase elegida, el número de click, la versión de ipywidgets y si el entorno es Colab. La celda también imprime ese aviso por `print`, para que quede constancia si el botón no se dibuja.

### Qué se probó

Nada en Colab. En local, con ipywidgets 8.1.9 y Python 3.12.10, sin frontend de Jupyter, se llamó dos veces a `Button.click()` sobre el mismo patrón de la celda: `Output`, `clear_output(wait=True)` y un `print` adentro.

### Resultado

El callback corrió las dos veces. La consola mostró «click 1» y «click 2», con secuencias de limpieza entre medio. `Output.outputs` quedó vacío: sin kernel, el `print` no entra al widget y sale por la consola. Eso no dice si Colab dibuja el botón ni si el segundo click reemplaza la línea de verdad.

### Resultado en Colab

Pendiente de prueba.

### Cómo probarlo

1. En Colab, correr desde la celda de setup (1.1) y después la 1.5. No hace falta correr el árbol.
2. Anotar la versión que imprime la celda y si dice «Google Colab».
3. Confirmar que se ven el desplegable y el botón.
4. Click una vez: debajo tiene que aparecer una sola línea con «Click 1» y la clase elegida.
5. Cambiar el desplegable y click de nuevo: la línea anterior desaparece, queda «Click 2» y la clase nueva.
6. Si no se dibuja nada, el texto del fallback igual tiene que estar en la salida de la celda. En ese caso: `pip install ipywidgets`, reiniciar el runtime y repetir desde el setup.

### Conclusión

Pendiente de la corrida de Mauricio. Sin ese click no se cierra la tarjeta ni se anota «qué onda tiene ipywidgets en Colab».

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
| 11. Probar ipywidgets en Colab | Backlog | Sola | Ver si un botón con `Output` imprime. Si no renderiza, la UI igual tiene que imprimir en la celda. |
| 6. Instalar LaTeX y verificar `llncs.cls` | En revisión | Con Celeste Martín Rodich | `kpsewhich llncs.cls` y `kpsewhich splncs04.bst` tienen que devolver una ruta. |
| 42. Figuras con nombre estable | Backlog | Sola | `figuras/`, gris legible, DPI alto, `plt.close()`. Hoy hay fig4, fig7, fig9 y fig10. |
| 44. Tablas a `.tex` | Backlog | Sola | Media y desvío en columnas separadas. Hoy están la tabla 2 y la tabla 5. |
| 45. UI: dataset, target y features | Backlog | Sola | Dropdowns. Al cambiar el dataset se repuebla el target. |
| 46. UI: hiperparámetros DT y RF | Backlog | Sola | Incluye `max_depth` sin límite. `IntSlider(value=None)` no sirve. |
| 47. UI: CV y tamaño de prueba | Backlog | Sola | `n_splits`, `n_repeats`, `test_size`, con un tope para no disparar una corrida eterna. |
| 48. Botón Ejecutar | Backlog | Sola | Corre los dos modelos, muestra tabla, matrices y barras, y limpia la salida anterior. |
| 49. Exportar resultados a CSV | Backlog | Sola | Descarga media y desvío. Fuera de Colab no tiene que romper. |
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
