"""Regresiones del panel sin descargar datasets ni ejecutar el informe completo."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace

import gradio as gr
import matplotlib
import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_iris

matplotlib.use("Agg")
NOTEBOOK = Path(__file__).resolve().parents[1] / "TPI_Inteligencia_Artificial.ipynb"


def cargar_panel(carpeta):
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    scope = dict(np=np, pd=pd, SEED=42, TARGET_COL="target", DATASET_KAGGLE="iris",
                 FEATURE_COLS=None, DIR_FIGURAS=carpeta, gr=gr)
    constantes = {"_TOPE_CODIGO", "DISPATCH", "_C45_CF", "_C45_Z", "METRICA_COMPARACION"}
    for cell in cells:
        source = "".join(cell["source"])
        if "# ═══ 6.1 Panel" in source:
            panel = source
            break
        if cell["cell_type"] != "code" or "# ═══ 1.1 Setup" in source:
            continue
        tree = ast.parse(source)
        nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef))
                 or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constantes for t in n.targets)]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "notebook", "exec"), scope)
    iris = load_iris(as_frame=True)
    frame = iris.frame.copy()
    frame["target"] = frame["target"].map(dict(enumerate(iris.target_names)))
    scope["CATALOGO_KAGGLE"] = {"iris": {"nombre": "Iris"}}
    scope["_tabla_kaggle"] = lambda _: (frame.copy(), "Iris")
    exec(panel[:panel.index("\n_faltan =")], scope)
    return scope, panel


@pytest.fixture
def panel(tmp_path):
    return cargar_panel(tmp_path)[0]


def cadena(nivel=1, limite=7):
    return SimpleNamespace(es_hoja=nivel == limite, clase="final", atributo=f"nivel{nivel}",
                           es_continuo=False, hijos={} if nivel == limite else {"rama": cadena(nivel + 1, limite)})


def test_niveles_y_formas_graphviz(panel, monkeypatch):
    import graphviz
    dibujos = []

    class Dibujo:
        def __init__(self):
            self.nodos = []
            dibujos.append(self)

        def attr(self, *args, **kwargs): pass
        def edge(self, *args, **kwargs): pass
        def node(self, *args, **kwargs): self.nodos.append((args, kwargs))
        def render(self, base, **kwargs): return base + ".png"

    monkeypatch.setattr(graphviz, "Digraph", Dibujo)
    monkeypatch.setattr(panel["shutil"], "which", lambda _: "dot")
    raiz = cadena()
    _, total, recorte, _ = panel["_dibujar"](raiz)
    assert total == 7 and recorte and len(dibujos[-1].nodos) == 5
    assert "más ramas" in dibujos[-1].nodos[-1][0][1]
    _, _, recorte, _ = panel["_dibujar"](raiz, niveles=7)
    assert not recorte and len(dibujos[-1].nodos) == 7
    assert dibujos[-1].nodos[-1][1]["shape"] == "ellipse"
    assert dibujos[-1].nodos[0][1]["shape"] == "box"


def test_respaldo_matplotlib_respeta_niveles(panel, monkeypatch):
    etiquetas = []
    original = panel["_etiqueta_nodo"]
    def etiqueta(nodo, cortado):
        etiquetas.append((nodo.atributo, cortado))
        return original(nodo, cortado)
    monkeypatch.setitem(panel, "_etiqueta_nodo", etiqueta)
    ruta = panel["_dibujar_matplotlib"](cadena(), set(), 5)
    assert Path(ruta).exists()
    assert len(etiquetas) == 5 and ("nivel5", True) in etiquetas


def test_contenido_fila_filtra_y_escapa(panel, monkeypatch):
    frame = pd.DataFrame({"dato": ["ignorar", "<script>", None], "clase": [None, "A", "B"]})
    monkeypatch.setitem(panel, "_frame_dataset", lambda _: (frame, "Prueba"))
    ajuste, contenido = panel["_contenido_fila"]("x", "clase", ["dato"], 0)
    assert ajuste["maximum"] == 1 and ajuste["value"] == 0
    assert "&lt;script&gt;" in contenido and "<script>" not in contenido
    assert "clase real" in contenido and "Contenido de la fila 0" in contenido
    ajuste, contenido = panel["_contenido_fila"]("x", "clase", ["dato"], 999)
    assert ajuste["value"] == 1 and "Sin dato" in contenido


def test_comparacion_avanza_exporta_y_limpia_errores(panel):
    frame, _ = panel["_frame_dataset"]("iris")
    attrs = list(frame.columns[:-1])
    args = ["iris", "target", attrs, .2, 2, 1, "3", 2, 1, 0, False, .25, 3, "2", "sqrt", 1]
    eventos = list(panel["_comparar"](*args))
    assert "Preparando" in eventos[0][4] and "panel-spinner" in eventos[0][5]
    assert any("Validación 2/2" in e[4] for e in eventos)
    tabla, cm, barras, csv, aviso, *estados = eventos[-1]
    assert not tabla.empty and cm is not None and barras is not None
    assert len(pd.read_csv(csv)) == len(tabla)
    assert all("panel-spinner" not in e for e in estados)
    assert "Listo" in aviso
    args[2] = []
    final = list(panel["_comparar"](*args))[-1]
    assert final[0].empty and final[1:4] == (None, None, None)
    assert all("panel-spinner" not in e for e in final[5:])
    assert panel["_ui"]["tabla"] is None


def test_arbol_y_cambio_de_niveles_no_reentrena(panel, monkeypatch):
    frame, _ = panel["_frame_dataset"]("iris")
    args = ["iris", "target", list(frame.columns[:-1]), .2, "3", 2, 1, 0, False, .25, 0, 5]
    eventos = list(panel["_ver_arbol"](*args))
    assert "panel-spinner" in eventos[0][1] and eventos[-1][0] is not None
    modelo = panel["_ui"]["modelo"]
    def no_entrenar(*args, **kwargs): raise AssertionError("No debe reentrenar")
    monkeypatch.setattr(modelo, "fit", no_entrenar)
    imagen, camino, nota = panel["_ver_camino"](20, 2)
    assert imagen is not None and "Fila 20" in nota and "2 niveles" in nota
    panel["_invalidar_arbol"]()
    assert panel["_ver_camino"](20, 5)[0] is None


def test_panel_se_construye_con_tema_claro(tmp_path, monkeypatch):
    scope, source = cargar_panel(tmp_path)
    gain_original = scope["gain"]
    monkeypatch.setattr(gr.Blocks, "launch", lambda *args, **kwargs: None)
    exec(source[source.index("\n_faltan ="):], scope)
    # Los controles deben quedar locales: gain sigue siendo la función del árbol.
    assert scope["gain"] is gain_original
    assert not any(isinstance(value, gr.components.Component) for value in scope.values())
    assert scope["_tema"] is not None
    theme = scope["_tema"].to_dict()["theme"]
    assert theme["body_background_fill_dark"] == "white"
    assert theme["block_label_text_color_dark"] == "#465568"
    config = scope["demo_panel"].config
    assert any(c["props"].get("label") == "Niveles visibles del árbol" and c["props"]["value"] == 5 for c in config["components"])
    scope["demo_panel"].close()
    # Reproduce la validación en procesos separados que rompía el panel global.
    from sklearn.model_selection import cross_val_score
    frame, _ = scope["_frame_dataset"]("iris")
    scores = cross_val_score(scope["DecisionTreeC45"](max_depth=2),
                             frame.drop(columns="target"), frame["target"], cv=2, n_jobs=2)
    assert len(scores) == 2 and np.isfinite(scores).all()
