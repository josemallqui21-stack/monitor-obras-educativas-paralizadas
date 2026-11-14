"""Genera notebooks/proyecto_completo.ipynb: UN SOLO cuaderno con TODO el codigo del proyecto adentro.

El cuaderno no necesita la carpeta src: cada modulo (config, utils, nlp_causas, producto_final...) va en una celda que empieza con «%%modulo nombre»;
al ejecutarla, el codigo queda cargado en memoria como un modulo mas, y las celdas siguientes lo importan con `import nombre`. Asi se puede leer,
editar y ejecutar todo desde Jupyter / VS Code.

  python generar_cuaderno.py              arma el cuaderno (sin ejecutarlo)
  python generar_cuaderno.py --ejecutar   lo arma y lo ejecuta para guardar los resultados dentro (tarda unos 8 minutos)

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


PRESENTACION = """# Proyecto completo: de los portales al dashboard (un solo cuaderno)

**Monitor de obras de infraestructura educativa paralizadas** (USMP, Data Analytics).

Este cuaderno es **autosuficiente**: lleva adentro **todo el código** del proyecto (descarga, extracción, PDF, NLP de causas, producto final, CSV del dashboard,
diccionario y auditorías) y lo ejecuta de principio a fin. Termina escribiendo **un solo CSV para el dashboard: `data/final/dashboard_obras.csv`** (se carga directo en Power BI).

**Cómo usarlo en VS Code:** abrir la carpeta del proyecto → abrir este archivo → *Seleccionar kernel* → *Python Environments* → **`.venv`** → *Run All*.
Con la configuración por defecto **no descarga nada** (usa lo que ya está en `data/raw`) y tarda unos 8 minutos. Todas las rutas son relativas a la carpeta del proyecto.
Para instalar las librerías: `pip install -r requirements.txt` (o doble clic en `ejecutar.bat`, que crea el entorno `.venv`).

**Estructura**
* **Parte A — el código** (una celda por módulo, `%%modulo nombre`): se ejecuta una vez y deja los módulos cargados. Cada celda se puede leer y editar.
* **Parte B — la ejecución paso a paso**, con explicaciones y resultados: 1 descarga · 2 ESCALE y ENLA · 3 datos personales · 4 proyecto PDF · 5 **NLP de causas** · 6 producto final y CSV del dashboard · 7 diccionario, auditorías e inventario."""

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

| Paso | Qué hace | Módulos |
|---|---|---|
| 1 | Descarga ESCALE, ENLA (todos los grados que ofrece SICRECE), Contraloría y MEF (INFOBRAS solo si se pide) | `main`, `scraper_*`, `descarga_mef` |
| 2 | Tablas de ESCALE (+ indicadores ampliados) y ENLA (+ niveles de logro) y catálogo de variables | `extraccion`, `escale_ampliado`, `catalogo_escale` |
| 3 | Quita nombres de personas de los comentarios ya guardados | `datos_personales`, `utils` |
| 4 | Proyecto PDF (fases 1 a 4) y anexos Excel de la Contraloría (incluido el anexo 03) | `main_pdf` y sus módulos |
| 5 | **NLP de las causas de paralización** (reglas + modelo de apoyo + macro-categorías) | `nlp_causas` |
| 6 | Tablas del producto final y **CSV único del dashboard** | `producto_final`, `dashboard` |
| 7 | Diccionario, auditoría de datos personales, inventario y **auditoría de calidad** | `diccionario`, `datos_personales`, `inventario_datos`, `auditoria_calidad` |"""),
    texto("## 0. Opciones"),
    codigo('''from types import SimpleNamespace

import pandas as pd

import auditoria_calidad
import catalogo_escale
import config
import datos_personales
import diccionario
import escale_ampliado
import inventario_datos
import main
import main_pdf
import nlp_causas
import pipeline_completo
import producto_final
import texto_nlp
import utils

pd.set_option("display.width", 200, "display.max_columns", 40, "display.max_colwidth", 70)

# ---------------- opciones ----------------
DESCARGAR = False          # True: consulta ESCALE, ENLA, Contraloría y MEF (Chrome visible + internet, ~15 min). False: usa data/raw tal como está
INCLUIR_INFOBRAS = False   # True: ADEMAS vuelve a leer INFOBRAS. Cambia el listado (hay obras que dejaron de estar paralizadas) y mueve los números
FORZAR = False             # True: rehace todo aunque ya esté hecho (muy lento)
TODO_DE_UNA_VEZ = False    # True: al final corre pipeline_completo.ejecutar() de nuevo (equivale a «python src/pipeline_completo.py»)

FUENTES = list(pipeline_completo.FUENTES_POR_DEFECTO) + (["infobras"] if INCLUIR_INFOBRAS else [])
ARGS = SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES)
print("Carpeta del proyecto:", config.RAIZ.name)
print("Descargar:", DESCARGAR, "| fuentes:", FUENTES)'''),
    texto("""## 1. Descarga de las fuentes

| Fuente | Cómo | Notas |
|---|---|---|
| ESCALE (Censo Educativo) | Chrome visible (Selenium) | Archivos `.zip` por año |
| ENLA (UMC y SICRECE) | Chrome visible | PDF de reportes + JSON por región de **todos los grados que devuelve SICRECE** (2.°, 4.° y 6.° de primaria; 2.° de secundaria) |
| Contraloría (gob.pe) | Chrome visible | 21 informes PDF (jun-2022 a jun-2026) y sus anexos Excel (1, 2 y 3) |
| MEF (Datos Abiertos) | Una petición HTTP | `FORMATO_12B.csv` (~180 MB): devengado por CUI. Una vez al mes |
| INFOBRAS | Chrome visible | **Solo si se pide**: es una foto (27-oct y 11-nov-2026). La ficha carga las coordenadas con JavaScript unos segundos después: el programa espera a que terminen |

Reglas de cortesía para todas: pausa de 2 a 5 s, 3 reintentos, nada en paralelo, UA con el nombre del proyecto y **lo ya descargado se salta**.
Los archivos de `data/raw` nunca se modifican. Cada descarga queda en `docs/registro_fuentes.csv`."""),
    codigo('''if DESCARGAR:
    main.descargar(ARGS)
else:
    print("DESCARGAR = False: no se consulta ningún portal. Lo que hay en data/raw:")
inventario_datos.inventario_raw()'''),
    texto("""## 2. Tablas de ESCALE y ENLA
`extraccion` convierte los archivos crudos en `escale_infraestructura.csv` (por distrito y año), `enla_regiones.csv` (% Satisfactorio por región y grado) y `enla_niveles_logro.csv` (los 4 niveles).
`escale_ampliado` calcula 16 indicadores más de infraestructura por distrito (internet, agua y luz todos los días, rampas, antigüedad, estado de techos...) con el Censo 2025.
`catalogo_escale` lista las 331 variables de los archivos de ESCALE con su descripción oficial. Los nombres de lugares quedan en MAYÚSCULAS sin tildes (la Ñ se conserva: es una letra)."""),
    codigo('''main.extraer(SimpleNamespace(anio_inicio=config.ANIO_INICIO, solo=None, forzar=FORZAR, headless=False, fuentes=FUENTES))
catalogo = catalogo_escale.construir()
ampliado = escale_ampliado.construir()
ampliado.head(3)'''),
    codigo('''for nombre in ("escale_infraestructura", "escale_distrito_ampliado", "enla_regiones", "enla_niveles_logro"):
    t = pd.read_csv(config.PROCESSED / f"{nombre}.csv", dtype={"ubigeo": str}, encoding="utf-8-sig")
    print(f"{nombre}: {t.shape[0]} filas x {t.shape[1]} columnas | años: {sorted(t.anio.unique())}")
niveles = pd.read_csv(config.PROCESSED / "enla_niveles_logro.csv", encoding="utf-8-sig")
niveles.groupby(["anio", "evaluacion", "grado"]).size().rename("regiones x 2 áreas").reset_index()'''),
    texto("""## 3. Datos personales
Las entidades escriben a veces el nombre de su residente o supervisor en los comentarios libres (INFOBRAS y MEF). **La regla del proyecto es no guardar nombres de personas.**
`utils.omitir_nombres` reemplaza esos nombres por `[NOMBRE OMITIDO]` apenas se lee el comentario; este paso vuelve a pasar el filtro por lo ya guardado (se puede repetir sin cambiar nada).
Del MEF ni siquiera se guardan los dos campos narrativos que no se usan."""),
    codigo('''ejemplos = ["SUPERVISOR DE OBRA: ING. JUAN PEREZ QUISPE RESIDENTE DE OBRA: MARIA LOPEZ RAMOS",
            "aprobada por el supervisor de obra, Ing. Walter Martos, cumple los requisitos",
            "NO SE TIENE ASIGNACIÓN PRESUPUESTAL PARA PROSEGUIR CON LA EJECUCIÓN",
            "con supervisión del Consorcio Supervisor Villa María"]
print(pd.DataFrame({"antes": ejemplos, "despues": [utils.omitir_nombres(e) for e in ejemplos]}).to_string())
datos_personales.limpiar()'''),
    texto("""## 4. Proyecto PDF (fases 1 a 4)
1. **Inventario** de los PDF (informes de la Contraloría, reportes de ENLA y ESCALE): ninguno es un escaneo, no hace falta OCR.
2. **Texto y tablas** de cada PDF (pdfplumber/pypdf): compactar celdas vacías, unir tablas partidas entre páginas, limpiar números; cada tabla se cataloga por tipo.
3. **Tablas finales y validación:** cifras oficiales (país, sector, departamento), causales, distribuciones, ENLA del PDF; y las de los anexos Excel de la Contraloría
   (datos por obra, panel histórico, PIM, modalidad, evento, servicios de control y **anexo 03: servicios de control por obra**). Como el orden de las columnas cambia entre informes,
   el rol de cada columna se decide por la **magnitud** de sus valores (obras < saldo ≤ costo); los informes de 2022 se leen del texto de la página. Cada cifra conserva `fuente_pdf`, `pagina` y `tabla_n`.
   Los totales se validan contra la suma de las filas y contra los anexos Excel.
4. **Texto, causas e INFOBRAS:** citas sobre educación, términos más característicos de cada año (TF-IDF), ubigeo de cada obra y las tablas ampliadas de INFOBRAS (avances, paralizaciones, 429 fichas).
Un PDF ya procesado no se vuelve a procesar. La primera vez desde cero tarda ~20 minutos; con lo ya hecho, ~2 minutos."""),
    codigo("main_pdf.ejecutar(4, FORZAR)"),
    codigo('''inv = pd.read_csv(config.INVENTARIO_PDF, dtype=str, encoding="utf-8-sig")
cat = pd.read_csv(config.CATALOGO_TABLAS, dtype=str, keep_default_na=False, encoding="utf-8-sig")
print(len(inv), "PDF |", len(cat), "tablas detectadas,", int((cat.estado == "guardada").sum()), "guardadas")
inv.groupby(["fuente", "tipo_texto"]).agg(documentos=("archivo", "count"), paginas=("paginas", lambda s: s.astype(int).sum()))'''),
    codigo('''v = pd.read_csv(config.DOCS / "validacion_pdf.csv", encoding="utf-8-sig")
x = pd.read_csv(config.DOCS / "validacion_excel.csv", encoding="utf-8-sig")
a = pd.read_csv(config.DOCS / "validacion_anexos_excel.csv", encoding="utf-8-sig")
print(f"PDF: {len(v)} comprobaciones, {(~v.ok).sum()} falla (error del propio informe de jun-2023)")
print(f"PDF vs Excel de la Contraloría: {len(x)} comparaciones, {(~x.ok_10pct).sum()} fuera del 10 % (set-2023 y set-2025: errores del PDF)")
print(f"Panel y tablas de los anexos Excel: {len(a)} comprobaciones, {(~a.ok).sum()} no pasan (explicadas en docs/hallazgos_pdf.md)")
pd.read_csv(config.DOCS / "validacion_infobras.csv", encoding="utf-8-sig")'''),
    texto("""### 4.1 Texto narrativo de los informes (citas y términos)
`texto_nlp.citas_educacion` toma las oraciones de la narrativa que hablan de educación (dejando fuera las filas de tabla, que tienen muchos números).
`texto_nlp.frecuencia_terminos` cuenta palabras y pares de palabras por año y los ordena por **TF-IDF**: frecuencia relativa en el año × log(años / años en que aparece).
Así suben los términos propios de un informe y bajan los que aparecen siempre («gobierno», «inversión»)."""),
    codigo('''terminos = pd.read_csv(config.PROCESSED / "frecuencia_terminos.csv", encoding="utf-8-sig")
print("Años:", sorted(terminos.anio.unique()))
terminos[(terminos.anio == terminos.anio.max()) & (terminos.tipo == "par")].head(8)'''),
    texto("""## 5. NLP de las causas de paralización

**Entrada:** tres textos por obra: (1) los **comentarios de INFOBRAS** de todos los meses paralizados leídos (310 de las 429 obras tienen comentario útil),
(2) la **causal oficial** de la Contraloría y (3) la **problemática** que la entidad registra en el MEF.

**Método** (código en la celda `%%modulo nlp_causas` de la Parte A; todo explicable):
1. **Normalizar:** minúsculas, sin tildes, sin fechas ni frases de relleno («No se registraron comentarios»).
2. **Puntuar con reglas:** 14 grupos de palabras clave (`config.CAUSAS_REGLAS`). Cada grupo suma 1 punto por el primer patrón que aparece y 0.5 por cada patrón distinto adicional (máximo 2), así ningún grupo gana solo por tener más patrones. Un texto puede tener varias causas.
3. **Negación:** en las causas «de presencia» (clima, conflictos sociales, controversias, pandemia, interferencias) se descartan las menciones precedidas de «no», «sin» o «permiten» («las condiciones climatológicas permiten su ejecución» no es una causa).
4. **Combinar fuentes** con pesos: causal oficial 3, comentarios del último tramo de paralización 2, problemática del MEF 1.5, comentarios de tramos anteriores 0.5. La causa principal es la de mayor puntaje; hasta 2 causas secundarias (≥ la mitad del puntaje). Los grupos de **estado** (obra concluida o en marcha, sin restricciones) solo se asignan si no hay ninguna causa real.
5. **Modelo de apoyo balanceado:** TF-IDF + regresión logística con `class_weight="balanced"` (cada clase pesa igual aunque unas tengan 600 ejemplos y otras 14), entrenada con los textos que las reglas clasifican sin ambigüedad. Solo se usa cuando las reglas no encuentran nada y la probabilidad es ≥ 0.60. Se mide con validación cruzada de 5 pliegues.
   **Cómo leer sus métricas:** el modelo se entrena con las etiquetas que ponen las reglas, así que su F1 mide **cuánto reproduce a las reglas**, no la exactitud frente a una causa verificada a mano. Sirve como **control de consistencia**. En la corrida actual **no clasificó ninguna obra** (`Método: {'reglas': 429}` en la sección 6.1): las reglas encontraron causa, o no había texto, en todas.
6. **Macro-categorías** para el dashboard (8 en vez de 16 grupos): `config.CAUSAS_MACRO`."""),
    codigo('''reglas = pd.DataFrame([(g, len(p), config.CAUSAS_MACRO[g], "estado" if g in config.CAUSAS_ESTADO else "causa") for g, p in config.CAUSAS_REGLAS.items()],
                      columns=["grupo", "patrones", "macro_categoria", "clase"])
reglas'''),
    codigo('''pruebas = ["FALTA DE ASIGNACIÓN PRESUPUESTAL PARA CULMINAR LA OBRA",
           "Paralizada por lluvias intensas y deslizamiento del talud",
           "Las condiciones climatológicas permiten su ejecución sin ningún problema",
           "Se resolvió el contrato por incumplimiento y se inició el proceso arbitral",
           "NO EXISTE RESTRICCIONES A LA FECHA.",
           "El avance físico se determinó respecto al costo del Expediente Técnico"]
filas = []
for t in pruebas:
    r = nlp_causas.analizar([("texto", t, 1.0)])
    filas.append({"texto": t, "puntajes": nlp_causas.puntuar(nlp_causas.normalizar(t)), "principal": r["principal"], "secundarias": r["secundarias"]})
pd.DataFrame(filas)'''),
    codigo('''# Las 13 causales oficiales de la Contraloría deben caer en el grupo esperado (prueba de las reglas)
fallas = [(c, esperado, texto_nlp.clasificar_causa(c)) for c, esperado in texto_nlp.PRUEBA_REGLAS.items() if texto_nlp.clasificar_causa(c) != esperado]
print(f"{len(texto_nlp.PRUEBA_REGLAS) - len(fallas)} de {len(texto_nlp.PRUEBA_REGLAS)} causales oficiales caen en su grupo.", "Fallan:" if fallas else "", fallas or "")'''),
    texto("### 5.1 Modelo de apoyo: entrenamiento y evaluación"),
    codigo('''par = pd.read_csv(config.PROCESSED / "infobras_paralizaciones.csv", dtype=str, keep_default_na=False, encoding="utf-8-sig")
mef = pd.read_csv(config.PROCESSED / "mef_f12b_obras.csv", dtype=str, keep_default_na=False, encoding="utf-8-sig")
textos_comentarios = [t for lista in nlp_causas.textos_de_infobras(par).values() for t, _ in lista]
modelo, metricas = nlp_causas.entrenar(textos_comentarios + list(mef.ult_problema))
print("Textos de entrenamiento: comentarios de INFOBRAS", len(textos_comentarios), "| problemáticas del MEF", int((mef.ult_problema != "").sum()))
metricas'''),
    texto("""Cómo leer la tabla: **precision** = de lo que el modelo dice que es de esa clase, cuánto acierta; **recall** = de lo que de verdad es de esa clase, cuánto encuentra; **f1** = promedio de ambos;
**macro avg** = promedio simple entre clases (cada clase pesa igual, por eso es la cifra que importa cuando las clases están desbalanceadas).
La «verdad» aquí son las etiquetas de las reglas sobre textos sin ambigüedad: mide si el modelo es **consistente** con las reglas, no si estas son perfectas; por eso además se revisa a mano una muestra.
`permisos_licencias` y `personal_clave` tienen pocos ejemplos: es una limitación real de los datos, no se inventan ejemplos.
**Importante al presentar:** un F1 alto dice que las reglas son coherentes entre sí, no que acierten la causa real en ese porcentaje."""),
    texto("""## 6. Producto final y CSV único del dashboard
Se arman cinco tablas intermedias (`data/interim/componentes`: obras, regiones, series y causales) y se unen en **un solo CSV en formato largo**: `data/final/dashboard_obras.csv`.
La columna `tipo_registro` dice qué representa cada fila; hay que **filtrar por ella** en cada gráfico para no mezclar niveles ni contar dos veces.
La columna `alertas_calidad` marca los datos dudosos que vienen así de la fuente (sin corregirlos)."""),
    codigo('''tablas, validacion = producto_final.construir()
print(f"{len(validacion)} comprobaciones, {(~validacion.ok).sum()} fallan")
validacion[["tabla", "comprobacion", "valor", "esperado", "ok"]]'''),
    texto("### 6.1 Resultado del NLP sobre las 429 obras"),
    codigo('''obras = tablas["obras_maestra"]
distribucion = pd.DataFrame({"obras": obras.causa_grupo_final.value_counts(), "paralizadas_hoy": obras[obras.paralizada_hoy].causa_grupo_final.value_counts()}).fillna(0).astype(int)
distribucion["macro_categoria"] = distribucion.index.map(config.CAUSAS_MACRO)
distribucion.sort_values("obras", ascending=False)'''),
    codigo('''macro = obras.groupby("causa_macro").agg(obras=("codigo_infobras", "count"), paralizadas_hoy=("paralizada_hoy", "sum"))
macro["% de obras"] = (100 * macro.obras / macro.obras.sum()).round(1)
print("Ninguna macro-categoría supera el 50 %:", macro["% de obras"].max() <= 50)
macro.sort_values("obras", ascending=False)'''),
    codigo('''print("Fuente que más aportó:", obras.causa_fuente.value_counts().to_dict())
print("Confianza:", obras.causa_confianza.replace("", "sin causa").value_counts().to_dict())
print("Método:", obras.causa_metodo.value_counts().to_dict())
# acuerdo entre fuentes: obras que tienen causa clara en dos fuentes a la vez
claras = lambda s: ~s.isin(["otros", "sin_informacion", "sin_restricciones", "obra_concluida_o_en_marcha"])
ambas = obras[claras(obras.causa_grupo_infobras) & claras(obras.causa_grupo_contraloria)]
print(f"Comentarios de INFOBRAS vs causal oficial: {len(ambas)} obras con causa clara en ambas; coinciden {100 * (ambas.causa_grupo_infobras == ambas.causa_grupo_contraloria).mean():.0f} %")'''),
    texto("### 6.2 El CSV único"),
    codigo('''dashboard = pd.read_csv(config.FINAL / "dashboard_obras.csv", dtype={"cod_departamento": str, "ubigeo": str, "codigo_infobras": str, "cui": str, "escale_codlocal": str}, encoding="utf-8-sig")
print(dashboard.shape[0], "filas x", dashboard.shape[1], "columnas")
dashboard.groupby("tipo_registro").agg(filas=("tipo_registro", "size"), n_obras=("n_obras", "sum"), desde=("fecha_corte", "min"), hasta=("fecha_corte", "max"))'''),
    codigo('''# Ejemplos de cómo se filtra: obras paralizadas hoy por macro-categoría de causa, y evolución de Educación en el país
hoy = dashboard[(dashboard.tipo_registro == "obra_infobras") & (dashboard.paralizada_hoy == True)]
print(hoy.groupby("causa_macro").n_obras_paralizadas.sum().sort_values(ascending=False).to_dict())
dashboard[dashboard.tipo_registro == "pais_educacion_corte"][["fecha_corte", "n_obras", "pct_obras", "educacion_corregida"]].tail(6)'''),
    codigo('''# Avisos de calidad de las obras de INFOBRAS (la columna alertas_calidad no corrige nada: marca lo dudoso)
ob = dashboard[dashboard.tipo_registro == "obra_infobras"]
ob.alertas_calidad.fillna("(sin alertas)").str.split("|").explode().value_counts().rename("obras")'''),
    texto("""**Para Power BI:** *Obtener datos → Texto/CSV → `data/final/dashboard_obras.csv`* (codificación UTF-8, separador coma, punto decimal). Cambiar `cod_departamento`, `ubigeo`, `codigo_infobras`, `cui` y `escale_codlocal` a **Texto**.
Para el mapa usar **`latitud_mapa`/`longitud_mapa`**: son las de INFOBRAS (412 obras) y, en las 17 que INFOBRAS no tiene, una ubicación **aproximada** de ESCALE (el local que declara el CUI de la obra o el centro de los colegios del distrito). `coordenada_origen` dice cuál es cuál: conviene darles otro color o forma en el mapa. `latitud`/`longitud` siguen siendo solo las de INFOBRAS. `dashboard_obras_diccionario.csv` explica cada columna y en qué tipos de registro se llena.
Medidas de ejemplo: obras paralizadas = `SUM(n_obras_paralizadas)` con el filtro `tipo_registro = "obra_infobras"`; monto = `SUM(costo_actualizado_soles)` con el mismo filtro."""),
    texto("""## 7. Diccionario, auditorías e inventario
* **Diccionario** (`docs/diccionario.csv`): describe cada columna de cada tabla; si falta una descripción, el programa falla a propósito.
* **Auditoría de datos personales:** busca nombres de personas con patrones propios en todas las tablas; si encuentra alguno, el proceso se detiene.
* **Inventario** (`docs/inventario_datos.md`): qué datos hay, de qué periodo y qué necesidades del proyecto cubren.
* **Auditoría de calidad** (`docs/auditoria_calidad.csv`): revisa el CSV único (estructura, texto, códigos, rangos, fechas, consistencia entre tipos, obligatorios); si hay un ERROR, el proceso se detiene."""),
    codigo('''dic = diccionario.escribir_diccionario()
print(dic.tabla.nunique(), "tablas,", len(dic), "columnas descritas")
hallazgos = datos_personales.auditoria_o_falla()
print("Auditoría de datos personales:", len(hallazgos), "hallazgos")
tablas_inv, raw_inv, necesidades = inventario_datos.construir()
tablas_inv.drop(columns="archivo")'''),
    codigo('''calidad = auditoria_calidad.auditoria_o_falla()
print("Errores:", int((calidad.nivel == "ERROR").sum()), "| avisos:", int((calidad.nivel == "aviso").sum()))
calidad'''),
    codigo("necesidades"),
    texto("""## Todo de una vez
`TODO_DE_UNA_VEZ = True` (celda de opciones) corre `pipeline_completo.ejecutar()`, que hace los 9 pasos seguidos: es lo mismo que `python src\\pipeline_completo.py` (o `ejecutar.bat`).
Al terminar devuelve la lista de pasos que fallaron (vacía si todo salió bien)."""),
    codigo('''if TODO_DE_UNA_VEZ:
    fallidos = pipeline_completo.ejecutar(FUENTES, sin_descarga=not DESCARGAR, forzar=FORZAR)
    print("Pasos fallidos:", fallidos or "ninguno")
else:
    print("TODO_DE_UNA_VEZ = False: ya se ejecutaron los pasos uno por uno arriba.")'''),
    texto("""## Límites y calidad del dato

Lo que el proyecto **no tiene o no puede afirmar**, con su tamaño. Ningún dato dudoso se corrigió en silencio: se marca en `alertas_calidad` o se explica aquí.

## 1. No existe en la fuente
- **Coordenadas:** 17 de las 429 obras no tienen coordenadas en INFOBRAS. En el mapa se usan coordenadas **aproximadas** de ESCALE (el local escolar que declara el CUI de la obra o el centro de los colegios del distrito; `coordenada_origen`). En las obras que sí tienen coordenadas, ese centro queda a unos 3 km de la ubicación real (mediana).
- **Contraloría antes de sep-2023:** solo hay cifras agregadas en los PDF; no hay datos obra por obra.
- **Costos:** 98 filas de la Contraloría traen costo 0 o vacío y 9 traen saldo mayor que el costo. Están marcadas en `alertas_calidad`, sin corregir.
- **Expediente técnico:** 3 obras sin ejecución tienen expediente técnico 0 o vacío en INFOBRAS.
- **MEF:** 53 obras no aparecen en el Formato 12-B; 15 de ellas tienen CUI «NO ASOCIADO».

## 2. El portal no respondió
- **ENLA:** SICRECE no devolvió datos de 6.º de primaria 2022, 2.º de primaria 2023 ni 5.º de secundaria 2025 (3 intentos cada uno).
- **ENLA por UGEL o provincia:** no se consiguió; solo hay datos por región.

## 3. Fuera del alcance (decisión por tiempo)
- **ESCALE ampliado:** los 16 indicadores nuevos son solo de 2025 (para 2022-2024 habría que mapear los nombres de variable de cada año). Quedan 123 variables candidatas en el catálogo sin extraer. Los 5 indicadores principales sí tienen serie 2022-2025.
- **Anexo 03 de la Contraloría:** solo se usa el corte de marzo de 2026 (el de junio no se publicó). 43 % de las obras figuran ahí; vacío = la obra no figura.
- **INFOBRAS no se actualizó:** es una foto del 27-oct y del 11-nov-2026. Volver a leerlo cambiaría los números.

## 4. Calidad del dato e interpretación
- **INFOBRAS y la Contraloría son poblaciones distintas:** 198 obras de Educación paralizadas en INFOBRAS (27-oct) frente a 341 en la lista de la Contraloría (jun-2026); solo 110 están en ambas. Las 429 obras del tablero son la unión de las dos.
- **Las fuentes tienen fechas distintas:** INFOBRAS, 11-nov-2026; Contraloría, hasta jun-2026; ESCALE y ENLA, hasta 2025; MEF, foto mensual. El tablero compara datos de momentos distintos.
- **El estado cambia rápido:** de las 198 obras paralizadas el 27-oct, 20 ya estaban en ejecución el 11-nov. De las 231 obras de la Contraloría que ya no figuraban como paralizadas, 130 están en ejecución y 95 finalizadas.
- **Causas:** la causa principal sale sobre todo de la causal oficial de la Contraloría (310 de 429 obras); los comentarios de INFOBRAS decidieron en 83 y el MEF en 24. Comentarios y causal oficial coinciden solo en 49 % de las obras donde ambos dicen algo claro. 12 obras quedan sin causa clasificada.
- **Modelo de NLP:** no clasificó ninguna obra (las 429 causas salen de las reglas). Su F1 de 0.885 mide cuánto reproduce a las reglas con las que se entrenó, no la exactitud frente a una revisión manual: es un control de consistencia.
- **INFOBRAS se contradice a sí mismo:** en 6 obras el avance físico del encabezado no coincide con el último avance de su propia tabla. En 4 obras la ubicación estaba mal (2 figuraban en Huancavelica y son de Ica; 2 en el distrito Chavín de Huántar y son de Huanta); se corrigió el ubigeo a mano con el motivo documentado.
- **MEF frente a INFOBRAS:** 41 obras tienen devengado mayor al costo y en 61 el avance físico de INFOBRAS difiere más de 30 puntos del MEF.
- **Alertas:** 206 de las 429 obras tienen al menos una alerta de calidad.
- **Relación no es causa:** que una región tenga más obras paralizadas y peores resultados en ENLA o peor infraestructura no prueba que una cosa cause la otra.

## Hallazgos que no son falta de datos
- **Loreto y Tumbes no tienen obras de Educación paralizadas** ni en la lista de la Contraloría de jun-2026 (tienen 35 y 10 obras paralizadas de otros sectores) ni en INFOBRAS. En el mapa valen 0, no «sin dato».

Este texto también está en `docs/limites_y_calidad.md`."""),
    texto("""## Qué leer después
* `docs/limites_y_calidad.md` — lo que el proyecto no tiene o no puede afirmar, con su tamaño (la sección de arriba).
* `docs/producto_final.md` — qué contiene el CSV único, cómo usarlo y los límites que hay que decir al presentar.
* `docs/hallazgos_pdf.md` — qué se validó, qué no coincide y por qué.
* `docs/diccionario.csv` y `data/final/dashboard_obras_diccionario.csv` — qué significa cada columna.
* `docs/auditoria_calidad.csv` y `docs/nlp_causas_metricas.csv` — resultados de las auditorías y del modelo de apoyo."""),
]


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
