"""Genera notebooks/proyecto_completo.ipynb: UN SOLO cuaderno con TODO el codigo del proyecto adentro.

El cuaderno no necesita la carpeta src: cada modulo (config, utils, nlp_causas, producto_final...) va en una celda que empieza con «%%modulo nombre»;
al ejecutarla, el codigo queda cargado en memoria como un modulo mas, y las celdas siguientes lo importan con `import nombre`. Asi se puede leer,
editar y ejecutar todo desde Jupyter / VS Code.

  python generar_cuaderno.py              arma el cuaderno (sin ejecutarlo) y el script proyecto_completo.py (el mismo flujo, solo codigo)
  python generar_cuaderno.py --ejecutar   ademas ejecuta el cuaderno para guardar los resultados dentro (tarda unos 8 minutos)

La fuente del codigo es la carpeta src; este programa la copia al cuaderno cada vez que se ejecuta (el cuaderno y src nunca se desfasan).
"""
import ast
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell as codigo, new_markdown_cell as texto, new_notebook

RAIZ = Path(__file__).resolve().parent
SRC = RAIZ / "src"
SALIDA = RAIZ / "notebooks" / "proyecto_completo.ipynb"

SECCION = {
    "config": "Configuración", "utils": "Utilidades (navegador, descargas, registro, datos personales)",
    "scraper_escale": "Descarga ESCALE", "scraper_enla": "Descarga ENLA", "scraper_contraloria": "Descarga Contraloría", "scraper_infobras": "Descarga INFOBRAS",
    "descarga_mef": "Descarga MEF", "extraccion": "Tablas de ESCALE y ENLA", "catalogo_escale": "Catálogo de variables de ESCALE", "escale_obras": "ESCALE: locales en construcción",
    "escale_ampliado": "ESCALE ampliado (2025)", "exportar": "Exportar a Excel", "leer_pdf": "PDF: texto y tablas", "tablas_pdf": "PDF: catálogo de tablas",
    "tablas_finales": "PDF: tablas finales y validación", "contraloria_excel": "Contraloría: anexos Excel", "contraloria_anexo03": "Contraloría: anexo 03 (servicios de control)",
    "ubigeo_obras": "Ubigeo de cada obra", "datos_personales": "Datos personales (limpieza y auditoría)", "nlp_causas": "NLP de las causas de paralización",
    "texto_nlp": "NLP del texto de los informes (citas y términos)", "dashboard": "CSV único para el dashboard", "producto_final": "Producto final",
    "auditoria_calidad": "Auditoría de calidad", "diccionario": "Diccionario (ESCALE y ENLA)", "diccionario_pdf": "Diccionario (PDF, final y dashboard)",
    "inventario_datos": "Inventario de datos", "main": "Orquestación de ESCALE/ENLA/Contraloría/INFOBRAS", "main_pdf": "Orquestación del proyecto PDF",
    "pipeline_completo": "Pipeline completo (los 9 pasos)",
}
ORDEN_SECCIONES = list(SECCION)


def orden_de_modulos():
    """Modulos de src en orden de dependencia (un modulo va despues de los que importa); a igual dependencia, el orden de SECCION."""
    nombres = sorted(p.stem for p in SRC.glob("*.py"))
    deps = {}
    for n in nombres:
        arbol = ast.parse((SRC / f"{n}.py").read_text(encoding="utf-8"))
        usados = set()
        for nodo in arbol.body:
            if isinstance(nodo, ast.Import):
                usados |= {a.name.split(".")[0] for a in nodo.names}
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                usados.add(nodo.module.split(".")[0])
        deps[n] = {u for u in usados if u in nombres and u != n}
    puestos, orden = set(), []
    while len(orden) < len(nombres):
        listos = [n for n in nombres if n not in puestos and deps[n] <= puestos]
        if not listos:
            raise SystemExit(f"hay un ciclo de imports entre modulos: {[n for n in nombres if n not in puestos]}")
        proximo = min(listos, key=lambda n: (ORDEN_SECCIONES.index(n) if n in ORDEN_SECCIONES else 999, n))
        puestos.add(proximo)
        orden.append(proximo)
    return orden


def primera_linea_docstring(nombre):
    arbol = ast.parse((SRC / f"{nombre}.py").read_text(encoding="utf-8"))
    doc = ast.get_docstring(arbol) or ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


PRESENTACION = """# Resumen de todo lo que se hizo: extracción, limpieza, NLP y dashboard (todos los scripts juntos)

**Monitor de obras de infraestructura educativa paralizadas.**

**Por qué este cuaderno es tan extenso:** reúne **todos los scripts del proyecto en un solo archivo** (la Parte A trae el código completo de cada módulo).
Cada script también existe **por separado en la carpeta `src/`** (por ejemplo `src/nlp_causas.py` o `src/scraper_infobras.py`), por si se quiere revisar por partes.
`proyecto_completo.py` es la misma ejecución, pero solo con código.

Este cuaderno es **autosuficiente**: lleva adentro **todo el código** del proyecto (descarga, extracción, PDF, NLP de causas, producto final, CSV del dashboard,
diccionario y auditorías) y lo ejecuta de principio a fin. Termina escribiendo **un solo CSV para el dashboard: `data/final/dashboard_obras.csv`** (se carga directo en Power BI).

**Cómo ejecutarlo (para quien revise): no hay que cambiar ninguna ruta ni editar código; solo ejecutar.** Instalar una vez con `pip install -r requirements.txt` (Python 3.10 o superior) y, en VS Code, *Seleccionar kernel* → *Run All*.
* **Rápido (menos de 1 minuto):** *Run All* tal como está. Si no hay datos crudos (como al bajar el repositorio de GitHub), el cuaderno parte solo de las tablas ya procesadas y rehace el NLP, el CSV final y las auditorías.
* **Todo desde cero (alrededor de 1 hora):** poner `DESCARGAR = True` en la celda «0. Opciones» y *Run All*. Se abre Chrome y baja ESCALE, ENLA, Contraloría y MEF (≈ 450 MB); no hay que cerrarlo ni usarlo. INFOBRAS no se vuelve a leer (es una foto de noviembre de 2026).
* Si un portal no responde, volver a ejecutar: lo ya descargado se salta. Guía completa en el `README.md`.

**Cómo usarlo en VS Code:** abrir la carpeta del proyecto → abrir este archivo → *Seleccionar kernel* → *Python Environments* → **`.venv`** → *Run All*.
Con la configuración por defecto **no descarga nada**: usa lo que ya está en `data/raw` (unos 8 minutos) y, si no hay datos crudos (como al bajar el repositorio de GitHub, que no los incluye), parte de las tablas ya procesadas y corre los pasos 5 a 7 (menos de 1 minuto). Todas las rutas son relativas a la carpeta del proyecto.
Para instalar las librerías: `pip install -r requirements.txt` (o doble clic en `ejecutar.bat`, que crea el entorno `.venv`).

**Estructura**
* **Parte A — el código** (una celda por módulo, `%%modulo nombre`): se ejecuta una vez y deja los módulos cargados. Cada celda se puede leer y editar.
* **Parte B — la ejecución paso a paso**: solo el código que corre el proyecto, un paso por celda: 1 descarga · 2 ESCALE y ENLA · 3 datos personales · 4 proyecto PDF · 5 producto final (**NLP de causas** y CSV del dashboard) · 6 diccionario, datos personales e inventario · 7 auditoría de calidad."""

PREPARACION = '''import sys
import types
from pathlib import Path

from IPython.core.magic import register_cell_magic

# La carpeta del proyecto es la que tiene src/ y notebooks/. Se busca desde el cuaderno (VS Code) y desde la carpeta actual, subiendo de
# nivel, para que funcione aunque VS Code se haya abierto sin la carpeta del proyecto.
_inicios = [Path(globals().get("__vsc_ipynb_file__", ".")).resolve().parent, Path.cwd().resolve()]
RAIZ_PROYECTO = next((d for inicio in _inicios for d in [inicio, *inicio.parents] if (d / "src").is_dir() and (d / "notebooks").is_dir()), None)
if RAIZ_PROYECTO is None:
    raise FileNotFoundError("No encuentro la carpeta del proyecto (la que tiene src y notebooks). En VS Code: File -> Open Folder -> la carpeta "
                            "del proyecto, y vuelve a abrir este cuaderno.")


@register_cell_magic
def modulo(linea, celda):
    """%%modulo nombre: ejecuta la celda como un modulo de Python llamado «nombre», que las demas celdas pueden importar."""
    nombre = linea.strip()
    mod = types.ModuleType(nombre)
    mod.__file__ = str(RAIZ_PROYECTO / "src" / f"{nombre}.py")        # config.py deduce de aqui la carpeta del proyecto
    sys.modules[nombre] = mod
    try:
        exec(compile(celda, mod.__file__, "exec"), mod.__dict__)
    except BaseException:
        sys.modules.pop(nombre, None)
        raise
    print(f"módulo «{nombre}» cargado ({len(celda.splitlines())} líneas)")


print("Carpeta del proyecto:", RAIZ_PROYECTO.name)'''

PARTE_B = [
    texto("""# Parte B — Ejecución paso a paso

Solo el código que **corre el proyecto**, un paso por celda y en orden. No hay tablas de revisión: los resultados quedan en `data/final/dashboard_obras.csv` y en `docs/`
(`validacion_final.csv`, `auditoria_calidad.csv`, `auditoria_datos_personales.csv`, `nlp_causas_metricas.csv`, `diccionario.csv`, `inventario_datos.md`).

| Paso | Qué hace | Módulos |
|---|---|---|
| 1 | Descarga ESCALE, ENLA (todos los grados que ofrece SICRECE), Contraloría y MEF (INFOBRAS solo si se pide) | `main`, `scraper_*`, `descarga_mef` |
| 2 | Tablas de ESCALE (+ indicadores ampliados) y ENLA (+ niveles de logro) y catálogo de variables | `extraccion`, `escale_ampliado`, `catalogo_escale` |
| 3 | Quita nombres de personas de los comentarios ya guardados | `datos_personales`, `utils` |
| 4 | Proyecto PDF (fases 1 a 4) y anexos Excel de la Contraloría (incluido el anexo 03) | `main_pdf` y sus módulos |
| 5 | Producto final: **NLP de las causas** (reglas + modelo de apoyo + macro-categorías), tablas y **CSV único del dashboard** | `producto_final`, `nlp_causas`, `dashboard` |
| 6 | Diccionario, auditoría de datos personales e inventario | `diccionario`, `datos_personales`, `inventario_datos` |
| 7 | **Auditoría de calidad** del CSV único (se detiene si hay un error) | `auditoria_calidad` |"""),
    texto("## 0. Opciones"),
    codigo('''from types import SimpleNamespace

import auditoria_calidad
import catalogo_escale
import config
import datos_personales
import diccionario
import escale_ampliado
import inventario_datos
import main
import main_pdf
import pipeline_completo
import producto_final

# ---------------- opciones ----------------
DESCARGAR = False          # True: consulta ESCALE, ENLA, Contraloría y MEF (Chrome visible + internet, ~15 min). False: usa data/raw tal como está
INCLUIR_INFOBRAS = False   # True: ADEMAS vuelve a leer INFOBRAS. Cambia el listado (hay obras que dejaron de estar paralizadas) y mueve los números
FORZAR = False             # True: rehace todo aunque ya esté hecho (muy lento)

# Sin datos crudos (por ejemplo, al bajar el repositorio de GitHub) y sin descargar: se parte de las tablas ya procesadas (solo los pasos 5 a 7)
DESDE_TABLAS = not (DESCARGAR or pipeline_completo.hay_datos_crudos())

FUENTES = list(pipeline_completo.FUENTES_POR_DEFECTO) + (["infobras"] if INCLUIR_INFOBRAS else [])
ARGS = SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES)
print("Carpeta del proyecto:", config.RAIZ.name)
print("Descargar:", DESCARGAR, "| fuentes:", FUENTES)
print("Modo:", "desde las tablas ya procesadas (pasos 5 a 7)" if DESDE_TABLAS else "completo (pasos 1 a 7)")'''),
    texto("""## 1. Descarga de las fuentes
ESCALE, ENLA y Contraloría se descargan con Chrome visible (Selenium); el MEF con una petición HTTP. INFOBRAS solo si se pide: es una foto (27-oct y 11-nov-2026) y leerlo de nuevo cambia los números.
Reglas de cortesía: pausa de 2 a 5 s, 3 reintentos, nada en paralelo, y **lo ya descargado se salta**. Los archivos de `data/raw` nunca se modifican."""),
    codigo('''if DESCARGAR:
    main.descargar(ARGS)
elif DESDE_TABLAS:
    print("No hay datos crudos en data/raw y DESCARGAR = False: se parte de las tablas ya procesadas (pasos 5 a 7). Para repetir desde los portales: DESCARGAR = True")
else:
    print("DESCARGAR = False: no se consulta ningún portal; se usa lo que hay en data/raw")'''),
    texto("""## 2. Tablas de ESCALE y ENLA
`extraccion` convierte los archivos crudos en las tablas de ESCALE (por distrito y año) y de ENLA (por región y grado); `escale_ampliado` calcula 16 indicadores más de infraestructura (Censo 2025);
`catalogo_escale` lista las 331 variables de ESCALE con su descripción oficial."""),
    codigo('''if not DESDE_TABLAS:
    main.extraer(SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES))
    catalogo_escale.construir()
    escale_ampliado.construir()'''),
    texto("""## 3. Datos personales
**La regla del proyecto es no guardar nombres de personas.** `utils.omitir_nombres` los reemplaza por `[NOMBRE OMITIDO]` apenas se lee un comentario; este paso vuelve a pasar el filtro por lo ya guardado (se puede repetir sin cambiar nada)."""),
    codigo('''if not DESDE_TABLAS:
    datos_personales.limpiar()'''),
    texto("""## 4. Proyecto PDF (fases 1 a 4) y anexos Excel
Texto y tablas de los PDF (pdfplumber/pypdf), cifras oficiales, causales, panel por obra de los anexos Excel de la Contraloría (incluido el anexo 03), citas y términos de los informes, ubigeo de cada obra
y tablas ampliadas de INFOBRAS. Un PDF ya procesado no se vuelve a procesar."""),
    codigo('''if not DESDE_TABLAS:
    main_pdf.ejecutar(4, FORZAR)'''),
    texto("""## 5. Producto final: NLP de las causas, tablas y CSV único
`producto_final.construir()` clasifica la causa de cada obra con `nlp_causas` y arma las tablas del producto final y el **CSV único** `data/final/dashboard_obras.csv`.

**NLP** (código en la celda `%%modulo nlp_causas` de la Parte A): normaliza los textos de INFOBRAS, la causal oficial de la Contraloría y la problemática del MEF; puntúa 14 grupos de palabras clave (con negación);
combina las fuentes con pesos; deja una causa principal y hasta 2 secundarias; un modelo de apoyo (TF-IDF + regresión logística con pesos por clase) solo interviene si las reglas no encuentran nada;
y agrupa en 8 macro-categorías para el dashboard. Escribe sus métricas en `docs/nlp_causas_metricas.csv`."""),
    codigo("tablas, validacion = producto_final.construir()"),
    texto("""## 6. Diccionario, datos personales e inventario
El diccionario describe cada columna de cada tabla (si falta una descripción, el programa falla a propósito); la auditoría de datos personales se detiene si encuentra un nombre; el inventario lista qué datos hay."""),
    codigo('''diccionario.escribir_diccionario()
datos_personales.auditoria_o_falla()
inventario_datos.construir()'''),
    texto("""## 7. Auditoría de calidad del CSV único
Revisa estructura, texto, códigos, rangos, fechas, consistencia entre tipos de registro y campos obligatorios; escribe `docs/auditoria_calidad.csv` y se detiene si hay un ERROR."""),
    codigo("auditoria_calidad.auditoria_o_falla()"),
    texto("""## Qué leer después
* `docs/producto_final.md` — qué contiene el CSV único, cómo usarlo y los límites que hay que decir al presentar.
* `docs/limites_y_calidad.md` — lo que la data no tiene o no puede afirmar.
* `docs/diccionario.csv` y `data/final/dashboard_obras_diccionario.csv` — qué significa cada columna."""),
]


CABECERA_SCRIPT = """\"\"\"Proyecto completo, de inicio a fin, en un solo script (solo codigo, sin explicaciones).

Es el mismo flujo de la Parte B del cuaderno notebooks/proyecto_completo.ipynb (que si trae las explicaciones): descarga, tablas de ESCALE y ENLA,
datos personales, proyecto PDF, NLP de las causas, producto final, CSV unico del dashboard, diccionario y auditorias.
El codigo de cada modulo esta en src/ (config.py, utils.py, nlp_causas.py, producto_final.py, ...).

  python proyecto_completo.py        (o en VS Code: «Run Cell» en cada bloque «# %%»)

Este archivo lo genera generar_cuaderno.py desde el cuaderno: no se edita a mano.
\"\"\"
import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ_PROYECTO / "src"))

"""


def armar_script():
    """proyecto_completo.py: las celdas de codigo de la Parte B en orden, con un «# %% titulo» por bloque y sin texto explicativo."""
    bloques, titulo = [], "Preparacion"
    for celda in PARTE_B:
        if celda.cell_type == "markdown":
            primera = celda.source.strip().splitlines()[0].lstrip("# ").strip()
            if primera:
                titulo = primera
        else:
            bloques.append(f"# %% {titulo}\n" + celda.source)
    return CABECERA_SCRIPT + "\n\n".join(bloques) + "\n"


def armar():
    celdas = [texto(PRESENTACION), texto("## Preparación (ejecutar primero)"), codigo(PREPARACION),
              texto("# Parte A — El código del proyecto\nUna celda por módulo, en orden de dependencias. Se ejecutan una vez y quedan cargados; después la Parte B los usa.")]
    for nombre in orden_de_modulos():
        resumen = primera_linea_docstring(nombre)
        celdas.append(texto(f"### `{nombre}` — {SECCION.get(nombre, '')}\n{resumen}"))
        celdas.append(codigo(f"%%modulo {nombre}\n" + (SRC / f"{nombre}.py").read_text(encoding="utf-8").rstrip("\n")))
    celdas += PARTE_B
    return new_notebook(cells=celdas, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    nb = armar()
    SALIDA.parent.mkdir(exist_ok=True)
    nbformat.write(nb, SALIDA)
    (RAIZ / "proyecto_completo.py").write_text(armar_script(), encoding="utf-8")
    print("script armado: proyecto_completo.py (solo codigo)")
    print(f"cuaderno armado: {SALIDA.name} con {len(nb.cells)} celdas ({sum(1 for c in nb.cells if c.cell_type == 'code' and c.source.startswith('%%modulo'))} módulos)")
    if "--ejecutar" in sys.argv:
        from nbclient import NotebookClient
        print("ejecutando el cuaderno (unos minutos)...")
        NotebookClient(nb, timeout=3600, kernel_name="python3", resources={"metadata": {"path": str(SALIDA.parent)}}).execute()
        nbformat.write(nb, SALIDA)
        errores = [c.source[:80].replace("\n", " | ") for c in nb.cells if c.cell_type == "code" and any(o.get("output_type") == "error" for o in c.get("outputs", []))]
        print("celdas con error:", len(errores))
        for e in errores:
            print("  ERROR:", e)
        sys.exit(1 if errores else 0)
